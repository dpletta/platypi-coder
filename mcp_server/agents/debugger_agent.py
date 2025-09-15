"""
Debugger Agent

Specialized agent for debugging, error analysis, and problem resolution.
"""

from typing import Dict, List, Any
import json
import logging
from datetime import datetime

from .base_agent import BaseAgent, AgentRole, TaskContext


class DebuggerAgent(BaseAgent):
    """
    Specialized agent for debugging and error resolution.
    
    Capabilities:
    - Error analysis and diagnosis
    - Root cause identification
    - Fix implementation
    - Testing and validation
    - Prevention strategies
    """
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any] = None):
        super().__init__(agent_id, role, config)
        self.debugging_strategies = self.config.get("debugging_strategies", [
            "systematic", "binary_search", "hypothesis_testing", "log_analysis"
        ])
        self.error_patterns = self.config.get("error_patterns", {
            "runtime": ["null_pointer", "index_out_of_bounds", "type_error"],
            "logic": ["infinite_loop", "off_by_one", "race_condition"],
            "performance": ["memory_leak", "slow_query", "inefficient_algorithm"]
        })
    
    def _define_capabilities(self) -> List[str]:
        return [
            "error_analysis",
            "root_cause_identification",
            "fix_implementation",
            "testing_validation",
            "prevention_strategies",
            "log_analysis",
            "performance_debugging",
            "systematic_debugging"
        ]
    
    async def execute_task(self, task: TaskContext) -> Dict[str, Any]:
        """Execute debugging task."""
        self.logger.info(f"Debugging task: {task.description}")
        
        try:
            # Analyze the debugging task
            analysis = await self._analyze_debug_task(task)
            
            # Perform systematic debugging
            debugging_result = await self._perform_debugging(task, analysis)
            
            # Implement fixes
            fix_result = await self._implement_fixes(task, debugging_result)
            
            # Validate fixes
            validation_result = await self._validate_fixes(task, fix_result)
            
            # Generate prevention strategies
            prevention_strategies = await self._generate_prevention_strategies(task, debugging_result)
            
            result = {
                "task_id": task.task_id,
                "analysis": analysis,
                "debugging_result": debugging_result,
                "fix_result": fix_result,
                "validation_result": validation_result,
                "prevention_strategies": prevention_strategies,
                "debugging_summary": self._generate_debugging_summary(debugging_result, fix_result),
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            await self.handle_error(e, f"debugging task {task.task_id}")
            raise
    
    async def _analyze_debug_task(self, task: TaskContext) -> Dict[str, Any]:
        """Analyze the debugging task to understand the problem."""
        description = task.description.lower()
        
        # Identify error type
        error_type = self._identify_error_type(description, task.requirements)
        
        # Determine debugging approach
        debugging_approach = self._determine_debugging_approach(error_type, task)
        
        # Estimate debugging effort
        effort_estimate = self._estimate_debugging_effort(task, error_type)
        
        # Identify symptoms and context
        symptoms = self._extract_symptoms(description, task.requirements)
        
        return {
            "error_type": error_type,
            "debugging_approach": debugging_approach,
            "effort_estimate": effort_estimate,
            "symptoms": symptoms,
            "severity": self._assess_severity(task),
            "urgency": self._assess_urgency(task)
        }
    
    def _identify_error_type(self, description: str, requirements: List[str]) -> str:
        """Identify the type of error based on description and requirements."""
        text = f"{description} {' '.join(requirements)}".lower()
        
        # Runtime errors
        if any(word in text for word in ["crash", "exception", "error", "fail"]):
            return "runtime_error"
        
        # Logic errors
        if any(word in text for word in ["wrong", "incorrect", "unexpected", "bug"]):
            return "logic_error"
        
        # Performance issues
        if any(word in text for word in ["slow", "performance", "timeout", "memory"]):
            return "performance_issue"
        
        # Integration issues
        if any(word in text for word in ["connection", "api", "service", "network"]):
            return "integration_issue"
        
        # Data issues
        if any(word in text for word in ["data", "database", "query", "corrupt"]):
            return "data_issue"
        
        return "unknown_error"
    
    def _determine_debugging_approach(self, error_type: str, task: TaskContext) -> str:
        """Determine the best debugging approach for the error type."""
        approach_mapping = {
            "runtime_error": "systematic",
            "logic_error": "hypothesis_testing",
            "performance_issue": "log_analysis",
            "integration_issue": "systematic",
            "data_issue": "binary_search",
            "unknown_error": "systematic"
        }
        
        return approach_mapping.get(error_type, "systematic")
    
    def _estimate_debugging_effort(self, task: TaskContext, error_type: str) -> Dict[str, Any]:
        """Estimate effort required for debugging."""
        base_effort = {
            "runtime_error": 60,      # 1 hour
            "logic_error": 120,       # 2 hours
            "performance_issue": 180, # 3 hours
            "integration_issue": 90,  # 1.5 hours
            "data_issue": 75,         # 1.25 hours
            "unknown_error": 150      # 2.5 hours
        }
        
        base_time = base_effort.get(error_type, 120)
        
        # Adjust based on complexity
        complexity_multiplier = 1 + (len(task.requirements) * 0.1)
        adjusted_time = base_time * complexity_multiplier
        
        return {
            "estimated_minutes": int(adjusted_time),
            "error_type": error_type,
            "complexity_multiplier": complexity_multiplier
        }
    
    def _extract_symptoms(self, description: str, requirements: List[str]) -> List[str]:
        """Extract symptoms and error indicators."""
        symptoms = []
        
        # Common symptom patterns
        symptom_patterns = {
            "crash": ["crash", "exception", "terminate", "abort"],
            "incorrect_output": ["wrong", "incorrect", "unexpected", "bad"],
            "performance": ["slow", "timeout", "hang", "freeze"],
            "memory": ["memory", "leak", "out of memory", "oom"],
            "network": ["connection", "timeout", "network", "unreachable"]
        }
        
        text = f"{description} {' '.join(requirements)}".lower()
        
        for symptom_type, patterns in symptom_patterns.items():
            if any(pattern in text for pattern in patterns):
                symptoms.append(symptom_type)
        
        return symptoms
    
    def _assess_severity(self, task: TaskContext) -> str:
        """Assess the severity of the debugging task."""
        description = task.description.lower()
        
        if any(word in description for word in ["critical", "crash", "data loss", "security"]):
            return "critical"
        elif any(word in description for word in ["major", "broken", "not working"]):
            return "high"
        elif any(word in description for word in ["minor", "issue", "problem"]):
            return "medium"
        else:
            return "low"
    
    def _assess_urgency(self, task: TaskContext) -> str:
        """Assess the urgency of the debugging task."""
        if task.priority >= 3:
            return "urgent"
        elif task.priority >= 2:
            return "high"
        else:
            return "normal"
    
    async def _perform_debugging(self, task: TaskContext, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Perform systematic debugging based on analysis."""
        error_type = analysis["error_type"]
        approach = analysis["debugging_approach"]
        
        debugging_steps = []
        hypotheses = []
        findings = []
        
        # Generate debugging steps based on approach
        if approach == "systematic":
            debugging_steps = await self._generate_systematic_steps(task, error_type)
        elif approach == "hypothesis_testing":
            hypotheses = await self._generate_hypotheses(task, error_type)
            debugging_steps = await self._generate_hypothesis_tests(hypotheses)
        elif approach == "log_analysis":
            debugging_steps = await self._generate_log_analysis_steps(task)
        elif approach == "binary_search":
            debugging_steps = await self._generate_binary_search_steps(task)
        
        # Simulate debugging findings
        findings = await self._simulate_debugging_findings(task, error_type)
        
        return {
            "approach": approach,
            "debugging_steps": debugging_steps,
            "hypotheses": hypotheses,
            "findings": findings,
            "root_cause": self._identify_root_cause(findings, error_type),
            "confidence_level": self._calculate_confidence_level(findings)
        }
    
    async def _generate_systematic_steps(self, task: TaskContext, error_type: str) -> List[Dict[str, Any]]:
        """Generate systematic debugging steps."""
        steps = [
            {
                "step": 1,
                "description": "Reproduce the error consistently",
                "action": "Run the code with the same inputs that caused the error",
                "expected_outcome": "Error reproduces reliably"
            },
            {
                "step": 2,
                "description": "Gather error information",
                "action": "Collect error messages, stack traces, and logs",
                "expected_outcome": "Complete error context available"
            },
            {
                "step": 3,
                "description": "Analyze error patterns",
                "action": "Look for patterns in when and how the error occurs",
                "expected_outcome": "Error pattern identified"
            },
            {
                "step": 4,
                "description": "Isolate the problem area",
                "action": "Narrow down the code section causing the issue",
                "expected_outcome": "Problem area identified"
            },
            {
                "step": 5,
                "description": "Test hypotheses",
                "action": "Test different theories about the root cause",
                "expected_outcome": "Root cause confirmed"
            }
        ]
        
        return steps
    
    async def _generate_hypotheses(self, task: TaskContext, error_type: str) -> List[Dict[str, Any]]:
        """Generate debugging hypotheses based on error type."""
        hypotheses = []
        
        if error_type == "runtime_error":
            hypotheses = [
                {
                    "hypothesis": "Null pointer dereference",
                    "probability": 0.3,
                    "test_method": "Check for null checks before object access"
                },
                {
                    "hypothesis": "Array index out of bounds",
                    "probability": 0.25,
                    "test_method": "Validate array indices"
                },
                {
                    "hypothesis": "Type conversion error",
                    "probability": 0.2,
                    "test_method": "Check data types and conversions"
                }
            ]
        elif error_type == "logic_error":
            hypotheses = [
                {
                    "hypothesis": "Off-by-one error in loops",
                    "probability": 0.4,
                    "test_method": "Review loop conditions and bounds"
                },
                {
                    "hypothesis": "Incorrect conditional logic",
                    "probability": 0.3,
                    "test_method": "Trace through conditional statements"
                },
                {
                    "hypothesis": "Wrong algorithm implementation",
                    "probability": 0.3,
                    "test_method": "Compare with expected algorithm"
                }
            ]
        elif error_type == "performance_issue":
            hypotheses = [
                {
                    "hypothesis": "Inefficient algorithm",
                    "probability": 0.4,
                    "test_method": "Profile algorithm complexity"
                },
                {
                    "hypothesis": "Memory leak",
                    "probability": 0.3,
                    "test_method": "Monitor memory usage over time"
                },
                {
                    "hypothesis": "Database query inefficiency",
                    "probability": 0.3,
                    "test_method": "Analyze query execution plans"
                }
            ]
        
        return hypotheses
    
    async def _generate_hypothesis_tests(self, hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate tests for debugging hypotheses."""
        steps = []
        
        for i, hypothesis in enumerate(hypotheses, 1):
            steps.append({
                "step": i,
                "description": f"Test hypothesis: {hypothesis['hypothesis']}",
                "action": hypothesis["test_method"],
                "expected_outcome": f"Confirm or reject hypothesis (probability: {hypothesis['probability']})"
            })
        
        return steps
    
    async def _generate_log_analysis_steps(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate log analysis debugging steps."""
        return [
            {
                "step": 1,
                "description": "Collect relevant logs",
                "action": "Gather application logs, system logs, and error logs",
                "expected_outcome": "Complete log set available"
            },
            {
                "step": 2,
                "description": "Parse and filter logs",
                "action": "Filter logs by timestamp, severity, and relevant components",
                "expected_outcome": "Relevant log entries identified"
            },
            {
                "step": 3,
                "description": "Analyze log patterns",
                "action": "Look for error patterns, timing issues, and correlations",
                "expected_outcome": "Log patterns identified"
            },
            {
                "step": 4,
                "description": "Correlate with code execution",
                "action": "Map log entries to code execution paths",
                "expected_outcome": "Code execution path identified"
            }
        ]
    
    async def _generate_binary_search_steps(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate binary search debugging steps."""
        return [
            {
                "step": 1,
                "description": "Identify search space",
                "action": "Define the range of code or data to search",
                "expected_outcome": "Search space defined"
            },
            {
                "step": 2,
                "description": "Divide search space",
                "action": "Split the search space in half",
                "expected_outcome": "Two equal halves created"
            },
            {
                "step": 3,
                "description": "Test each half",
                "action": "Test if the error occurs in each half",
                "expected_outcome": "Problematic half identified"
            },
            {
                "step": 4,
                "description": "Repeat with problematic half",
                "action": "Continue binary search with the problematic half",
                "expected_outcome": "Problem area narrowed down"
            }
        ]
    
    async def _simulate_debugging_findings(self, task: TaskContext, error_type: str) -> List[Dict[str, Any]]:
        """Simulate debugging findings based on error type."""
        findings = []
        
        if error_type == "runtime_error":
            findings = [
                {
                    "finding": "Null pointer exception in line 45",
                    "severity": "high",
                    "confidence": 0.9,
                    "evidence": "Stack trace shows null pointer at specific line"
                },
                {
                    "finding": "Missing null check before object access",
                    "severity": "medium",
                    "confidence": 0.8,
                    "evidence": "Code review shows missing validation"
                }
            ]
        elif error_type == "logic_error":
            findings = [
                {
                    "finding": "Off-by-one error in loop condition",
                    "severity": "medium",
                    "confidence": 0.85,
                    "evidence": "Loop iterates one time too many"
                },
                {
                    "finding": "Incorrect boundary condition",
                    "severity": "medium",
                    "confidence": 0.7,
                    "evidence": "Boundary check logic is wrong"
                }
            ]
        elif error_type == "performance_issue":
            findings = [
                {
                    "finding": "N+1 query problem in database access",
                    "severity": "high",
                    "confidence": 0.9,
                    "evidence": "Multiple database queries in loop"
                },
                {
                    "finding": "Inefficient algorithm with O(n²) complexity",
                    "severity": "medium",
                    "confidence": 0.8,
                    "evidence": "Nested loops causing performance degradation"
                }
            ]
        
        return findings
    
    def _identify_root_cause(self, findings: List[Dict[str, Any]], error_type: str) -> Dict[str, Any]:
        """Identify the root cause from findings."""
        if not findings:
            return {"cause": "unknown", "confidence": 0.0}
        
        # Find the finding with highest confidence and severity
        best_finding = max(findings, key=lambda f: f["confidence"])
        
        return {
            "cause": best_finding["finding"],
            "confidence": best_finding["confidence"],
            "severity": best_finding["severity"],
            "evidence": best_finding["evidence"]
        }
    
    def _calculate_confidence_level(self, findings: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence level in debugging results."""
        if not findings:
            return 0.0
        
        # Weight by confidence and severity
        weighted_sum = 0.0
        total_weight = 0.0
        
        severity_weights = {"high": 1.0, "medium": 0.7, "low": 0.4}
        
        for finding in findings:
            weight = severity_weights.get(finding["severity"], 0.5)
            weighted_sum += finding["confidence"] * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    async def _implement_fixes(self, task: TaskContext, debugging_result: Dict[str, Any]) -> Dict[str, Any]:
        """Implement fixes based on debugging results."""
        root_cause = debugging_result["root_cause"]
        findings = debugging_result["findings"]
        
        fixes = []
        
        for finding in findings:
            fix = await self._generate_fix_for_finding(finding, task)
            fixes.append(fix)
        
        return {
            "fixes": fixes,
            "implementation_plan": self._create_implementation_plan(fixes),
            "testing_requirements": self._define_testing_requirements(fixes)
        }
    
    async def _generate_fix_for_finding(self, finding: Dict[str, Any], task: TaskContext) -> Dict[str, Any]:
        """Generate a fix for a specific finding."""
        finding_type = finding["finding"].lower()
        
        if "null pointer" in finding_type:
            return {
                "type": "null_check",
                "description": "Add null pointer checks before object access",
                "code_changes": ["Add null validation", "Implement safe navigation"],
                "risk_level": "low",
                "estimated_effort": 30
            }
        elif "off-by-one" in finding_type:
            return {
                "type": "boundary_fix",
                "description": "Fix loop boundary conditions",
                "code_changes": ["Adjust loop conditions", "Review boundary logic"],
                "risk_level": "medium",
                "estimated_effort": 45
            }
        elif "query" in finding_type:
            return {
                "type": "query_optimization",
                "description": "Optimize database queries",
                "code_changes": ["Implement eager loading", "Add query caching"],
                "risk_level": "medium",
                "estimated_effort": 60
            }
        else:
            return {
                "type": "general_fix",
                "description": f"Fix {finding['finding']}",
                "code_changes": ["Review and fix identified issue"],
                "risk_level": "medium",
                "estimated_effort": 45
            }
    
    def _create_implementation_plan(self, fixes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create implementation plan for fixes."""
        plan = []
        
        # Sort fixes by risk level and effort
        sorted_fixes = sorted(fixes, key=lambda f: (f["risk_level"], f["estimated_effort"]))
        
        for i, fix in enumerate(sorted_fixes, 1):
            plan.append({
                "step": i,
                "fix": fix,
                "description": f"Implement {fix['description']}",
                "estimated_minutes": fix["estimated_effort"]
            })
        
        return plan
    
    def _define_testing_requirements(self, fixes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Define testing requirements for fixes."""
        return [
            {
                "test_type": "unit_test",
                "description": "Test individual fix components",
                "priority": "high"
            },
            {
                "test_type": "integration_test",
                "description": "Test fix integration with existing code",
                "priority": "high"
            },
            {
                "test_type": "regression_test",
                "description": "Ensure fix doesn't break existing functionality",
                "priority": "medium"
            },
            {
                "test_type": "performance_test",
                "description": "Verify performance improvements",
                "priority": "low"
            }
        ]
    
    async def _validate_fixes(self, task: TaskContext, fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that fixes resolve the original problem."""
        fixes = fix_result["fixes"]
        
        validation_results = []
        
        for fix in fixes:
            validation = {
                "fix_type": fix["type"],
                "validation_status": "pending",
                "test_results": [],
                "success_criteria": self._define_success_criteria(fix)
            }
            validation_results.append(validation)
        
        return {
            "validation_results": validation_results,
            "overall_status": "pending",
            "next_steps": ["Run tests", "Monitor in production", "Document changes"]
        }
    
    def _define_success_criteria(self, fix: Dict[str, Any]) -> List[str]:
        """Define success criteria for a fix."""
        fix_type = fix["type"]
        
        criteria_mapping = {
            "null_check": ["No null pointer exceptions", "Proper error handling"],
            "boundary_fix": ["Correct loop execution", "Proper boundary handling"],
            "query_optimization": ["Improved query performance", "Reduced database load"],
            "general_fix": ["Issue resolved", "No regression"]
        }
        
        return criteria_mapping.get(fix_type, ["Issue resolved"])
    
    async def _generate_prevention_strategies(self, task: TaskContext, 
                                            debugging_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategies to prevent similar issues in the future."""
        error_type = debugging_result.get("root_cause", {}).get("cause", "unknown")
        
        strategies = []
        
        if "null pointer" in error_type.lower():
            strategies.extend([
                {
                    "strategy": "defensive_programming",
                    "description": "Implement defensive programming practices",
                    "implementation": ["Add null checks", "Use optional types", "Implement safe navigation"]
                },
                {
                    "strategy": "static_analysis",
                    "description": "Use static analysis tools",
                    "implementation": ["Configure IDE warnings", "Add linting rules", "Use static analyzers"]
                }
            ])
        elif "off-by-one" in error_type.lower():
            strategies.extend([
                {
                    "strategy": "code_review",
                    "description": "Enhanced code review process",
                    "implementation": ["Review loop conditions", "Check boundary logic", "Use pair programming"]
                },
                {
                    "strategy": "testing",
                    "description": "Comprehensive boundary testing",
                    "implementation": ["Test edge cases", "Add boundary tests", "Use property-based testing"]
                }
            ])
        elif "performance" in error_type.lower():
            strategies.extend([
                {
                    "strategy": "performance_monitoring",
                    "description": "Implement performance monitoring",
                    "implementation": ["Add performance metrics", "Monitor query performance", "Set up alerts"]
                },
                {
                    "strategy": "code_standards",
                    "description": "Establish performance coding standards",
                    "implementation": ["Document performance guidelines", "Review algorithms", "Optimize early"]
                }
            ])
        
        # General prevention strategies
        strategies.extend([
            {
                "strategy": "error_logging",
                "description": "Improve error logging and monitoring",
                "implementation": ["Add comprehensive logging", "Set up error tracking", "Monitor application health"]
            },
            {
                "strategy": "testing_automation",
                "description": "Automate testing processes",
                "implementation": ["Add automated tests", "Implement CI/CD", "Use test coverage tools"]
            }
        ])
        
        return strategies
    
    def _generate_debugging_summary(self, debugging_result: Dict[str, Any], 
                                  fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the debugging process."""
        root_cause = debugging_result.get("root_cause", {})
        fixes = fix_result.get("fixes", [])
        
        return {
            "problem_identified": root_cause.get("cause", "Unknown"),
            "confidence_level": debugging_result.get("confidence_level", 0.0),
            "fixes_implemented": len(fixes),
            "total_effort": sum(fix.get("estimated_effort", 0) for fix in fixes),
            "risk_assessment": "low" if all(fix.get("risk_level") == "low" for fix in fixes) else "medium",
            "success_probability": min(root_cause.get("confidence", 0.0) + 0.2, 1.0)
        }