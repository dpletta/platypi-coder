"""
Base Agent Class

Defines the interface and common functionality for all specialized coding agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import json
from datetime import datetime


class AgentRole(Enum):
    """Defines the role of an agent in the ensemble."""
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"
    DEBUGGER = "debugger"
    TESTER = "tester"
    ORCHESTRATOR = "orchestrator"


class AgentStatus(Enum):
    """Current status of an agent."""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class AgentMessage:
    """Message structure for inter-agent communication."""
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None


@dataclass
class TaskContext:
    """Context information for a task being executed."""
    task_id: str
    description: str
    requirements: List[str]
    constraints: List[str]
    priority: int = 1
    deadline: Optional[datetime] = None
    metadata: Dict[str, Any] = None


class BaseAgent(ABC):
    """
    Base class for all specialized coding agents.
    
    Provides common functionality for:
    - Inter-agent communication
    - Task management
    - State tracking
    - Error handling
    """
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.role = role
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.current_task: Optional[TaskContext] = None
        self.message_queue: List[AgentMessage] = []
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.capabilities = self._define_capabilities()
        
    @abstractmethod
    def _define_capabilities(self) -> List[str]:
        """Define what this agent can do."""
        pass
    
    @abstractmethod
    async def execute_task(self, task: TaskContext) -> Dict[str, Any]:
        """Execute a specific task assigned to this agent."""
        pass
    
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process incoming messages from other agents."""
        self.logger.info(f"Received message from {message.sender}: {message.message_type}")
        
        # Default message handling - can be overridden by subclasses
        if message.message_type == "task_assignment":
            return await self._handle_task_assignment(message)
        elif message.message_type == "collaboration_request":
            return await self._handle_collaboration_request(message)
        elif message.message_type == "status_inquiry":
            return await self._handle_status_inquiry(message)
        
        return None
    
    async def _handle_task_assignment(self, message: AgentMessage) -> AgentMessage:
        """Handle task assignment messages."""
        task_data = message.content.get("task")
        if task_data:
            task = TaskContext(**task_data)
            await self.assign_task(task)
            
        return AgentMessage(
            sender=self.agent_id,
            recipient=message.sender,
            message_type="task_assignment_ack",
            content={"status": "accepted", "agent_id": self.agent_id},
            timestamp=datetime.now(),
            correlation_id=message.correlation_id
        )
    
    async def _handle_collaboration_request(self, message: AgentMessage) -> AgentMessage:
        """Handle collaboration requests from other agents."""
        # Default implementation - agents can override for specific behavior
        return AgentMessage(
            sender=self.agent_id,
            recipient=message.sender,
            message_type="collaboration_response",
            content={"available": self.status == AgentStatus.IDLE, "capabilities": self.capabilities},
            timestamp=datetime.now(),
            correlation_id=message.correlation_id
        )
    
    async def _handle_status_inquiry(self, message: AgentMessage) -> AgentMessage:
        """Handle status inquiry messages."""
        return AgentMessage(
            sender=self.agent_id,
            recipient=message.sender,
            message_type="status_response",
            content={
                "status": self.status.value,
                "current_task": self.current_task.task_id if self.current_task else None,
                "capabilities": self.capabilities
            },
            timestamp=datetime.now(),
            correlation_id=message.correlation_id
        )
    
    async def assign_task(self, task: TaskContext):
        """Assign a task to this agent."""
        if self.status != AgentStatus.IDLE:
            raise RuntimeError(f"Agent {self.agent_id} is not available for new tasks")
        
        self.current_task = task
        self.status = AgentStatus.WORKING
        self.logger.info(f"Assigned task {task.task_id}: {task.description}")
    
    async def complete_task(self, result: Dict[str, Any]):
        """Mark the current task as completed."""
        if not self.current_task:
            raise RuntimeError("No current task to complete")
        
        self.logger.info(f"Completed task {self.current_task.task_id}")
        self.current_task = None
        self.status = AgentStatus.IDLE
        
        return result
    
    async def send_message(self, recipient: str, message_type: str, content: Dict[str, Any], 
                          correlation_id: str = None) -> AgentMessage:
        """Send a message to another agent."""
        message = AgentMessage(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content,
            timestamp=datetime.now(),
            correlation_id=correlation_id
        )
        
        self.logger.info(f"Sending {message_type} to {recipient}")
        return message
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of this agent."""
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "status": self.status.value,
            "current_task": self.current_task.task_id if self.current_task else None,
            "capabilities": self.capabilities,
            "queue_length": len(self.message_queue)
        }
    
    async def handle_error(self, error: Exception, context: str = ""):
        """Handle errors that occur during task execution."""
        self.logger.error(f"Error in {context}: {str(error)}")
        self.status = AgentStatus.ERROR
        
        # Notify other agents about the error if needed
        error_message = {
            "error": str(error),
            "context": context,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return error_message