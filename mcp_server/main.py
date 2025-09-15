from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio
import logging
import os
import json
from datetime import datetime
from dataclasses import asdict

# Import the agentic ensemble
from agents import AgentManager, PlannerAgent, CoderAgent, ReviewerAgent, DebuggerAgent, TesterAgent
from agents.base_agent import AgentRole, TaskContext

# Import configuration and monitoring
from config import config_manager
from monitoring import metrics_collector, structured_logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the agentic ensemble with configuration
ensemble_config = config_manager.get_ensemble_config()
agent_config = config_manager.get_agent_config()

agent_manager = AgentManager({
    "consensus_threshold": ensemble_config["consensus_threshold"],
    "max_concurrent_tasks": ensemble_config["max_concurrent_tasks"],
    "task_timeout": ensemble_config["task_timeout"],
    "agents": agent_config
})


app = FastAPI(
    title="Agentic Coder MCP Server",
    description="A sophisticated MCP server with ensemble of specialized coding agents",
    version="2.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Agentic Coder MCP Server!",
        "version": "2.0.0",
        "agents": ["planner", "coder", "reviewer", "debugger", "tester"],
        "features": ["ensemble_collaboration", "intelligent_planning", "quality_assurance", "automated_testing"]
    }

@app.get("/metrics")
async def get_metrics():
    """Get system metrics and performance data."""
    try:
        return {
            "performance_summary": metrics_collector.get_performance_summary(),
            "health_status": metrics_collector.get_health_status(),
            "system_metrics": [asdict(m) for m in metrics_collector.get_system_metrics(5)],
            "agent_metrics": {aid: asdict(m) for aid, m in metrics_collector.get_all_agent_metrics().items()}
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
async def get_configuration():
    """Get current configuration."""
    try:
        return {
            "agent_config": config_manager.get_agent_config(),
            "ensemble_config": config_manager.get_ensemble_config(),
            "server_config": config_manager.get_server_config(),
            "config_summary": config_manager.get_config_summary(),
            "validation": config_manager.validate_config()
        }
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/config/update")
async def update_configuration(request: Dict[str, Any]):
    """Update configuration."""
    try:
        if "agent" in request:
            for agent_name, config_updates in request["agent"].items():
                config_manager.update_agent_config(agent_name, config_updates)
        
        if "ensemble" in request:
            config_manager.update_ensemble_config(request["ensemble"])
        
        if "server" in request:
            config_manager.update_server_config(request["server"])
        
        # Save configuration
        config_manager.save_config()
        
        return {"status": "success", "message": "Configuration updated successfully"}
    except Exception as e:
        logger.error(f"Error updating configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Core file system tools
async def list_directory_impl(path: str, ignore: Optional[List[str]] = None) -> Dict[str, Any]:
    """List directory contents."""
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Path not found: {path}")
        
        if not os.path.isdir(path):
            raise HTTPException(status_code=400, detail=f"Path is not a directory: {path}")
        
        ignore_set = set(ignore or [])
        items = []
        
        for item in os.listdir(path):
            if item in ignore_set:
                continue
            
            item_path = os.path.join(path, item)
            stat = os.stat(item_path)
            
            items.append({
                "name": item,
                "path": item_path,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        return {
            "path": path,
            "items": items,
            "count": len(items)
        }
    except Exception as e:
        logger.error(f"Error listing directory {path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def read_file_impl(absolute_path: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
    """Read file contents."""
    try:
        if not os.path.exists(absolute_path):
            raise HTTPException(status_code=404, detail=f"File not found: {absolute_path}")
        
        if not os.path.isfile(absolute_path):
            raise HTTPException(status_code=400, detail=f"Path is not a file: {absolute_path}")
        
        with open(absolute_path, 'r', encoding='utf-8') as f:
            if offset:
                f.seek(offset)
            
            if limit:
                content = f.read(limit)
            else:
                content = f.read()
        
        stat = os.stat(absolute_path)
        
        return {
            "path": absolute_path,
            "content": content,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "lines": len(content.splitlines()) if content else 0
        }
    except Exception as e:
        logger.error(f"Error reading file {absolute_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def write_file_impl(file_path: str, content: str) -> Dict[str, Any]:
    """Write content to file."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        stat = os.stat(file_path)
        
        return {
            "path": file_path,
            "size": stat.st_size,
            "lines": len(content.splitlines()),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def replace_impl(file_path: str, old_string: str, new_string: str, expected_replacements: Optional[int] = None) -> Dict[str, Any]:
    """Replace text in file."""
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences
        count = content.count(old_string)
        
        if expected_replacements and count != expected_replacements:
            raise HTTPException(
                status_code=400, 
                detail=f"Expected {expected_replacements} replacements, found {count}"
            )
        
        # Perform replacement
        new_content = content.replace(old_string, new_string)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            "path": file_path,
            "replacements_made": count,
            "old_string": old_string,
            "new_string": new_string
        }
    except Exception as e:
        logger.error(f"Error replacing in file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_shell_command_impl(command: str, description: Optional[str] = None, directory: Optional[str] = None) -> Dict[str, Any]:
    """Run shell command."""
    try:
        import subprocess
        
        # Change to specified directory if provided
        cwd = directory if directory and os.path.exists(directory) else None
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300  # 5 minute timeout
        )
        
        return {
            "command": command,
            "description": description,
            "directory": cwd,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timed out")
    except Exception as e:
        logger.error(f"Error running command {command}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Models
class ListDirectoryRequest(BaseModel):
    path: str
    ignore: Optional[List[str]] = None

class ReadFileRequest(BaseModel):
    absolute_path: str
    limit: Optional[int] = None
    offset: Optional[int] = None

class WriteFileRequest(BaseModel):
    file_path: str
    content: str

class ReplaceRequest(BaseModel):
    file_path: str
    old_string: str
    new_string: str
    expected_replacements: Optional[int] = None

class RunShellCommandRequest(BaseModel):
    command: str
    description: Optional[str] = None
    directory: Optional[str] = None

class SearchFileContentRequest(BaseModel):
    pattern: str
    include: Optional[str] = None
    path: Optional[str] = None

class GlobRequest(BaseModel):
    pattern: str
    case_sensitive: Optional[bool] = None
    path: Optional[str] = None
    respect_git_ignore: Optional[bool] = None

class PlannerRequest(BaseModel):
    task: str

class OrchestratorRequest(BaseModel):
    plan: List[Dict]

class ConsensusRequest(BaseModel):
    problem: str
    solutions: List[str]

class CodeReviewRequest(BaseModel):
    code: str

class DebugRequest(BaseModel):
    code: str
    error: str

class TestRequest(BaseModel):
    description: str
    requirements: Optional[List[str]] = None

class GoogleWebSearchRequest(BaseModel):
    query: str


# Core tool endpoints
@app.post("/tools/list_directory")
async def list_directory(request: ListDirectoryRequest):
    """List directory contents."""
    return await list_directory_impl(request.path, request.ignore)

@app.post("/tools/read_file")
async def read_file(request: ReadFileRequest):
    """Read file contents."""
    return await read_file_impl(request.absolute_path, request.limit, request.offset)

@app.post("/tools/write_file")
async def write_file(request: WriteFileRequest):
    """Write content to file."""
    return await write_file_impl(request.file_path, request.content)

@app.post("/tools/replace")
async def replace(request: ReplaceRequest):
    """Replace text in file."""
    return await replace_impl(request.file_path, request.old_string, request.new_string, request.expected_replacements)

@app.post("/tools/run_shell_command")
async def run_shell_command(request: RunShellCommandRequest):
    """Run shell command."""
    return await run_shell_command_impl(request.command, request.description, request.directory)

# Agentic tool endpoints
@app.post("/tools/planner")
async def planner(request: PlannerRequest):
    """Plan complex tasks using the planner agent."""
    try:
        task_id = await agent_manager.submit_task(
            description=request.task,
            requirements=[],
            constraints=[],
            priority=2
        )
        
        # Get the result from the planner agent
        planner_agent = agent_manager.agents.get("planner_agent")
        if planner_agent and planner_agent.current_task:
            result = await planner_agent.execute_task(planner_agent.current_task)
            await planner_agent.complete_task(result)
            return result
        else:
            return {"error": "Planner agent not available"}
    except Exception as e:
        logger.error(f"Error in planner: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/orchestrator")
async def orchestrator(request: OrchestratorRequest):
    """Orchestrate execution of a plan using multiple agents."""
    try:
        # Convert plan to task requirements
        requirements = [step.get("description", "") for step in request.plan]
        
        task_id = await agent_manager.submit_task(
            description="Execute orchestrated plan",
            requirements=requirements,
            constraints=[],
            priority=3
        )
        
        # The agent manager will handle the orchestration
        return {
            "task_id": task_id,
            "status": "orchestration_started",
            "plan_steps": len(request.plan),
            "message": "Plan execution started by agent ensemble"
        }
    except Exception as e:
        logger.error(f"Error in orchestrator: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/consensus")
async def consensus(request: ConsensusRequest):
    """Build consensus on solutions using multiple agents."""
    try:
        # Use reviewer agent for consensus building
        reviewer_agent = agent_manager.agents.get("reviewer_agent")
        if not reviewer_agent:
            raise HTTPException(status_code=500, detail="Reviewer agent not available")
        
        # Create consensus task
        task = TaskContext(
            task_id=f"consensus_{datetime.now().timestamp()}",
            description=f"Build consensus on: {request.problem}",
            requirements=request.solutions,
            constraints=[]
        )
        
        await reviewer_agent.assign_task(task)
        result = await reviewer_agent.execute_task(task)
        await reviewer_agent.complete_task(result)
        
        return {
            "consensus_score": result.get("consensus_score", 0.0),
            "recommendations": result.get("recommendations", []),
            "quality_summary": result.get("quality_summary", {}),
            "solutions_analyzed": len(request.solutions)
        }
    except Exception as e:
        logger.error(f"Error in consensus: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/codereview")
async def codereview(request: CodeReviewRequest):
    """Perform code review using the reviewer agent."""
    try:
        reviewer_agent = agent_manager.agents.get("reviewer_agent")
        if not reviewer_agent:
            raise HTTPException(status_code=500, detail="Reviewer agent not available")
        
        task = TaskContext(
            task_id=f"review_{datetime.now().timestamp()}",
            description="Review provided code",
            requirements=[request.code],
            constraints=[]
        )
        
        await reviewer_agent.assign_task(task)
        result = await reviewer_agent.execute_task(task)
        await reviewer_agent.complete_task(result)
        
        return {
            "review_results": result.get("review_results", {}),
            "consensus_score": result.get("consensus_score", 0.0),
            "recommendations": result.get("recommendations", []),
            "quality_summary": result.get("quality_summary", {})
        }
    except Exception as e:
        logger.error(f"Error in codereview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/debug")
async def debug(request: DebugRequest):
    """Debug code issues using the debugger agent."""
    try:
        debugger_agent = agent_manager.agents.get("debugger_agent")
        if not debugger_agent:
            raise HTTPException(status_code=500, detail="Debugger agent not available")
        
        task = TaskContext(
            task_id=f"debug_{datetime.now().timestamp()}",
            description=f"Debug error: {request.error}",
            requirements=[request.code],
            constraints=[]
        )
        
        await debugger_agent.assign_task(task)
        result = await debugger_agent.execute_task(task)
        await debugger_agent.complete_task(result)
        
        return {
            "debugging_result": result.get("debugging_result", {}),
            "fix_result": result.get("fix_result", {}),
            "validation_result": result.get("validation_result", {}),
            "prevention_strategies": result.get("prevention_strategies", []),
            "debugging_summary": result.get("debugging_summary", {})
        }
    except Exception as e:
        logger.error(f"Error in debug: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/test")
async def test(request: TestRequest):
    """Run tests using the tester agent."""
    try:
        tester_agent = agent_manager.agents.get("tester_agent")
        if not tester_agent:
            raise HTTPException(status_code=500, detail="Tester agent not available")
        
        task = TaskContext(
            task_id=f"test_{datetime.now().timestamp()}",
            description=f"Test: {request.description}",
            requirements=request.requirements or [],
            constraints=[]
        )
        
        await tester_agent.assign_task(task)
        result = await tester_agent.execute_task(task)
        await tester_agent.complete_task(result)
        
        return {
            "test_plan": result.get("test_plan", {}),
            "test_cases": result.get("test_cases", []),
            "test_results": result.get("test_results", {}),
            "analysis_results": result.get("analysis_results", {}),
            "recommendations": result.get("recommendations", []),
            "testing_summary": result.get("testing_summary", {})
        }
    except Exception as e:
        logger.error(f"Error in test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/ensemble_status")
async def ensemble_status():
    """Get status of the agent ensemble."""
    try:
        status = await agent_manager.get_ensemble_status()
        return status
    except Exception as e:
        logger.error(f"Error getting ensemble status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional utility endpoints
@app.post("/tools/search_file_content")
async def search_file_content(request: SearchFileContentRequest):
    """Search for content in files."""
    try:
        import re
        import glob
        
        pattern = request.pattern
        path = request.path or "."
        include_pattern = request.include or "*"
        
        # Find files matching include pattern
        search_path = os.path.join(path, "**", include_pattern)
        files = glob.glob(search_path, recursive=True)
        
        results = []
        for file_path in files:
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.finditer(pattern, content, re.MULTILINE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            results.append({
                                "file": file_path,
                                "line": line_num,
                                "match": match.group(),
                                "context": content[max(0, match.start()-50):match.end()+50]
                            })
                except Exception:
                    continue
        
        return {
            "pattern": pattern,
            "files_searched": len(files),
            "matches_found": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error searching file content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/glob")
async def glob(request: GlobRequest):
    """Find files matching glob pattern."""
    try:
        import glob
        
        pattern = request.pattern
        path = request.path or "."
        full_pattern = os.path.join(path, pattern)
        
        files = glob.glob(full_pattern, recursive=True)
        
        results = []
        for file_path in files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                results.append({
                    "path": file_path,
                    "type": "directory" if os.path.isdir(file_path) else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return {
            "pattern": pattern,
            "path": path,
            "matches": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in glob: {e}")
        raise HTTPException(status_code=500, detail=str(e))