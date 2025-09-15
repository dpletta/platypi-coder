"""
Monitoring and Metrics System for Agentic Coder MCP Server

This module provides comprehensive monitoring, logging, and metrics collection
for the agent ensemble and MCP server operations.
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
import psutil
import os


@dataclass
class TaskMetrics:
    """Metrics for individual tasks."""
    task_id: str
    agent_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status: str = "running"
    error_message: Optional[str] = None
    input_size: int = 0
    output_size: int = 0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0


@dataclass
class AgentMetrics:
    """Metrics for individual agents."""
    agent_id: str
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_duration: float = 0.0
    total_duration: float = 0.0
    last_activity: Optional[datetime] = None
    current_status: str = "idle"
    memory_usage: float = 0.0
    cpu_usage: float = 0.0


@dataclass
class SystemMetrics:
    """System-wide metrics."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_available: int
    disk_usage_percent: float
    active_connections: int
    total_requests: int
    requests_per_minute: float
    error_rate: float


class MetricsCollector:
    """Collects and stores metrics for the agentic coder system."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.logger = logging.getLogger(__name__)
        
        # Metrics storage
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.system_metrics: deque = deque(maxlen=max_history)
        
        # Performance tracking
        self.request_times: deque = deque(maxlen=100)
        self.error_counts: Dict[str, int] = defaultdict(int)
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Start background collection
        self._collection_task = None
        self._start_collection()
    
    def _start_collection(self):
        """Start background metrics collection."""
        self._collection_task = asyncio.create_task(self._collect_system_metrics())
    
    async def _collect_system_metrics(self):
        """Collect system metrics periodically."""
        while True:
            try:
                await asyncio.sleep(60)  # Collect every minute
                
                # Get system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Calculate request metrics
                current_time = datetime.now()
                requests_per_minute = len(self.request_times)
                
                # Calculate error rate
                total_requests = sum(self.error_counts.values()) + requests_per_minute
                error_rate = sum(self.error_counts.values()) / max(total_requests, 1)
                
                system_metric = SystemMetrics(
                    timestamp=current_time,
                    cpu_percent=cpu_percent,
                    memory_percent=memory.percent,
                    memory_available=memory.available,
                    disk_usage_percent=disk.percent,
                    active_connections=0,  # Would need to track this
                    total_requests=total_requests,
                    requests_per_minute=requests_per_minute,
                    error_rate=error_rate
                )
                
                with self._lock:
                    self.system_metrics.append(system_metric)
                
                self.logger.debug(f"Collected system metrics: CPU {cpu_percent}%, Memory {memory.percent}%")
                
            except Exception as e:
                self.logger.error(f"Error collecting system metrics: {e}")
    
    def start_task(self, task_id: str, agent_id: str, input_size: int = 0) -> TaskMetrics:
        """Start tracking a task."""
        task_metric = TaskMetrics(
            task_id=task_id,
            agent_id=agent_id,
            start_time=datetime.now(),
            input_size=input_size,
            status="running"
        )
        
        with self._lock:
            self.task_metrics[task_id] = task_metric
            
            # Update agent metrics
            if agent_id not in self.agent_metrics:
                self.agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)
            
            agent_metric = self.agent_metrics[agent_id]
            agent_metric.total_tasks += 1
            agent_metric.current_status = "working"
            agent_metric.last_activity = datetime.now()
        
        self.logger.info(f"Started tracking task {task_id} for agent {agent_id}")
        return task_metric
    
    def complete_task(self, task_id: str, status: str = "completed", 
                     output_size: int = 0, error_message: Optional[str] = None):
        """Complete tracking a task."""
        with self._lock:
            if task_id not in self.task_metrics:
                self.logger.warning(f"Task {task_id} not found in metrics")
                return
            
            task_metric = self.task_metrics[task_id]
            task_metric.end_time = datetime.now()
            task_metric.duration = (task_metric.end_time - task_metric.start_time).total_seconds()
            task_metric.status = status
            task_metric.output_size = output_size
            task_metric.error_message = error_message
            
            # Update agent metrics
            agent_id = task_metric.agent_id
            if agent_id in self.agent_metrics:
                agent_metric = self.agent_metrics[agent_id]
                
                if status == "completed":
                    agent_metric.completed_tasks += 1
                elif status == "failed":
                    agent_metric.failed_tasks += 1
                
                agent_metric.total_duration += task_metric.duration
                agent_metric.average_duration = agent_metric.total_duration / agent_metric.total_tasks
                agent_metric.current_status = "idle"
                agent_metric.last_activity = datetime.now()
        
        self.logger.info(f"Completed tracking task {task_id} with status {status}")
    
    def record_request(self, endpoint: str, duration: float, success: bool):
        """Record API request metrics."""
        current_time = time.time()
        
        with self._lock:
            self.request_times.append(current_time)
            
            if not success:
                self.error_counts[endpoint] += 1
        
        self.logger.debug(f"Recorded request to {endpoint}: {duration:.3f}s, success={success}")
    
    def get_task_metrics(self, task_id: str) -> Optional[TaskMetrics]:
        """Get metrics for a specific task."""
        with self._lock:
            return self.task_metrics.get(task_id)
    
    def get_agent_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """Get metrics for a specific agent."""
        with self._lock:
            return self.agent_metrics.get(agent_id)
    
    def get_all_agent_metrics(self) -> Dict[str, AgentMetrics]:
        """Get metrics for all agents."""
        with self._lock:
            return dict(self.agent_metrics)
    
    def get_system_metrics(self, limit: int = 10) -> List[SystemMetrics]:
        """Get recent system metrics."""
        with self._lock:
            return list(self.system_metrics)[-limit:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a performance summary."""
        with self._lock:
            total_tasks = sum(agent.total_tasks for agent in self.agent_metrics.values())
            completed_tasks = sum(agent.completed_tasks for agent in self.agent_metrics.values())
            failed_tasks = sum(agent.failed_tasks for agent in self.agent_metrics.values())
            
            success_rate = completed_tasks / max(total_tasks, 1)
            
            avg_duration = 0.0
            if self.agent_metrics:
                total_duration = sum(agent.total_duration for agent in self.agent_metrics.values())
                avg_duration = total_duration / max(total_tasks, 1)
            
            # Get recent system metrics
            recent_metrics = list(self.system_metrics)[-5:] if self.system_metrics else []
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / max(len(recent_metrics), 1)
            avg_memory = sum(m.memory_percent for m in recent_metrics) / max(len(recent_metrics), 1)
            
            return {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": success_rate,
                "average_task_duration": avg_duration,
                "average_cpu_usage": avg_cpu,
                "average_memory_usage": avg_memory,
                "active_agents": len([a for a in self.agent_metrics.values() if a.current_status != "idle"]),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status."""
        with self._lock:
            # Check agent health
            agent_health = {}
            for agent_id, metrics in self.agent_metrics.items():
                health_status = "healthy"
                
                if metrics.failed_tasks > metrics.completed_tasks:
                    health_status = "unhealthy"
                elif metrics.failed_tasks > 0:
                    health_status = "degraded"
                
                agent_health[agent_id] = {
                    "status": health_status,
                    "total_tasks": metrics.total_tasks,
                    "success_rate": metrics.completed_tasks / max(metrics.total_tasks, 1),
                    "last_activity": metrics.last_activity.isoformat() if metrics.last_activity else None
                }
            
            # Check system health
            system_health = "healthy"
            if self.system_metrics:
                latest_metrics = self.system_metrics[-1]
                if latest_metrics.cpu_percent > 90 or latest_metrics.memory_percent > 90:
                    system_health = "critical"
                elif latest_metrics.cpu_percent > 80 or latest_metrics.memory_percent > 80:
                    system_health = "warning"
            
            return {
                "overall_status": system_health,
                "agent_health": agent_health,
                "system_metrics": asdict(self.system_metrics[-1]) if self.system_metrics else None,
                "timestamp": datetime.now().isoformat()
            }
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for external analysis."""
        with self._lock:
            return {
                "task_metrics": {tid: asdict(metric) for tid, metric in self.task_metrics.items()},
                "agent_metrics": {aid: asdict(metric) for aid, metric in self.agent_metrics.items()},
                "system_metrics": [asdict(metric) for metric in self.system_metrics],
                "performance_summary": self.get_performance_summary(),
                "health_status": self.get_health_status(),
                "export_timestamp": datetime.now().isoformat()
            }
    
    def clear_old_metrics(self, max_age_hours: int = 24):
        """Clear metrics older than specified age."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        with self._lock:
            # Clear old task metrics
            old_tasks = [tid for tid, metric in self.task_metrics.items() 
                        if metric.start_time < cutoff_time]
            for tid in old_tasks:
                del self.task_metrics[tid]
            
            self.logger.info(f"Cleared {len(old_tasks)} old task metrics")


class StructuredLogger:
    """Enhanced logging with structured output for better monitoring."""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log_task_start(self, task_id: str, agent_id: str, description: str):
        """Log task start with structured data."""
        self.logger.info(json.dumps({
            "event": "task_start",
            "task_id": task_id,
            "agent_id": agent_id,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_task_complete(self, task_id: str, agent_id: str, status: str, duration: float):
        """Log task completion with structured data."""
        self.logger.info(json.dumps({
            "event": "task_complete",
            "task_id": task_id,
            "agent_id": agent_id,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }))
    
    def log_agent_activity(self, agent_id: str, activity: str, details: Dict[str, Any] = None):
        """Log agent activity with structured data."""
        log_data = {
            "event": "agent_activity",
            "agent_id": agent_id,
            "activity": activity,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            log_data.update(details)
        
        self.logger.info(json.dumps(log_data))
    
    def log_error(self, error_type: str, message: str, context: Dict[str, Any] = None):
        """Log error with structured data."""
        log_data = {
            "event": "error",
            "error_type": error_type,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        if context:
            log_data.update(context)
        
        self.logger.error(json.dumps(log_data))
    
    def log_performance(self, metric_name: str, value: float, unit: str = ""):
        """Log performance metric."""
        self.logger.info(json.dumps({
            "event": "performance_metric",
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": datetime.now().isoformat()
        }))


# Global instances
metrics_collector = MetricsCollector()
structured_logger = StructuredLogger("agentic_coder", "agentic_coder.log")