import aiohttp
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GitHubActionsProvider:
    """Provider for GitHub Actions CI/CD pipelines"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def fetch_workflow_runs(
        self, 
        owner: str, 
        repo: str, 
        branch: str = "main",
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """Fetch workflow runs for a repository"""
        if not self.token:
            logger.warning("GitHub token not configured")
            return []
        
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs"
        params = {
            "branch": branch,
            "per_page": per_page,
            "status": "completed"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("workflow_runs", [])
                    else:
                        logger.error(f"Failed to fetch GitHub Actions runs: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching GitHub Actions runs: {e}")
            return []
    
    async def fetch_workflow_run_details(
        self, 
        owner: str, 
        repo: str, 
        run_id: int
    ) -> Optional[Dict[str, Any]]:
        """Fetch detailed information about a specific workflow run"""
        if not self.token:
            return None
        
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs/{run_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to fetch workflow run details: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching workflow run details: {e}")
            return None
    
    async def fetch_repository_workflows(
        self, 
        owner: str, 
        repo: str
    ) -> List[Dict[str, Any]]:
        """Fetch all workflows for a repository"""
        if not self.token:
            return []
        
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/workflows"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("workflows", [])
                    else:
                        logger.error(f"Failed to fetch workflows: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching workflows: {e}")
            return []
    
    def parse_workflow_run(self, run_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse GitHub Actions workflow run data into standardized format"""
        return {
            "build_number": run_data.get("run_number"),
            "status": self._map_status(run_data.get("conclusion") or run_data.get("status")),
            "start_time": run_data.get("created_at"),
            "end_time": run_data.get("updated_at"),
            "duration": self._calculate_duration(
                run_data.get("created_at"), 
                run_data.get("updated_at")
            ),
            "commit_hash": run_data.get("head_sha"),
            "commit_message": run_data.get("head_commit", {}).get("message"),
            "author": run_data.get("head_commit", {}).get("author", {}).get("name"),
            "build_url": run_data.get("html_url"),
            "metadata": {
                "workflow_id": run_data.get("workflow_id"),
                "workflow_name": run_data.get("name"),
                "trigger": run_data.get("event"),
                "actor": run_data.get("actor", {}).get("login")
            }
        }
    
    def _map_status(self, status: str) -> str:
        """Map GitHub Actions status to standardized status"""
        status_mapping = {
            "success": "success",
            "failure": "failed",
            "cancelled": "cancelled",
            "skipped": "skipped",
            "in_progress": "running",
            "queued": "queued",
            "waiting": "waiting"
        }
        return status_mapping.get(status, "unknown")
    
    def _calculate_duration(self, start_time: str, end_time: str) -> Optional[int]:
        """Calculate duration in seconds between start and end times"""
        try:
            start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            return int((end - start).total_seconds())
        except (ValueError, TypeError):
            return None
