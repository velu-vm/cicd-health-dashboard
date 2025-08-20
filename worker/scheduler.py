import asyncio
import logging
from typing import Dict, Any, Callable, Coroutine
from datetime import datetime, timedelta
import functools

logger = logging.getLogger(__name__)

class TaskScheduler:
    """Task scheduler for background jobs"""
    
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.running = False
        
    async def start(self):
        """Start the scheduler"""
        logger.info("Starting Task Scheduler")
        self.running = True
        
        # Start scheduled tasks
        await self.schedule_periodic_tasks()
        
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the scheduler and cancel all tasks"""
        logger.info("Stopping Task Scheduler")
        self.running = False
        
        # Cancel all running tasks
        for task_name, task in self.tasks.items():
            if not task.done():
                logger.info(f"Cancelling task: {task_name}")
                task.cancel()
        
        # Wait for all tasks to complete
        if self.tasks:
            await asyncio.gather(*self.tasks.values(), return_exceptions=True)
        
        logger.info("Task Scheduler stopped")
    
    async def schedule_periodic_tasks(self):
        """Schedule all periodic tasks"""
        # Schedule pipeline health checks every 5 minutes
        self.schedule_task(
            "pipeline_health_check",
            self.pipeline_health_check,
            interval_seconds=300
        )
        
        # Schedule cleanup tasks every hour
        self.schedule_task(
            "cleanup_old_data",
            self.cleanup_old_data,
            interval_seconds=3600
        )
        
        # Schedule metrics collection every 15 minutes
        self.schedule_task(
            "collect_metrics",
            self.collect_metrics,
            interval_seconds=900
        )
    
    def schedule_task(
        self, 
        name: str, 
        func: Callable[[], Coroutine[Any, Any, None]], 
        interval_seconds: int,
        delay_seconds: int = 0
    ):
        """Schedule a periodic task"""
        if name in self.tasks and not self.tasks[name].done():
            logger.warning(f"Task {name} is already scheduled")
            return
        
        async def periodic_wrapper():
            # Initial delay
            if delay_seconds > 0:
                await asyncio.sleep(delay_seconds)
            
            while self.running:
                try:
                    start_time = datetime.now()
                    logger.info(f"Starting scheduled task: {name}")
                    
                    await func()
                    
                    duration = (datetime.now() - start_time).total_seconds()
                    logger.info(f"Completed scheduled task: {name} in {duration:.2f}s")
                    
                except Exception as e:
                    logger.error(f"Error in scheduled task {name}: {e}")
                
                # Wait for next execution
                await asyncio.sleep(interval_seconds)
        
        task = asyncio.create_task(periodic_wrapper())
        self.tasks[name] = task
        logger.info(f"Scheduled task: {name} (every {interval_seconds}s)")
    
    async def pipeline_health_check(self):
        """Check health of all pipelines"""
        logger.info("Running pipeline health check")
        
        # This would integrate with the main application
        # For now, just log the action
        try:
            # Simulate health check
            await asyncio.sleep(1)
            logger.info("Pipeline health check completed")
        except Exception as e:
            logger.error(f"Pipeline health check failed: {e}")
    
    async def cleanup_old_data(self):
        """Clean up old build and alert data"""
        logger.info("Running data cleanup")
        
        try:
            # This would clean up old data from the database
            # For now, just log the action
            await asyncio.sleep(1)
            logger.info("Data cleanup completed")
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}")
    
    async def collect_metrics(self):
        """Collect system and pipeline metrics"""
        logger.info("Collecting metrics")
        
        try:
            # This would collect various metrics
            # For now, just log the action
            await asyncio.sleep(1)
            logger.info("Metrics collection completed")
        except Exception as e:
            logger.error(f"Metrics collection failed: {e}")
    
    def cancel_task(self, name: str):
        """Cancel a specific scheduled task"""
        if name in self.tasks:
            task = self.tasks[name]
            if not task.done():
                task.cancel()
                logger.info(f"Cancelled task: {name}")
            del self.tasks[name]
        else:
            logger.warning(f"Task {name} not found")
    
    def get_task_status(self) -> Dict[str, str]:
        """Get status of all scheduled tasks"""
        status = {}
        for name, task in self.tasks.items():
            if task.done():
                if task.cancelled():
                    status[name] = "cancelled"
                elif task.exception():
                    status[name] = f"failed: {task.exception()}"
                else:
                    status[name] = "completed"
            else:
                status[name] = "running"
        return status

async def main():
    """Main entry point for the scheduler"""
    scheduler = TaskScheduler()
    
    try:
        await scheduler.start()
    except KeyboardInterrupt:
        await scheduler.stop()

if __name__ == "__main__":
    asyncio.run(main())
