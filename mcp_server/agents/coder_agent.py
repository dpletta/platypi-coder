"""
Coder Agent

Specialized agent for implementing code solutions and writing software.
"""

from typing import Dict, List, Any
import json
import logging
from datetime import datetime

from .base_agent import BaseAgent, AgentRole, TaskContext


class CoderAgent(BaseAgent):
    """
    Specialized agent for code implementation and software development.
    
    Capabilities:
    - Code generation and implementation
    - Refactoring and optimization
    - API development
    - Database operations
    - Integration tasks
    """
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any] = None):
        super().__init__(agent_id, role, config)
        self.supported_languages = self.config.get("supported_languages", [
            "python", "javascript", "typescript", "java", "go", "rust", "cpp"
        ])
        self.code_standards = self.config.get("code_standards", {
            "python": "PEP8",
            "javascript": "ESLint",
            "typescript": "TSLint"
        })
        self.max_file_size = self.config.get("max_file_size", 10000)  # lines
    
    def _define_capabilities(self) -> List[str]:
        return [
            "code_generation",
            "refactoring",
            "api_development",
            "database_operations",
            "integration",
            "optimization",
            "testing",
            "documentation"
        ]
    
    async def execute_task(self, task: TaskContext) -> Dict[str, Any]:
        """Execute coding task."""
        self.logger.info(f"Coding task: {task.description}")
        
        try:
            # Analyze the coding task
            analysis = await self._analyze_coding_task(task)
            
            # Generate implementation plan
            implementation_plan = await self._create_implementation_plan(task, analysis)
            
            # Execute the implementation
            implementation_result = await self._execute_implementation(task, implementation_plan)
            
            # Generate documentation
            documentation = await self._generate_documentation(implementation_result)
            
            result = {
                "task_id": task.task_id,
                "analysis": analysis,
                "implementation_plan": implementation_plan,
                "implementation_result": implementation_result,
                "documentation": documentation,
                "code_quality_metrics": self._calculate_quality_metrics(implementation_result),
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            await self.handle_error(e, f"coding task {task.task_id}")
            raise
    
    async def _analyze_coding_task(self, task: TaskContext) -> Dict[str, Any]:
        """Analyze the coding task to understand requirements."""
        description = task.description.lower()
        
        # Detect programming language
        language = self._detect_language(task)
        
        # Detect task type
        task_type = self._detect_task_type(description)
        
        # Analyze complexity
        complexity_indicators = {
            "simple": ["read", "write", "basic", "simple"],
            "moderate": ["implement", "create", "modify", "update"],
            "complex": ["refactor", "optimize", "integrate", "architecture"],
            "advanced": ["performance", "scalability", "security", "distributed"]
        }
        
        complexity_level = "simple"
        for level, indicators in complexity_indicators.items():
            if any(indicator in description for indicator in indicators):
                complexity_level = level
                break
        
        # Estimate effort
        effort_estimate = self._estimate_coding_effort(task, complexity_level)
        
        return {
            "language": language,
            "task_type": task_type,
            "complexity_level": complexity_level,
            "effort_estimate": effort_estimate,
            "requirements": task.requirements,
            "constraints": task.constraints
        }
    
    def _detect_language(self, task: TaskContext) -> str:
        """Detect the programming language from task context."""
        description = task.description.lower()
        requirements_text = " ".join(task.requirements).lower()
        constraints_text = " ".join(task.constraints).lower()
        
        text = f"{description} {requirements_text} {constraints_text}"
        
        language_indicators = {
            "python": ["python", "py", "django", "flask", "fastapi"],
            "javascript": ["javascript", "js", "node", "react", "vue"],
            "typescript": ["typescript", "ts", "angular"],
            "java": ["java", "spring", "maven", "gradle"],
            "go": ["go", "golang", "goroutine"],
            "rust": ["rust", "cargo"],
            "cpp": ["c++", "cpp", "cmake"]
        }
        
        for lang, indicators in language_indicators.items():
            if any(indicator in text for indicator in indicators):
                return lang
        
        return "python"  # Default
    
    def _detect_task_type(self, description: str) -> str:
        """Detect the type of coding task."""
        if any(word in description for word in ["api", "endpoint", "rest", "graphql"]):
            return "api_development"
        elif any(word in description for word in ["database", "db", "sql", "query"]):
            return "database_operation"
        elif any(word in description for word in ["refactor", "optimize", "improve"]):
            return "refactoring"
        elif any(word in description for word in ["test", "unit", "integration"]):
            return "testing"
        elif any(word in description for word in ["integrate", "connect", "merge"]):
            return "integration"
        else:
            return "general_implementation"
    
    def _estimate_coding_effort(self, task: TaskContext, complexity_level: str) -> Dict[str, Any]:
        """Estimate effort required for coding task."""
        base_effort = {
            "simple": 30,      # 30 minutes
            "moderate": 120,   # 2 hours
            "complex": 240,    # 4 hours
            "advanced": 480    # 8 hours
        }
        
        base_time = base_effort.get(complexity_level, 120)
        
        # Adjust based on requirements and constraints
        requirement_multiplier = 1 + (len(task.requirements) * 0.1)
        constraint_multiplier = 1 + (len(task.constraints) * 0.05)
        
        estimated_time = base_time * requirement_multiplier * constraint_multiplier
        
        return {
            "estimated_minutes": int(estimated_time),
            "complexity_level": complexity_level,
            "requirement_count": len(task.requirements),
            "constraint_count": len(task.constraints)
        }
    
    async def _create_implementation_plan(self, task: TaskContext, 
                                        analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed implementation plan."""
        language = analysis["language"]
        task_type = analysis["task_type"]
        complexity_level = analysis["complexity_level"]
        
        plan = {
            "language": language,
            "task_type": task_type,
            "complexity_level": complexity_level,
            "phases": [],
            "dependencies": [],
            "testing_strategy": self._determine_testing_strategy(task_type, complexity_level)
        }
        
        # Generate phases based on task type
        if task_type == "api_development":
            plan["phases"] = [
                {"name": "design", "description": "Design API endpoints and data models"},
                {"name": "implementation", "description": "Implement API endpoints"},
                {"name": "validation", "description": "Add input validation and error handling"},
                {"name": "testing", "description": "Create unit and integration tests"},
                {"name": "documentation", "description": "Generate API documentation"}
            ]
        elif task_type == "database_operation":
            plan["phases"] = [
                {"name": "schema_design", "description": "Design database schema"},
                {"name": "migration", "description": "Create database migrations"},
                {"name": "implementation", "description": "Implement database operations"},
                {"name": "optimization", "description": "Optimize queries and indexes"},
                {"name": "testing", "description": "Test database operations"}
            ]
        elif task_type == "refactoring":
            plan["phases"] = [
                {"name": "analysis", "description": "Analyze existing code"},
                {"name": "planning", "description": "Plan refactoring approach"},
                {"name": "implementation", "description": "Implement refactoring"},
                {"name": "testing", "description": "Ensure functionality is preserved"},
                {"name": "optimization", "description": "Optimize performance"}
            ]
        else:
            plan["phases"] = [
                {"name": "analysis", "description": "Analyze requirements"},
                {"name": "design", "description": "Design solution"},
                {"name": "implementation", "description": "Implement solution"},
                {"name": "testing", "description": "Test implementation"},
                {"name": "documentation", "description": "Document code"}
            ]
        
        return plan
    
    def _determine_testing_strategy(self, task_type: str, complexity_level: str) -> Dict[str, Any]:
        """Determine appropriate testing strategy."""
        strategies = {
            "simple": ["unit_tests"],
            "moderate": ["unit_tests", "integration_tests"],
            "complex": ["unit_tests", "integration_tests", "performance_tests"],
            "advanced": ["unit_tests", "integration_tests", "performance_tests", "security_tests"]
        }
        
        return {
            "test_types": strategies.get(complexity_level, ["unit_tests"]),
            "coverage_target": 0.8 if complexity_level in ["moderate", "complex", "advanced"] else 0.6,
            "automated": True
        }
    
    async def _execute_implementation(self, task: TaskContext, 
                                    plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the implementation based on the plan."""
        # This is a mock implementation - in a real scenario, this would
        # generate actual code based on the task requirements
        
        implementation_result = {
            "files_created": [],
            "files_modified": [],
            "code_snippets": [],
            "dependencies_added": [],
            "configuration_changes": []
        }
        
        # Mock code generation based on task type
        task_type = plan["task_type"]
        language = plan["language"]
        
        if task_type == "api_development":
            implementation_result.update({
                "files_created": [f"api/{task.task_id}_endpoints.{self._get_file_extension(language)}"],
                "code_snippets": [self._generate_api_snippet(language, task)],
                "dependencies_added": self._get_api_dependencies(language)
            })
        elif task_type == "database_operation":
            implementation_result.update({
                "files_created": [f"models/{task.task_id}_model.{self._get_file_extension(language)}"],
                "code_snippets": [self._generate_database_snippet(language, task)],
                "dependencies_added": self._get_database_dependencies(language)
            })
        else:
            implementation_result.update({
                "files_created": [f"src/{task.task_id}.{self._get_file_extension(language)}"],
                "code_snippets": [self._generate_general_snippet(language, task)]
            })
        
        return implementation_result
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for programming language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "go": "go",
            "rust": "rs",
            "cpp": "cpp"
        }
        return extensions.get(language, "py")
    
    def _generate_api_snippet(self, language: str, task: TaskContext) -> str:
        """Generate API code snippet."""
        if language == "python":
            return f'''
# API endpoint for {task.description}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class {task.task_id.title()}Request(BaseModel):
    # Define request model based on requirements
    pass

class {task.task_id.title()}Response(BaseModel):
    # Define response model
    success: bool
    message: str

@app.post("/api/{task.task_id}")
async def {task.task_id}_endpoint(request: {task.task_id.title()}Request):
    """Endpoint for {task.description}"""
    try:
        # Implementation based on requirements: {task.requirements}
        # Constraints: {task.constraints}
        
        return {task.task_id.title()}Response(
            success=True,
            message="Operation completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
        else:
            return f"// API implementation for {task.description} in {language}"
    
    def _generate_database_snippet(self, language: str, task: TaskContext) -> str:
        """Generate database code snippet."""
        if language == "python":
            return f'''
# Database model for {task.description}
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class {task.task_id.title()}Model(Base):
    __tablename__ = '{task.task_id}'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Add fields based on requirements: {task.requirements}
    # Constraints: {task.constraints}
    
    def __repr__(self):
        return f"<{task.task_id.title()}Model(id={{self.id}})>"
'''
        else:
            return f"// Database model for {task.description} in {language}"
    
    def _generate_general_snippet(self, language: str, task: TaskContext) -> str:
        """Generate general code snippet."""
        if language == "python":
            return f'''
# Implementation for {task.description}
def {task.task_id}():
    """
    {task.description}
    
    Requirements: {task.requirements}
    Constraints: {task.constraints}
    """
    # Implementation goes here
    pass

if __name__ == "__main__":
    {task.task_id}()
'''
        else:
            return f"// Implementation for {task.description} in {language}"
    
    def _get_api_dependencies(self, language: str) -> List[str]:
        """Get API dependencies for language."""
        dependencies = {
            "python": ["fastapi", "uvicorn", "pydantic"],
            "javascript": ["express", "cors", "helmet"],
            "typescript": ["express", "@types/express", "cors"],
            "java": ["spring-boot-starter-web", "spring-boot-starter-validation"],
            "go": ["github.com/gin-gonic/gin"],
            "rust": ["axum", "tokio", "serde"]
        }
        return dependencies.get(language, [])
    
    def _get_database_dependencies(self, language: str) -> List[str]:
        """Get database dependencies for language."""
        dependencies = {
            "python": ["sqlalchemy", "alembic"],
            "javascript": ["sequelize", "pg"],
            "typescript": ["typeorm", "pg"],
            "java": ["spring-boot-starter-data-jpa", "h2"],
            "go": ["gorm.io/gorm", "gorm.io/driver/postgres"],
            "rust": ["diesel", "tokio-postgres"]
        }
        return dependencies.get(language, [])
    
    async def _generate_documentation(self, implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate documentation for the implementation."""
        return {
            "readme_section": f"## {implementation_result.get('files_created', ['Unknown'])[0]}\n\nImplementation details and usage instructions.",
            "api_docs": "API documentation if applicable",
            "code_comments": "Generated code includes comprehensive comments",
            "examples": "Usage examples and code samples"
        }
    
    def _calculate_quality_metrics(self, implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate code quality metrics."""
        files_count = len(implementation_result.get("files_created", []))
        snippets_count = len(implementation_result.get("code_snippets", []))
        
        return {
            "files_created": files_count,
            "code_snippets_generated": snippets_count,
            "estimated_lines_of_code": snippets_count * 50,  # Rough estimate
            "complexity_score": min(files_count * 0.2, 1.0),
            "maintainability_score": 0.8,  # Mock score
            "test_coverage": 0.0  # Would be calculated from actual tests
        }