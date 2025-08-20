import asyncio
import logging
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
import aiohttp
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CICDPoller:
    """Background worker for polling CI/CD providers"""
    
    def __init__(self):
        self.api_base_url = os.getenv("VITE_API_BASE_URL", "http://localhost:8000")
        self.poll_interval = int(os.getenv("WORKER_POLL_INTERVAL", "300"))  # 5 minutes default
        self.max_concurrent_jobs = int(os.getenv("WORKER_MAX_CONCURRENT_JOBS", "10"))
        self.running = False
        self.session = None
        
    async def start(self):
        """Start the polling worker"""
        logger.info("Starting CI/CD Poller")
        self.running = True
        
        # Create HTTP session
        self.session = aiohttp.ClientSession()
        
        try:
            while self.running:
                await self.poll_all_providers()
                await asyncio.sleep(self.poll_interval)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Unexpected error in poller: {e}")
        finally:
            await self.cleanup()
    
    async def stop(self):
        """Stop the polling worker"""
        logger.info("Stopping CI/CD Poller")
        self.running = False
    
    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
        logger.info("CI/CD Poller stopped")
    
    async def poll_all_providers(self):
        """Poll all configured CI/CD providers"""
        logger.info("Starting provider polling cycle")
        
        # Get list of pipelines to poll
        pipelines = await self.get_pipelines()
        
        if not pipelines:
            logger.info("No pipelines configured for polling")
            return
        
        # Process pipelines with concurrency limit
        semaphore = asyncio.Semaphore(self.max_concurrent_jobs)
        tasks = []
        
        for pipeline in pipelines:
            task = asyncio.create_task(
                self.poll_pipeline_with_semaphore(semaphore, pipeline)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log results
        success_count = sum(1 for r in results if not isinstance(r, Exception))
        error_count = len(results) - success_count
        
        logger.info(f"Polling cycle completed: {success_count} successful, {error_count} errors")
    
    async def poll_pipeline_with_semaphore(self, semaphore: asyncio.Semaphore, pipeline: Dict[str, Any]):
        """Poll a single pipeline with semaphore for concurrency control"""
        async with semaphore:
            return await self.poll_pipeline(pipeline)
    
    async def poll_pipeline(self, pipeline: Dict[str, Any]):
        """Poll a single pipeline"""
        try:
            pipeline_id = pipeline["id"]
            provider = pipeline["provider"]
            repository = pipeline["repository"]
            
            logger.info(f"Polling pipeline {pipeline_id} ({provider}: {repository})")
            
            # Fetch latest data from provider
            if provider == "github_actions":
                data = await self.poll_github_actions(pipeline)
            elif provider == "jenkins":
                data = await self.poll_jenkins(pipeline)
            else:
                logger.warning(f"Unknown provider: {provider}")
                return
            
            if data:
                # Update pipeline status
                await self.update_pipeline_status(pipeline_id, data)
                logger.info(f"Successfully updated pipeline {pipeline_id}")
            else:
                logger.warning(f"No data received for pipeline {pipeline_id}")
                
        except Exception as e:
            logger.error(f"Error polling pipeline {pipeline.get('id', 'unknown')}: {e}")
            raise
    
    async def poll_github_actions(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Poll GitHub Actions for pipeline data"""
        # This would integrate with the GitHub Actions provider
        # For now, return mock data
        return {
            "status": "success",
            "last_build_number": 123,
            "last_build_time": datetime.now().isoformat(),
            "last_build_url": f"https://github.com/{pipeline['repository']}/actions/runs/123"
        }
    
    async def poll_jenkins(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Poll Jenkins for pipeline data"""
        # This would integrate with the Jenkins provider
        # For now, return mock data
        return {
            "status": "success",
            "last_build_number": 456,
            "last_build_time": datetime.now().isoformat(),
            "last_build_url": f"{os.getenv('JENKINS_URL', 'http://jenkins')}/job/{pipeline['name']}/456"
        }
    
    async def get_pipelines(self) -> List[Dict[str, Any]]:
        """Get list of pipelines from the API"""
        try:
            url = f"{self.api_base_url}/api/v1/pipelines"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Failed to fetch pipelines: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching pipelines: {e}")
            return []
    
    async def update_pipeline_status(self, pipeline_id: int, data: Dict[str, Any]):
        """Update pipeline status via API"""
        try:
            url = f"{self.api_base_url}/api/v1/pipelines/{pipeline_id}"
            payload = {
                "status": data["status"],
                "last_build_number": data["last_build_number"],
                "last_build_time": data["last_build_time"],
                "last_build_url": data["last_build_url"]
            }
            
            async with self.session.put(url, json=payload) as response:
                if response.status != 200:
                    logger.error(f"Failed to update pipeline {pipeline_id}: {response.status}")
        except Exception as e:
            logger.error(f"Error updating pipeline {pipeline_id}: {e}")

async def main():
    """Main entry point"""
    poller = CICDPoller()
    
    try:
        await poller.start()
    except KeyboardInterrupt:
        await poller.stop()

if __name__ == "__main__":
    asyncio.run(main())
