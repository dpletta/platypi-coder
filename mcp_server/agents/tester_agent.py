"""
Tester Agent

Specialized agent for testing, validation, and quality assurance.
"""

from typing import Dict, List, Any
import json
import logging
from datetime import datetime

from .base_agent import BaseAgent, AgentRole, TaskContext


class TesterAgent(BaseAgent):
    """
    Specialized agent for testing and quality assurance.
    
    Capabilities:
    - Test case generation
    - Test execution and validation
    - Coverage analysis
    - Performance testing
    - Integration testing
    """
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any] = None):
        super().__init__(agent_id, role, config)
        self.test_types = self.config.get("test_types", [
            "unit", "integration", "performance", "security", "usability"
        ])
        self.coverage_thresholds = self.config.get("coverage_thresholds", {
            "unit": 0.8,
            "integration": 0.6,
            "overall": 0.7
        })
        self.test_frameworks = self.config.get("test_frameworks", {
            "python": ["pytest", "unittest"],
            "javascript": ["jest", "mocha"],
            "java": ["junit", "testng"],
            "go": ["testing", "testify"]
        })
    
    def _define_capabilities(self) -> List[str]:
        return [
            "test_case_generation",
            "test_execution",
            "coverage_analysis",
            "performance_testing",
            "integration_testing",
            "security_testing",
            "test_automation",
            "quality_assurance"
        ]
    
    async def execute_task(self, task: TaskContext) -> Dict[str, Any]:
        """Execute testing task."""
        self.logger.info(f"Testing task: {task.description}")
        
        try:
            # Analyze the testing task
            analysis = await self._analyze_testing_task(task)
            
            # Generate test plan
            test_plan = await self._generate_test_plan(task, analysis)
            
            # Generate test cases
            test_cases = await self._generate_test_cases(task, test_plan)
            
            # Execute tests
            test_results = await self._execute_tests(task, test_cases)
            
            # Analyze results
            analysis_results = await self._analyze_test_results(test_results)
            
            # Generate recommendations
            recommendations = await self._generate_testing_recommendations(analysis_results)
            
            result = {
                "task_id": task.task_id,
                "analysis": analysis,
                "test_plan": test_plan,
                "test_cases": test_cases,
                "test_results": test_results,
                "analysis_results": analysis_results,
                "recommendations": recommendations,
                "testing_summary": self._generate_testing_summary(test_results, analysis_results),
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            await self.handle_error(e, f"testing task {task.task_id}")
            raise
    
    async def _analyze_testing_task(self, task: TaskContext) -> Dict[str, Any]:
        """Analyze the testing task to understand requirements."""
        description = task.description.lower()
        
        # Determine testing scope
        testing_scope = self._determine_testing_scope(description, task.requirements)
        
        # Identify test types needed
        test_types = self._identify_test_types(description, task.requirements)
        
        # Estimate testing effort
        effort_estimate = self._estimate_testing_effort(task, test_types)
        
        # Determine testing approach
        testing_approach = self._determine_testing_approach(test_types)
        
        return {
            "testing_scope": testing_scope,
            "test_types": test_types,
            "effort_estimate": effort_estimate,
            "testing_approach": testing_approach,
            "priority_level": self._determine_priority(task)
        }
    
    def _determine_testing_scope(self, description: str, requirements: List[str]) -> str:
        """Determine the scope of testing."""
        text = f"{description} {' '.join(requirements)}".lower()
        
        if any(word in text for word in ["comprehensive", "full", "complete", "thorough"]):
            return "comprehensive"
        elif any(word in text for word in ["smoke", "basic", "quick", "minimal"]):
            return "smoke"
        elif any(word in text for word in ["regression", "existing", "current"]):
            return "regression"
        elif any(word in text for word in ["new", "feature", "functionality"]):
            return "feature"
        else:
            return "standard"
    
    def _identify_test_types(self, description: str, requirements: List[str]) -> List[str]:
        """Identify which types of tests are needed."""
        test_types = []
        text = f"{description} {' '.join(requirements)}".lower()
        
        # Check for specific test type indicators
        type_indicators = {
            "unit": ["unit", "function", "method", "class"],
            "integration": ["integration", "api", "service", "database"],
            "performance": ["performance", "speed", "load", "stress"],
            "security": ["security", "vulnerability", "auth", "permission"],
            "usability": ["usability", "ui", "ux", "user", "interface"]
        }
        
        for test_type, indicators in type_indicators.items():
            if any(indicator in text for indicator in indicators):
                test_types.append(test_type)
        
        # Default to unit and integration if none specified
        if not test_types:
            test_types = ["unit", "integration"]
        
        return test_types
    
    def _estimate_testing_effort(self, task: TaskContext, test_types: List[str]) -> Dict[str, Any]:
        """Estimate effort required for testing."""
        base_effort_per_type = {
            "unit": 30,        # 30 minutes
            "integration": 60, # 1 hour
            "performance": 90, # 1.5 hours
            "security": 45,    # 45 minutes
            "usability": 75    # 1.25 hours
        }
        
        total_time = sum(base_effort_per_type.get(test_type, 30) for test_type in test_types)
        
        # Adjust based on complexity
        complexity_multiplier = 1 + (len(task.requirements) * 0.1)
        adjusted_time = total_time * complexity_multiplier
        
        return {
            "estimated_minutes": int(adjusted_time),
            "test_types_count": len(test_types),
            "complexity_multiplier": complexity_multiplier
        }
    
    def _determine_testing_approach(self, test_types: List[str]) -> str:
        """Determine the testing approach based on test types."""
        if "performance" in test_types and "security" in test_types:
            return "comprehensive"
        elif len(test_types) > 3:
            return "systematic"
        elif "unit" in test_types and "integration" in test_types:
            return "pyramid"
        else:
            return "focused"
    
    def _determine_priority(self, task: TaskContext) -> str:
        """Determine testing priority."""
        if task.priority >= 3:
            return "high"
        elif task.priority >= 2:
            return "medium"
        else:
            return "low"
    
    async def _generate_test_plan(self, task: TaskContext, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive test plan."""
        test_types = analysis["test_types"]
        testing_scope = analysis["testing_scope"]
        
        plan = {
            "testing_scope": testing_scope,
            "test_types": test_types,
            "phases": [],
            "test_environment": self._define_test_environment(task),
            "success_criteria": self._define_success_criteria(test_types),
            "risk_assessment": self._assess_testing_risks(task)
        }
        
        # Generate phases based on test types
        phases = []
        
        if "unit" in test_types:
            phases.append({
                "phase": "unit_testing",
                "description": "Test individual components in isolation",
                "estimated_duration": 30,
                "dependencies": []
            })
        
        if "integration" in test_types:
            phases.append({
                "phase": "integration_testing",
                "description": "Test component interactions",
                "estimated_duration": 60,
                "dependencies": ["unit_testing"]
            })
        
        if "performance" in test_types:
            phases.append({
                "phase": "performance_testing",
                "description": "Test performance characteristics",
                "estimated_duration": 90,
                "dependencies": ["integration_testing"]
            })
        
        if "security" in test_types:
            phases.append({
                "phase": "security_testing",
                "description": "Test security aspects",
                "estimated_duration": 45,
                "dependencies": ["integration_testing"]
            })
        
        plan["phases"] = phases
        
        return plan
    
    def _define_test_environment(self, task: TaskContext) -> Dict[str, Any]:
        """Define the test environment requirements."""
        return {
            "environment_type": "isolated",
            "data_requirements": ["test_data", "mock_data"],
            "infrastructure": ["test_database", "mock_services"],
            "tools": ["test_framework", "coverage_tool", "reporting_tool"]
        }
    
    def _define_success_criteria(self, test_types: List[str]) -> Dict[str, Any]:
        """Define success criteria for testing."""
        criteria = {
            "coverage_thresholds": {},
            "performance_requirements": {},
            "quality_gates": []
        }
        
        for test_type in test_types:
            if test_type in self.coverage_thresholds:
                criteria["coverage_thresholds"][test_type] = self.coverage_thresholds[test_type]
        
        criteria["quality_gates"] = [
            "All tests pass",
            "Coverage thresholds met",
            "No critical issues found",
            "Performance requirements satisfied"
        ]
        
        return criteria
    
    def _assess_testing_risks(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Assess risks associated with testing."""
        risks = []
        
        if len(task.requirements) > 5:
            risks.append({
                "risk": "requirement_complexity",
                "severity": "medium",
                "description": "Many requirements may complicate testing",
                "mitigation": "Prioritize requirements and focus on critical paths"
            })
        
        if any("performance" in req.lower() for req in task.requirements):
            risks.append({
                "risk": "performance_testing_complexity",
                "severity": "high",
                "description": "Performance testing may require specialized environment",
                "mitigation": "Use performance testing tools and realistic test data"
            })
        
        return risks
    
    async def _generate_test_cases(self, task: TaskContext, test_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test cases based on the test plan."""
        test_cases = []
        test_types = test_plan["test_types"]
        
        for test_type in test_types:
            cases = await self._generate_test_cases_for_type(test_type, task)
            test_cases.extend(cases)
        
        return test_cases
    
    async def _generate_test_cases_for_type(self, test_type: str, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate test cases for a specific test type."""
        if test_type == "unit":
            return await self._generate_unit_test_cases(task)
        elif test_type == "integration":
            return await self._generate_integration_test_cases(task)
        elif test_type == "performance":
            return await self._generate_performance_test_cases(task)
        elif test_type == "security":
            return await self._generate_security_test_cases(task)
        elif test_type == "usability":
            return await self._generate_usability_test_cases(task)
        else:
            return []
    
    async def _generate_unit_test_cases(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate unit test cases."""
        return [
            {
                "test_id": f"unit_{task.task_id}_001",
                "test_type": "unit",
                "description": "Test normal operation",
                "test_steps": [
                    "Setup test data",
                    "Execute function with valid inputs",
                    "Verify expected output",
                    "Check return values"
                ],
                "expected_result": "Function returns expected output",
                "priority": "high"
            },
            {
                "test_id": f"unit_{task.task_id}_002",
                "test_type": "unit",
                "description": "Test edge cases",
                "test_steps": [
                    "Setup edge case data",
                    "Execute function with edge inputs",
                    "Verify proper handling",
                    "Check error conditions"
                ],
                "expected_result": "Function handles edge cases correctly",
                "priority": "medium"
            },
            {
                "test_id": f"unit_{task.task_id}_003",
                "test_type": "unit",
                "description": "Test error conditions",
                "test_steps": [
                    "Setup invalid test data",
                    "Execute function with invalid inputs",
                    "Verify error handling",
                    "Check exception behavior"
                ],
                "expected_result": "Function handles errors appropriately",
                "priority": "high"
            }
        ]
    
    async def _generate_integration_test_cases(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate integration test cases."""
        return [
            {
                "test_id": f"integration_{task.task_id}_001",
                "test_type": "integration",
                "description": "Test component integration",
                "test_steps": [
                    "Setup integrated environment",
                    "Execute end-to-end workflow",
                    "Verify data flow between components",
                    "Check integration points"
                ],
                "expected_result": "Components integrate correctly",
                "priority": "high"
            },
            {
                "test_id": f"integration_{task.task_id}_002",
                "test_type": "integration",
                "description": "Test API integration",
                "test_steps": [
                    "Setup API test environment",
                    "Send API requests",
                    "Verify API responses",
                    "Check API contracts"
                ],
                "expected_result": "API integration works correctly",
                "priority": "high"
            }
        ]
    
    async def _generate_performance_test_cases(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate performance test cases."""
        return [
            {
                "test_id": f"performance_{task.task_id}_001",
                "test_type": "performance",
                "description": "Test response time",
                "test_steps": [
                    "Setup performance test environment",
                    "Execute operations with timing",
                    "Measure response times",
                    "Compare against benchmarks"
                ],
                "expected_result": "Response time within acceptable limits",
                "priority": "medium"
            },
            {
                "test_id": f"performance_{task.task_id}_002",
                "test_type": "performance",
                "description": "Test load handling",
                "test_steps": [
                    "Setup load test environment",
                    "Simulate concurrent users",
                    "Monitor system performance",
                    "Check for bottlenecks"
                ],
                "expected_result": "System handles expected load",
                "priority": "medium"
            }
        ]
    
    async def _generate_security_test_cases(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate security test cases."""
        return [
            {
                "test_id": f"security_{task.task_id}_001",
                "test_type": "security",
                "description": "Test input validation",
                "test_steps": [
                    "Setup security test environment",
                    "Send malicious inputs",
                    "Verify input sanitization",
                    "Check for vulnerabilities"
                ],
                "expected_result": "Input validation prevents attacks",
                "priority": "high"
            },
            {
                "test_id": f"security_{task.task_id}_002",
                "test_type": "security",
                "description": "Test authentication",
                "test_steps": [
                    "Test authentication mechanisms",
                    "Verify authorization checks",
                    "Test session management",
                    "Check access controls"
                ],
                "expected_result": "Authentication and authorization work correctly",
                "priority": "high"
            }
        ]
    
    async def _generate_usability_test_cases(self, task: TaskContext) -> List[Dict[str, Any]]:
        """Generate usability test cases."""
        return [
            {
                "test_id": f"usability_{task.task_id}_001",
                "test_type": "usability",
                "description": "Test user interface",
                "test_steps": [
                    "Setup UI test environment",
                    "Navigate through interface",
                    "Test user interactions",
                    "Verify usability standards"
                ],
                "expected_result": "Interface is user-friendly",
                "priority": "medium"
            }
        ]
    
    async def _execute_tests(self, task: TaskContext, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute the generated test cases."""
        # This is a mock implementation - in a real scenario, this would
        # actually execute the tests and collect results
        
        execution_results = {
            "test_execution_summary": {
                "total_tests": len(test_cases),
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "execution_time": 0
            },
            "test_results": [],
            "coverage_report": {},
            "performance_metrics": {}
        }
        
        # Simulate test execution results
        for test_case in test_cases:
            result = await self._simulate_test_execution(test_case)
            execution_results["test_results"].append(result)
            
            if result["status"] == "passed":
                execution_results["test_execution_summary"]["passed"] += 1
            elif result["status"] == "failed":
                execution_results["test_execution_summary"]["failed"] += 1
            else:
                execution_results["test_execution_summary"]["skipped"] += 1
        
        # Generate mock coverage report
        execution_results["coverage_report"] = await self._generate_coverage_report(test_cases)
        
        # Generate mock performance metrics
        execution_results["performance_metrics"] = await self._generate_performance_metrics(test_cases)
        
        return execution_results
    
    async def _simulate_test_execution(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate execution of a single test case."""
        # Mock test execution - in reality this would run actual tests
        import random
        
        # Simulate test outcome based on test type and priority
        test_type = test_case["test_type"]
        priority = test_case["priority"]
        
        # Higher priority tests are more likely to pass
        pass_probability = {
            "high": 0.9,
            "medium": 0.8,
            "low": 0.7
        }.get(priority, 0.8)
        
        status = "passed" if random.random() < pass_probability else "failed"
        
        return {
            "test_id": test_case["test_id"],
            "status": status,
            "execution_time": random.randint(1, 30),  # seconds
            "error_message": None if status == "passed" else "Mock test failure",
            "coverage": random.uniform(0.6, 1.0),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_coverage_report(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate coverage report."""
        test_types = list(set(test_case["test_type"] for test_case in test_cases))
        
        coverage_report = {
            "overall_coverage": 0.0,
            "coverage_by_type": {},
            "coverage_details": {}
        }
        
        total_coverage = 0.0
        
        for test_type in test_types:
            type_cases = [tc for tc in test_cases if tc["test_type"] == test_type]
            type_coverage = sum(random.uniform(0.6, 1.0) for _ in type_cases) / len(type_cases)
            coverage_report["coverage_by_type"][test_type] = type_coverage
            total_coverage += type_coverage
        
        coverage_report["overall_coverage"] = total_coverage / len(test_types)
        
        return coverage_report
    
    async def _generate_performance_metrics(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate performance metrics."""
        performance_cases = [tc for tc in test_cases if tc["test_type"] == "performance"]
        
        if not performance_cases:
            return {}
        
        return {
            "average_response_time": random.uniform(100, 500),  # milliseconds
            "throughput": random.uniform(100, 1000),  # requests per second
            "memory_usage": random.uniform(50, 200),  # MB
            "cpu_usage": random.uniform(20, 80),  # percentage
            "error_rate": random.uniform(0, 0.05)  # percentage
        }
    
    async def _analyze_test_results(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test execution results."""
        summary = test_results["test_execution_summary"]
        coverage_report = test_results["coverage_report"]
        performance_metrics = test_results["performance_metrics"]
        
        analysis = {
            "overall_status": "passed" if summary["failed"] == 0 else "failed",
            "quality_metrics": {
                "test_pass_rate": summary["passed"] / summary["total_tests"] if summary["total_tests"] > 0 else 0,
                "coverage_score": coverage_report.get("overall_coverage", 0),
                "performance_score": self._calculate_performance_score(performance_metrics)
            },
            "issues_found": [],
            "recommendations": []
        }
        
        # Identify issues
        if summary["failed"] > 0:
            analysis["issues_found"].append({
                "type": "test_failures",
                "count": summary["failed"],
                "severity": "high"
            })
        
        if coverage_report.get("overall_coverage", 0) < 0.7:
            analysis["issues_found"].append({
                "type": "low_coverage",
                "coverage": coverage_report["overall_coverage"],
                "severity": "medium"
            })
        
        if performance_metrics and performance_metrics.get("error_rate", 0) > 0.01:
            analysis["issues_found"].append({
                "type": "performance_issues",
                "error_rate": performance_metrics["error_rate"],
                "severity": "high"
            })
        
        return analysis
    
    def _calculate_performance_score(self, performance_metrics: Dict[str, Any]) -> float:
        """Calculate overall performance score."""
        if not performance_metrics:
            return 0.0
        
        # Simple scoring based on key metrics
        response_time_score = max(0, 1 - (performance_metrics.get("average_response_time", 1000) - 100) / 900)
        error_rate_score = max(0, 1 - performance_metrics.get("error_rate", 0) * 20)
        
        return (response_time_score + error_rate_score) / 2
    
    async def _generate_testing_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on test analysis."""
        recommendations = []
        
        quality_metrics = analysis_results["quality_metrics"]
        issues_found = analysis_results["issues_found"]
        
        # Coverage recommendations
        if quality_metrics["coverage_score"] < 0.7:
            recommendations.append({
                "category": "coverage",
                "recommendation": "Increase test coverage to meet quality standards",
                "priority": "medium",
                "action": "Add more test cases for uncovered code paths"
            })
        
        # Performance recommendations
        if quality_metrics["performance_score"] < 0.8:
            recommendations.append({
                "category": "performance",
                "recommendation": "Optimize performance based on test results",
                "priority": "high",
                "action": "Review and optimize slow operations"
            })
        
        # Test quality recommendations
        if quality_metrics["test_pass_rate"] < 0.9:
            recommendations.append({
                "category": "test_quality",
                "recommendation": "Improve test reliability and fix failing tests",
                "priority": "high",
                "action": "Investigate and fix test failures"
            })
        
        # General recommendations
        recommendations.extend([
            {
                "category": "automation",
                "recommendation": "Automate test execution in CI/CD pipeline",
                "priority": "medium",
                "action": "Set up automated testing workflow"
            },
            {
                "category": "monitoring",
                "recommendation": "Implement continuous test monitoring",
                "priority": "low",
                "action": "Add test result monitoring and alerting"
            }
        ])
        
        return recommendations
    
    def _generate_testing_summary(self, test_results: Dict[str, Any], 
                                analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the testing process."""
        summary = test_results["test_execution_summary"]
        quality_metrics = analysis_results["quality_metrics"]
        
        return {
            "total_tests_executed": summary["total_tests"],
            "success_rate": quality_metrics["test_pass_rate"],
            "coverage_achieved": quality_metrics["coverage_score"],
            "performance_score": quality_metrics["performance_score"],
            "overall_quality": "good" if quality_metrics["test_pass_rate"] > 0.9 and quality_metrics["coverage_score"] > 0.7 else "needs_improvement",
            "critical_issues": len([issue for issue in analysis_results["issues_found"] if issue["severity"] == "high"]),
            "recommendations_count": len(analysis_results["recommendations"])
        }