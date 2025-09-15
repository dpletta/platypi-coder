"""
Agent Manager

Orchestrates multiple specialized agents and manages their collaboration.
"""

from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime
import uuid

from .base_agent import BaseAgent, AgentRole, AgentStatus, TaskContext, AgentMessage
from .planner_agent import PlannerAgent
from .coder_agent import CoderAgent
from .reviewer_agent import ReviewerAgent
from .debugger_agent import DebuggerAgent
from .tester_agent import TesterAgent


class AgentManager:
    """
    Manages a collection of specialized agents and orchestrates their collaboration.
    
    Responsibilities:
    - Agent lifecycle management
    - Task distribution and coordination
    - Inter-agent communication routing
    - Consensus building for complex tasks
    - Performance monitoring and optimization
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agents: Dict[str, BaseAgent] = {}
        self.message_router: Dict[str, List[str]] = {}  # recipient -> [senders]
        self.task_queue: List[TaskContext] = []
        self.active_tasks: Dict[str, TaskContext] = {}
        self.logger = logging.getLogger("agent_manager")
        self.consensus_threshold = self.config.get("consensus_threshold", 0.7)
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialized agents."""
        agent_configs = self.config.get("agents", {})
        
        # Create agents based on configuration
        agents_to_create = [
            (PlannerAgent, "planner", AgentRole.PLANNER),
            (CoderAgent, "coder", AgentRole.CODER),
            (ReviewerAgent, "reviewer", AgentRole.REVIEWER),
            (DebuggerAgent, "debugger", AgentRole.DEBUGGER),
            (TesterAgent, "tester", AgentRole.TESTER),
        ]
        
        for agent_class, agent_name, role in agents_to_create:
            agent_config = agent_configs.get(agent_name, {})
            agent = agent_class(f"{agent_name}_agent", role, agent_config)
            self.agents[agent.agent_id] = agent
            self.logger.info(f"Initialized {agent.agent_id}")
    
    async def submit_task(self, description: str, requirements: List[str] = None, 
                         constraints: List[str] = None, priority: int = 1) -> str:
        """Submit a new task to the agent ensemble."""
        task_id = str(uuid.uuid4())
        task = TaskContext(
            task_id=task_id,
            description=description,
            requirements=requirements or [],
            constraints=constraints or [],
            priority=priority
        )
        
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        
        self.logger.info(f"Submitted task {task_id}: {description}")
        
        # Start processing the task
        asyncio.create_task(self._process_task_queue())
        
        return task_id
    
    async def _process_task_queue(self):
        """Process tasks in the queue."""
        while self.task_queue:
            task = self.task_queue.pop(0)
            self.active_tasks[task.task_id] = task
            
            try:
                await self._execute_task(task)
            except Exception as e:
                self.logger.error(f"Error processing task {task.task_id}: {e}")
                await self._handle_task_failure(task, str(e))
    
    async def _execute_task(self, task: TaskContext):
        """Execute a task using the appropriate agent(s)."""
        self.logger.info(f"Executing task {task.task_id}: {task.description}")
        
        # Determine execution strategy based on task complexity
        if self._is_simple_task(task):
            await self._execute_simple_task(task)
        else:
            await self._execute_complex_task(task)
    
    def _is_simple_task(self, task: TaskContext) -> bool:
        """Determine if a task is simple enough for a single agent."""
        # Simple heuristics - can be made more sophisticated
        simple_keywords = ["read", "write", "list", "search", "replace"]
        return any(keyword in task.description.lower() for keyword in simple_keywords)
    
    async def _execute_simple_task(self, task: TaskContext):
        """Execute a simple task with a single appropriate agent."""
        # Find the best agent for this task
        best_agent = self._find_best_agent(task)
        
        if not best_agent:
            raise RuntimeError(f"No suitable agent found for task {task.task_id}")
        
        # Assign and execute
        await best_agent.assign_task(task)
        result = await best_agent.execute_task(task)
        await best_agent.complete_task(result)
        
        self.logger.info(f"Task {task.task_id} completed by {best_agent.agent_id}")
    
    async def _execute_complex_task(self, task: TaskContext):
        """Execute a complex task using multiple agents in collaboration."""
        self.logger.info(f"Executing complex task {task.task_id} with ensemble")
        
        # Step 1: Planning phase
        planner = self.agents.get("planner_agent")
        if planner:
            await planner.assign_task(task)
            plan_result = await planner.execute_task(task)
            await planner.complete_task(plan_result)
            
            # Extract sub-tasks from the plan
            sub_tasks = plan_result.get("sub_tasks", [])
            
            # Step 2: Execute sub-tasks in parallel where possible
            await self._execute_sub_tasks(sub_tasks, task.task_id)
            
            # Step 3: Review and consensus
            await self._perform_consensus_review(task.task_id)
    
    async def _execute_sub_tasks(self, sub_tasks: List[Dict], parent_task_id: str):
        """Execute sub-tasks in parallel where possible."""
        tasks_to_execute = []
        
        for sub_task_data in sub_tasks:
            sub_task = TaskContext(
                task_id=f"{parent_task_id}_{sub_task_data['id']}",
                description=sub_task_data["description"],
                requirements=sub_task_data.get("requirements", []),
                constraints=sub_task_data.get("constraints", []),
                priority=sub_task_data.get("priority", 1)
            )
            
            # Find appropriate agent
            agent = self._find_best_agent(sub_task)
            if agent:
                tasks_to_execute.append((agent, sub_task))
        
        # Execute tasks in parallel
        if tasks_to_execute:
            await asyncio.gather(*[
                self._execute_agent_task(agent, task) 
                for agent, task in tasks_to_execute
            ])
    
    async def _execute_agent_task(self, agent: BaseAgent, task: TaskContext):
        """Execute a task with a specific agent."""
        await agent.assign_task(task)
        result = await agent.execute_task(task)
        await agent.complete_task(result)
        return result
    
    async def _perform_consensus_review(self, task_id: str):
        """Perform consensus review for complex tasks."""
        reviewer = self.agents.get("reviewer_agent")
        if not reviewer:
            return
        
        # Create review task
        review_task = TaskContext(
            task_id=f"{task_id}_review",
            description=f"Review and validate results for task {task_id}",
            requirements=["comprehensive_review", "quality_assessment"],
            constraints=[]
        )
        
        await reviewer.assign_task(review_task)
        review_result = await reviewer.execute_task(review_task)
        await reviewer.complete_task(review_result)
        
        # If consensus is not reached, trigger additional collaboration
        if review_result.get("consensus_score", 0) < self.consensus_threshold:
            await self._trigger_collaboration(task_id, review_result)
    
    async def _trigger_collaboration(self, task_id: str, review_result: Dict[str, Any]):
        """Trigger additional collaboration when consensus is not reached."""
        self.logger.info(f"Triggering collaboration for task {task_id}")
        
        # Get all available agents
        available_agents = [agent for agent in self.agents.values() 
                          if agent.status == AgentStatus.IDLE]
        
        if len(available_agents) < 2:
            return
        
        # Create collaboration task
        collab_task = TaskContext(
            task_id=f"{task_id}_collaboration",
            description=f"Collaborative refinement for task {task_id}",
            requirements=["consensus_building", "solution_refinement"],
            constraints=[]
        )
        
        # Assign to multiple agents for collaborative work
        for agent in available_agents[:3]:  # Limit to 3 agents
            await agent.assign_task(collab_task)
            await agent.execute_task(collab_task)
            await agent.complete_task({})
    
    def _find_best_agent(self, task: TaskContext) -> Optional[BaseAgent]:
        """Find the best agent for a given task."""
        available_agents = [agent for agent in self.agents.values() 
                          if agent.status == AgentStatus.IDLE]
        
        if not available_agents:
            return None
        
        # Simple scoring based on capabilities and role
        best_agent = None
        best_score = -1
        
        for agent in available_agents:
            score = self._calculate_agent_score(agent, task)
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
    
    def _calculate_agent_score(self, agent: BaseAgent, task: TaskContext) -> float:
        """Calculate how well an agent matches a task."""
        score = 0.0
        
        # Role-based scoring
        role_scores = {
            AgentRole.PLANNER: 0.8 if "plan" in task.description.lower() else 0.2,
            AgentRole.CODER: 0.9 if any(word in task.description.lower() 
                                      for word in ["code", "implement", "write", "create"]) else 0.3,
            AgentRole.REVIEWER: 0.9 if any(word in task.description.lower() 
                                         for word in ["review", "check", "validate"]) else 0.2,
            AgentRole.DEBUGGER: 0.9 if any(word in task.description.lower() 
                                         for word in ["debug", "fix", "error"]) else 0.1,
            AgentRole.TESTER: 0.9 if any(word in task.description.lower() 
                                       for word in ["test", "verify", "validate"]) else 0.2,
        }
        
        score += role_scores.get(agent.role, 0.1)
        
        # Capability-based scoring
        task_words = set(task.description.lower().split())
        capability_words = set()
        for capability in agent.capabilities:
            capability_words.update(capability.lower().split())
        
        overlap = len(task_words.intersection(capability_words))
        score += overlap * 0.1
        
        return min(score, 1.0)
    
    async def _handle_task_failure(self, task: TaskContext, error: str):
        """Handle task execution failure."""
        self.logger.error(f"Task {task.task_id} failed: {error}")
        
        # Try to reassign to a different agent
        alternative_agent = self._find_best_agent(task)
        if alternative_agent and alternative_agent.agent_id != task.task_id:
            self.logger.info(f"Retrying task {task.task_id} with {alternative_agent.agent_id}")
            await self._execute_agent_task(alternative_agent, task)
        else:
            self.logger.error(f"Could not recover task {task.task_id}")
    
    async def get_ensemble_status(self) -> Dict[str, Any]:
        """Get status of all agents in the ensemble."""
        return {
            "total_agents": len(self.agents),
            "active_tasks": len(self.active_tasks),
            "queued_tasks": len(self.task_queue),
            "agents": {agent_id: agent.get_status() for agent_id, agent in self.agents.items()},
            "consensus_threshold": self.consensus_threshold
        }
    
    async def route_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Route messages between agents."""
        recipient = self.agents.get(message.recipient)
        if not recipient:
            self.logger.warning(f"Unknown recipient: {message.recipient}")
            return None
        
        return await recipient.process_message(message)