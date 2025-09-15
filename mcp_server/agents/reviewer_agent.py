"""
Reviewer Agent

Specialized agent for code review, quality assessment, and validation.
"""

from typing import Dict, List, Any
import json
import logging
from datetime import datetime

from .base_agent import BaseAgent, AgentRole, TaskContext


class ReviewerAgent(BaseAgent):
    """
    Specialized agent for code review and quality assessment.
    
    Capabilities:
    - Code quality analysis
    - Security vulnerability detection
    - Performance assessment
    - Best practices validation
    - Documentation review
    """
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any] = None):
        super().__init__(agent_id, role, config)
        self.quality_thresholds = self.config.get("quality_thresholds", {
            "complexity": 10,
            "maintainability": 0.7,
            "test_coverage": 0.8,
            "security_score": 0.9
        })
        self.review_categories = self.config.get("review_categories", [
            "code_quality", "security", "performance", "maintainability", "documentation"
        ])
    
    def _define_capabilities(self) -> List[str]:
        return [
            "code_quality_analysis",
            "security_assessment",
            "performance_review",
            "best_practices_validation",
            "documentation_review",
            "vulnerability_detection",
            "consensus_building",
            "quality_scoring"
        ]
    
    async def execute_task(self, task: TaskContext) -> Dict[str, Any]:
        """Execute review task."""
        self.logger.info(f"Review task: {task.description}")
        
        try:
            # Analyze the review requirements
            analysis = await self._analyze_review_task(task)
            
            # Perform comprehensive review
            review_results = await self._perform_review(task, analysis)
            
            # Calculate consensus score
            consensus_score = await self._calculate_consensus_score(review_results)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(review_results)
            
            result = {
                "task_id": task.task_id,
                "analysis": analysis,
                "review_results": review_results,
                "consensus_score": consensus_score,
                "recommendations": recommendations,
                "quality_summary": self._generate_quality_summary(review_results),
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            await self.handle_error(e, f"review task {task.task_id}")
            raise
    
    async def _analyze_review_task(self, task: TaskContext) -> Dict[str, Any]:
        """Analyze the review task to understand scope and requirements."""
        description = task.description.lower()
        
        # Determine review scope
        review_scope = self._determine_review_scope(description)
        
        # Identify review categories
        categories = self._identify_review_categories(description, task.requirements)
        
        # Estimate review effort
        effort_estimate = self._estimate_review_effort(task, categories)
        
        return {
            "review_scope": review_scope,
            "categories": categories,
            "effort_estimate": effort_estimate,
            "priority_level": self._determine_priority(task)
        }
    
    def _determine_review_scope(self, description: str) -> str:
        """Determine the scope of the review."""
        if any(word in description for word in ["comprehensive", "full", "complete"]):
            return "comprehensive"
        elif any(word in description for word in ["security", "vulnerability", "safe"]):
            return "security_focused"
        elif any(word in description for word in ["performance", "optimization", "speed"]):
            return "performance_focused"
        elif any(word in description for word in ["quality", "standards", "best"]):
            return "quality_focused"
        else:
            return "general"
    
    def _identify_review_categories(self, description: str, requirements: List[str]) -> List[str]:
        """Identify which categories to review."""
        categories = []
        
        # Check description for category indicators
        category_indicators = {
            "code_quality": ["quality", "standards", "style", "format"],
            "security": ["security", "vulnerability", "safe", "secure"],
            "performance": ["performance", "optimization", "speed", "efficiency"],
            "maintainability": ["maintain", "readable", "clean", "refactor"],
            "documentation": ["document", "comment", "readme", "api"]
        }
        
        text = f"{description} {' '.join(requirements)}".lower()
        
        for category, indicators in category_indicators.items():
            if any(indicator in text for indicator in indicators):
                categories.append(category)
        
        # Default to general categories if none specified
        if not categories:
            categories = ["code_quality", "maintainability"]
        
        return categories
    
    def _estimate_review_effort(self, task: TaskContext, categories: List[str]) -> Dict[str, Any]:
        """Estimate effort required for review."""
        base_time_per_category = 15  # minutes
        total_time = len(categories) * base_time_per_category
        
        # Adjust based on complexity
        complexity_multiplier = 1 + (len(task.requirements) * 0.1)
        adjusted_time = total_time * complexity_multiplier
        
        return {
            "estimated_minutes": int(adjusted_time),
            "categories_count": len(categories),
            "complexity_multiplier": complexity_multiplier
        }
    
    def _determine_priority(self, task: TaskContext) -> str:
        """Determine review priority."""
        if task.priority >= 3:
            return "high"
        elif task.priority >= 2:
            return "medium"
        else:
            return "low"
    
    async def _perform_review(self, task: TaskContext, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual review based on analysis."""
        categories = analysis["categories"]
        review_results = {}
        
        for category in categories:
            review_results[category] = await self._review_category(category, task)
        
        return review_results
    
    async def _review_category(self, category: str, task: TaskContext) -> Dict[str, Any]:
        """Review a specific category."""
        if category == "code_quality":
            return await self._review_code_quality(task)
        elif category == "security":
            return await self._review_security(task)
        elif category == "performance":
            return await self._review_performance(task)
        elif category == "maintainability":
            return await self._review_maintainability(task)
        elif category == "documentation":
            return await self._review_documentation(task)
        else:
            return {"status": "not_applicable", "score": 0.0}
    
    async def _review_code_quality(self, task: TaskContext) -> Dict[str, Any]:
        """Review code quality aspects."""
        # Mock quality analysis
        quality_issues = []
        quality_score = 0.8
        
        # Check for common quality issues
        description = task.description.lower()
        
        if "complex" in description:
            quality_issues.append({
                "type": "complexity",
                "severity": "medium",
                "description": "Code complexity may be high",
                "recommendation": "Consider breaking down into smaller functions"
            })
            quality_score -= 0.1
        
        if len(task.requirements) > 5:
            quality_issues.append({
                "type": "requirement_overload",
                "severity": "low",
                "description": "Many requirements may affect code clarity",
                "recommendation": "Prioritize requirements and document trade-offs"
            })
            quality_score -= 0.05
        
        return {
            "score": max(quality_score, 0.0),
            "issues": quality_issues,
            "recommendations": [
                "Follow coding standards and best practices",
                "Ensure proper error handling",
                "Add comprehensive comments"
            ],
            "metrics": {
                "cyclomatic_complexity": 5.2,
                "lines_of_code": 150,
                "comment_density": 0.3
            }
        }
    
    async def _review_security(self, task: TaskContext) -> Dict[str, Any]:
        """Review security aspects."""
        security_issues = []
        security_score = 0.9
        
        # Check for security-related requirements
        security_keywords = ["input", "validation", "authentication", "authorization", "encryption"]
        has_security_requirements = any(keyword in req.lower() 
                                      for req in task.requirements 
                                      for keyword in security_keywords)
        
        if not has_security_requirements and any(word in task.description.lower() 
                                                for word in ["api", "user", "data"]):
            security_issues.append({
                "type": "missing_security",
                "severity": "high",
                "description": "Security considerations not explicitly addressed",
                "recommendation": "Add input validation and authentication checks"
            })
            security_score -= 0.2
        
        return {
            "score": max(security_score, 0.0),
            "issues": security_issues,
            "recommendations": [
                "Implement input validation",
                "Add authentication and authorization",
                "Use secure coding practices",
                "Consider data encryption"
            ],
            "vulnerabilities": []
        }
    
    async def _review_performance(self, task: TaskContext) -> Dict[str, Any]:
        """Review performance aspects."""
        performance_issues = []
        performance_score = 0.7
        
        # Check for performance-related indicators
        if any(word in task.description.lower() for word in ["database", "query", "large"]):
            performance_issues.append({
                "type": "database_performance",
                "severity": "medium",
                "description": "Database operations may need optimization",
                "recommendation": "Consider query optimization and indexing"
            })
            performance_score -= 0.1
        
        return {
            "score": max(performance_score, 0.0),
            "issues": performance_issues,
            "recommendations": [
                "Optimize database queries",
                "Consider caching strategies",
                "Profile performance bottlenecks",
                "Use efficient algorithms"
            ],
            "metrics": {
                "estimated_response_time": "100ms",
                "memory_usage": "moderate",
                "scalability": "good"
            }
        }
    
    async def _review_maintainability(self, task: TaskContext) -> Dict[str, Any]:
        """Review maintainability aspects."""
        maintainability_issues = []
        maintainability_score = 0.8
        
        # Check for maintainability indicators
        if len(task.requirements) > 3:
            maintainability_issues.append({
                "type": "complexity",
                "severity": "low",
                "description": "Multiple requirements may increase complexity",
                "recommendation": "Ensure clear separation of concerns"
            })
            maintainability_score -= 0.05
        
        return {
            "score": max(maintainability_score, 0.0),
            "issues": maintainability_issues,
            "recommendations": [
                "Write clear and readable code",
                "Use meaningful variable names",
                "Follow SOLID principles",
                "Add comprehensive documentation"
            ],
            "metrics": {
                "readability_score": 0.8,
                "modularity_score": 0.7,
                "testability_score": 0.6
            }
        }
    
    async def _review_documentation(self, task: TaskContext) -> Dict[str, Any]:
        """Review documentation aspects."""
        documentation_issues = []
        documentation_score = 0.6
        
        # Check if documentation is mentioned in requirements
        has_doc_requirements = any("document" in req.lower() or "comment" in req.lower() 
                                 for req in task.requirements)
        
        if not has_doc_requirements:
            documentation_issues.append({
                "type": "missing_documentation",
                "severity": "medium",
                "description": "Documentation requirements not specified",
                "recommendation": "Add comprehensive documentation"
            })
            documentation_score -= 0.2
        
        return {
            "score": max(documentation_score, 0.0),
            "issues": documentation_issues,
            "recommendations": [
                "Add comprehensive code comments",
                "Create API documentation",
                "Write user guides",
                "Include examples and tutorials"
            ],
            "coverage": {
                "code_comments": 0.3,
                "api_docs": 0.0,
                "user_guides": 0.0
            }
        }
    
    async def _calculate_consensus_score(self, review_results: Dict[str, Any]) -> float:
        """Calculate overall consensus score from review results."""
        if not review_results:
            return 0.0
        
        scores = []
        weights = {
            "code_quality": 0.3,
            "security": 0.25,
            "performance": 0.2,
            "maintainability": 0.15,
            "documentation": 0.1
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for category, results in review_results.items():
            if isinstance(results, dict) and "score" in results:
                weight = weights.get(category, 0.1)
                weighted_sum += results["score"] * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    async def _generate_recommendations(self, review_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on review results."""
        recommendations = []
        
        for category, results in review_results.items():
            if isinstance(results, dict) and "recommendations" in results:
                for rec in results["recommendations"]:
                    recommendations.append({
                        "category": category,
                        "recommendation": rec,
                        "priority": "high" if category == "security" else "medium"
                    })
        
        # Add overall recommendations
        overall_score = await self._calculate_consensus_score(review_results)
        
        if overall_score < 0.6:
            recommendations.append({
                "category": "overall",
                "recommendation": "Consider significant refactoring to improve overall quality",
                "priority": "high"
            })
        elif overall_score < 0.8:
            recommendations.append({
                "category": "overall",
                "recommendation": "Address identified issues to improve quality",
                "priority": "medium"
            })
        else:
            recommendations.append({
                "category": "overall",
                "recommendation": "Code quality is good, minor improvements suggested",
                "priority": "low"
            })
        
        return recommendations
    
    def _generate_quality_summary(self, review_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a quality summary from review results."""
        total_issues = 0
        high_severity_issues = 0
        categories_reviewed = len(review_results)
        
        for results in review_results.values():
            if isinstance(results, dict) and "issues" in results:
                issues = results["issues"]
                total_issues += len(issues)
                high_severity_issues += len([i for i in issues if i.get("severity") == "high"])
        
        return {
            "total_issues": total_issues,
            "high_severity_issues": high_severity_issues,
            "categories_reviewed": categories_reviewed,
            "overall_status": "good" if high_severity_issues == 0 else "needs_attention",
            "summary": f"Found {total_issues} issues across {categories_reviewed} categories"
        }