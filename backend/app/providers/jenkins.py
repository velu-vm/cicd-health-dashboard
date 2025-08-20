import aiohttp
import os
import base64
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class JenkinsProvider:
    """Provider for Jenkins CI/CD pipelines"""
    
    def __init__(self):
        self.url = os.getenv("JENKINS_URL")
        self.username = os.getenv("JENKINS_USERNAME")
        self.api_token = os.getenv("JENKINS_API_TOKEN")
        
        if self.username and self.api_token:
            credentials = f"{self.username}:{self.api_token}"
            self.auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
        else:
            self.auth_header = None
    
    async def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Fetch all Jenkins jobs"""
        if not self.url or not self.auth_header:
            logger.warning("Jenkins credentials not configured")
            return []
        
        url = f"{self.url}/api/json"
        params = {"tree": "jobs[name,url,color,builds[number,url,result,timestamp,duration]]"}
        headers = {"Authorization": self.auth_header}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("jobs", [])
                    else:
                        logger.error(f"Failed to fetch Jenkins jobs: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching Jenkins jobs: {e}")
            return []
    
    async def fetch_job_details(self, job_name: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information about a specific Jenkins job"""
        if not self.url or not self.auth_header:
            return None
        
        url = f"{self.url}/job/{job_name}/api/json"
        params = {"tree": "name,url,color,description,builds[number,url,result,timestamp,duration,actions[*]]"}
        headers = {"Authorization": self.auth_header}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to fetch job details: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching job details: {e}")
            return None
    
    async def fetch_build_details(
        self, 
        job_name: str, 
        build_number: int
    ) -> Optional[Dict[str, Any]]:
        """Fetch detailed information about a specific build"""
        if not self.url or not self.auth_header:
            return None
        
        url = f"{self.url}/job/{job_name}/{build_number}/api/json"
        params = {"tree": "number,url,result,timestamp,duration,actions[*],changeSet[*]"}
        headers = {"Authorization": self.auth_header}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to fetch build details: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching build details: {e}")
            return None
    
    async def fetch_pipeline_status(self, job_name: str) -> Optional[Dict[str, Any]]:
        """Fetch current status of a Jenkins pipeline job"""
        if not self.url or not self.auth_header:
            return None
        
        url = f"{self.url}/job/{job_name}/lastBuild/api/json"
        params = {"tree": "number,url,result,timestamp,duration,building,executor[*]"}
        headers = {"Authorization": self.auth_header}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        # Job exists but no builds yet
                        return {"status": "unknown", "building": False}
                    else:
                        logger.error(f"Failed to fetch pipeline status: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching pipeline status: {e}")
            return None
    
    def parse_job_data(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Jenkins job data into standardized format"""
        builds = job_data.get("builds", [])
        latest_build = builds[0] if builds else None
        
        return {
            "name": job_data.get("name"),
            "status": self._map_status(job_data.get("color")),
            "last_build_number": latest_build.get("number") if latest_build else None,
            "last_build_url": latest_build.get("url") if latest_build else None,
            "last_build_time": self._timestamp_to_datetime(latest_build.get("timestamp")) if latest_build else None,
            "build_count": len(builds),
            "metadata": {
                "jenkins_url": job_data.get("url"),
                "color": job_data.get("color")
            }
        }
    
    def parse_build_data(self, build_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Jenkins build data into standardized format"""
        return {
            "build_number": build_data.get("number"),
            "status": self._map_build_result(build_data.get("result")),
            "start_time": self._timestamp_to_datetime(build_data.get("timestamp")),
            "end_time": self._calculate_end_time(
                build_data.get("timestamp"), 
                build_data.get("duration")
            ),
            "duration": build_data.get("duration") // 1000 if build_data.get("duration") else None,  # Convert to seconds
            "build_url": build_data.get("url"),
            "metadata": {
                "building": build_data.get("building", False),
                "executor": build_data.get("executor", {})
            }
        }
    
    def _map_status(self, color: str) -> str:
        """Map Jenkins color to standardized status"""
        color_mapping = {
            "blue": "success",
            "red": "failed",
            "yellow": "unstable",
            "grey": "disabled",
            "aborted": "cancelled",
            "notbuilt": "unknown"
        }
        return color_mapping.get(color, "unknown")
    
    def _map_build_result(self, result: str) -> str:
        """Map Jenkins build result to standardized status"""
        result_mapping = {
            "SUCCESS": "success",
            "FAILURE": "failed",
            "UNSTABLE": "unstable",
            "ABORTED": "cancelled",
            "NOT_BUILT": "unknown"
        }
        return result_mapping.get(result, "unknown")
    
    def _timestamp_to_datetime(self, timestamp: Optional[int]) -> Optional[str]:
        """Convert Jenkins timestamp to ISO format"""
        if timestamp:
            try:
                dt = datetime.fromtimestamp(timestamp / 1000)  # Jenkins uses milliseconds
                return dt.isoformat()
            except (ValueError, TypeError):
                return None
        return None
    
    def _calculate_end_time(self, start_timestamp: Optional[int], duration: Optional[int]) -> Optional[str]:
        """Calculate end time based on start timestamp and duration"""
        if start_timestamp and duration:
            try:
                start_dt = datetime.fromtimestamp(start_timestamp / 1000)
                end_dt = start_dt + datetime.timedelta(milliseconds=duration)
                return end_dt.isoformat()
            except (ValueError, TypeError):
                return None
        return None
