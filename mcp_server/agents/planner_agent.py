"""
Planner Agent

Specialized agent for breaking down complex tasks into actionable plans.
"""

from typing import Dict, List, Any
import json
import logging
from datetime import datetime

from .base_agent import BaseAgent, AgentRole, TaskContext


class PlannerAgent(BaseAgent):
    """
    Specialized agent for task planning and decomposition.
    
    Capabilities:
    - Task analysis and decomposition
    - Dependency identification
    - Resource estimation
    - Timeline planning
    - Risk assessment
    """
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any] = None):
        super().__init__(agent_id, role, config)
        self.planning_strategies = self.config.get("planning_strategies", [
            "sequential", "parallel", "iterative", "agile"
        ])
        self.max_subtasks = self.config.get("max_subtasks", 10)
    
    def _define_capabilities(self) -> List[str]:
        return [
            "task_decomposition",
            "dependency_analysis", 
            "resource_estimation",
            "timeline_planning",
            "risk_assessment",
            "strategy_selection",
            "workflow_design"
        ]
    
    async def execute_task(self, task: TaskContext) -> Dict[str, Any]:
        """Execute planning task."""
        self.logger.info(f"Planning task: {task.description}")
        
        try:
            # Analyze the task
            analysis = await self._analyze_task(task)
            
            # Generate plan
            plan = await self._generate_plan(task, analysis)
            
            # Validate plan
            validation = await self._validate_plan(plan)
            
            result = {
                "task_id": task.task_id,
                "analysis": analysis,
                "plan": plan,
                "validation": validation,
                "sub_tasks": plan.get("sub_tasks", []),
                "estimated_duration": plan.get("estimated_duration"),
                "complexity_score": analysis.get("complexity_score"),
                "strategy": plan.get("strategy"),
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            await self.handle_error(e, f"planning task {task.task_id}")
            raise
    
    async def _analyze_task(self, task: TaskContext) -> Dict[str, Any]:
        """Analyze the task to understand its complexity and requirements."""
        description = task.description.lower()
        
        # Complexity analysis
        complexity_indicators = {
            "simple": ["read", "write", "list", "search", "replace"],
            "moderate": ["implement", "create", "modify", "update", "refactor"],
            "complex": ["design", "architecture", "system", "integration", "migration"],
            "very_complex": ["rewrite", "redesign", "optimize", "scale", "performance"]
        }
        
        complexity_score = 0.1
        complexity_level = "simple"
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in description for indicator in indicators):
                complexity_score = {
                    "simple": 0.2,
                    "moderate": 0.5,
                    "complex": 0.8,
                    "very_complex": 1.0
                }[level]
                complexity_level = level
                break
        
        # Requirement analysis
        requirements_analysis = {
            "functional": len([r for r in task.requirements if "function" in r.lower()]),
            "non_functional": len([r for r in task.requirements if any(nf in r.lower() 
                                    for nf in ["performance", "security", "scalability"])]),
            "technical": len([r for r in task.requirements if any(tech in r.lower() 
                                   for tech in ["api", "database", "framework", "library"])])
        }
        
        # Constraint analysis
        constraint_impact = {
            "time": 0.3 if any("time" in c.lower() for c in task.constraints) else 0,
            "resource": 0.2 if any("resource" in c.lower() for c in task.constraints) else 0,
            "compatibility": 0.1 if any("compat" in c.lower() for c in task.constraints) else 0
        }
        
        return {
            "complexity_score": complexity_score,
            "complexity_level": complexity_level,
            "requirements_analysis": requirements_analysis,
            "constraint_impact": constraint_impact,
            "estimated_effort": self._estimate_effort(complexity_score, len(task.requirements))
        }
    
    async def _generate_plan(self, task: TaskContext, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed execution plan."""
        complexity_score = analysis["complexity_score"]
        
        # Select planning strategy
        strategy = self._select_strategy(complexity_score, task)
        
        # Generate sub-tasks
        sub_tasks = await self._generate_subtasks(task, analysis, strategy)
        
        # Estimate timeline
        timeline = self._estimate_timeline(sub_tasks, complexity_score)
        
        # Identify dependencies
        dependencies = self._identify_dependencies(sub_tasks)
        
        return {
            "strategy": strategy,
            "sub_tasks": sub_tasks,
            "timeline": timeline,
            "dependencies": dependencies,
            "estimated_duration": timeline.get("total_duration"),
            "parallel_execution": strategy in ["parallel", "agile"],
            "risk_factors": self._assess_risks(task, analysis)
        }
    
    def _select_strategy(self, complexity_score: float, task: TaskContext) -> str:
        """Select the best planning strategy for the task."""
        if complexity_score < 0.3:
            return "sequential"
        elif complexity_score < 0.6:
            return "parallel"
        elif complexity_score < 0.8:
            return "iterative"
        else:
            return "agile"
    
    async def _generate_subtasks(self, task: TaskContext, analysis: Dict[str, Any], 
                               strategy: str) -> List[Dict[str, Any]]:
        """Generate sub-tasks based on the task analysis."""
        sub_tasks = []
        description = task.description.lower()
        
        # Common sub-task patterns
        if "implement" in description or "create" in description:
            sub_tasks.extend([
                {
                    "id": "analysis",
                    "description": "Analyze requirements and design approach",
                    "type": "analysis",
                    "priority": 1,
                    "estimated_duration": 30,
                    "dependencies": []
                },
                {
                    "id": "design",
                    "description": "Design the solution architecture",
                    "type": "design", 
                    "priority": 2,
                    "estimated_duration": 45,
                    "dependencies": ["analysis"]
                },
                {
                    "id": "implementation",
                    "description": "Implement the core functionality",
                    "type": "implementation",
                    "priority": 3,
                    "estimated_duration": 120,
                    "dependencies": ["design"]
                },
                {
                    "id": "testing",
                    "description": "Test the implementation",
                    "type": "testing",
                    "priority": 4,
                    "estimated_duration": 60,
                    "dependencies": ["implementation"]
                }
            ])
        
        elif "debug" in description or "fix" in description:
            sub_tasks.extend([
                {
                    "id": "reproduce",
                    "description": "Reproduce the issue",
                    "type": "analysis",
                    "priority": 1,
                    "estimated_duration": 20,
                    "dependencies": []
                },
                {
                    "id": "investigate",
                    "description": "Investigate root cause",
                    "type": "analysis",
                    "priority": 2,
                    "estimated_duration": 40,
                    "dependencies": ["reproduce"]
                },
                {
                    "id": "fix",
                    "description": "Implement the fix",
                    "type": "implementation",
                    "priority": 3,
                    "estimated_duration": 60,
                    "dependencies": ["investigate"]
                },
                {
                    "id": "verify",
                    "description": "Verify the fix works",
                    "type": "testing",
                    "priority": 4,
                    "estimated_duration": 30,
                    "dependencies": ["fix"]
                }
            ])
        
        elif "review" in description or "check" in description:
            sub_tasks.extend([
                {
                    "id": "code_review",
                    "description": "Review code quality and standards",
                    "type": "review",
                    "priority": 1,
                    "estimated_duration": 45,
                    "dependencies": []
                },
                {
                    "id": "security_check",
                    "description": "Check for security vulnerabilities",
                    "type": "review",
                    "priority": 2,
                    "estimated_duration": 30,
                    "dependencies": []
                },
                {
                    "id": "performance_check",
                    "description": "Check performance implications",
                    "type": "review",
                    "priority": 3,
                    "estimated_duration": 25,
                    "dependencies": []
                }
            ])
        
        else:
            # Generic sub-tasks for unknown task types
            sub_tasks.append({
                "id": "execute",
                "description": task.description,
                "type": "execution",
                "priority": 1,
                "estimated_duration": 60,
                "dependencies": []
            })
        
        # Limit number of sub-tasks
        return sub_tasks[:self.max_subtasks]
    
    def _estimate_timeline(self, sub_tasks: List[Dict[str, Any]], 
                          complexity_score: float) -> Dict[str, Any]:
        """Estimate timeline for the plan."""
        total_duration = sum(task.get("estimated_duration", 30) for task in sub_tasks)
        
        # Apply complexity multiplier
        complexity_multiplier = 1 + complexity_score
        adjusted_duration = total_duration * complexity_multiplier
        
        # Calculate parallel execution time
        parallel_duration = self._calculate_parallel_duration(sub_tasks)
        
        return {
            "total_duration": int(adjusted_duration),
            "parallel_duration": int(parallel_duration),
            "sequential_duration": int(adjusted_duration),
            "complexity_multiplier": complexity_multiplier
        }
    
    def _calculate_parallel_duration(self, sub_tasks: List[Dict[str, Any]]) -> float:
        """Calculate duration assuming parallel execution where possible."""
        # Simple heuristic - tasks without dependencies can run in parallel
        independent_tasks = [task for task in sub_tasks if not task.get("dependencies")]
        dependent_tasks = [task for task in sub_tasks if task.get("dependencies")]
        
        # Independent tasks can run in parallel
        parallel_time = max(task.get("estimated_duration", 30) for task in independent_tasks) if independent_tasks else 0
        
        # Dependent tasks must run sequentially
        sequential_time = sum(task.get("estimated_duration", 30) for task in dependent_tasks)
        
        return parallel_time + sequential_time
    
    def _identify_dependencies(self, sub_tasks: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Identify dependencies between sub-tasks."""
        dependencies = {}
        for task in sub_tasks:
            task_id = task["id"]
            task_deps = task.get("dependencies", [])
            dependencies[task_id] = task_deps
        return dependencies
    
    def _assess_risks(self, task: TaskContext, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess potential risks for the task."""
        risks = []
        
        complexity_score = analysis["complexity_score"]
        if complexity_score > 0.7:
            risks.append({
                "type": "high_complexity",
                "severity": "medium",
                "description": "High complexity may lead to implementation challenges",
                "mitigation": "Break down into smaller, manageable pieces"
            })
        
        if len(task.constraints) > 3:
            risks.append({
                "type": "constraint_overload",
                "severity": "low",
                "description": "Many constraints may limit solution options",
                "mitigation": "Prioritize constraints and identify trade-offs"
            })
        
        if any("time" in c.lower() for c in task.constraints):
            risks.append({
                "type": "time_pressure",
                "severity": "high",
                "description": "Time constraints may affect quality",
                "mitigation": "Focus on essential features first"
            })
        
        return risks
    
    def _estimate_effort(self, complexity_score: float, requirement_count: int) -> str:
        """Estimate effort level."""
        effort_score = complexity_score + (requirement_count * 0.1)
        
        if effort_score < 0.3:
            return "low"
        elif effort_score < 0.6:
            return "medium"
        elif effort_score < 0.8:
            return "high"
        else:
            return "very_high"
    
    async def _validate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated plan."""
        validation_results = {
            "is_valid": True,
            "warnings": [],
            "recommendations": []
        }
        
        sub_tasks = plan.get("sub_tasks", [])
        
        # Check if plan has sub-tasks
        if not sub_tasks:
            validation_results["is_valid"] = False
            validation_results["warnings"].append("Plan has no sub-tasks")
        
        # Check for circular dependencies
        if self._has_circular_dependencies(sub_tasks):
            validation_results["is_valid"] = False
            validation_results["warnings"].append("Circular dependencies detected")
        
        # Check timeline reasonableness
        total_duration = plan.get("estimated_duration", 0)
        if total_duration > 480:  # More than 8 hours
            validation_results["recommendations"].append(
                "Consider breaking down into smaller tasks"
            )
        
        return validation_results
    
    def _has_circular_dependencies(self, sub_tasks: List[Dict[str, Any]]) -> bool:
        """Check for circular dependencies in sub-tasks."""
        # Simple cycle detection - can be enhanced
        for task in sub_tasks:
            task_id = task["id"]
            dependencies = task.get("dependencies", [])
            
            # Check if any dependency depends on this task
            for dep_id in dependencies:
                dep_task = next((t for t in sub_tasks if t["id"] == dep_id), None)
                if dep_task and task_id in dep_task.get("dependencies", []):
                    return True
        
        return False