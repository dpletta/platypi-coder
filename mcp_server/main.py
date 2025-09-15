from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

# Import the default_api, assuming it's available in the execution environment
# In a real scenario, this would be a proper import
# For this example, we'll mock the tool calls
class MockTool:
    def __init__(self, name):
        self.name = name
    def __call__(self, **kwargs):
        return {f"{self.name}_response": {"output": f"Mocked {self.name} with args: {kwargs}"}}

class MockApi:
    def __init__(self):
        self.list_directory = MockTool("list_directory")
        self.read_file = MockTool("read_file")
        self.write_file = MockTool("write_file")
        self.replace = MockTool("replace")
        self.run_shell_command = MockTool("run_shell_command")
        self.search_file_content = MockTool("search_file_content")
        self.glob = MockTool("glob")
        self.planner = MockTool("planner")
        self.orchestrator = MockTool("orchestrator")
        self.consensus = MockTool("consensus")
        self.codereview = MockTool("codereview")
        self.debug = MockTool("debug")
        self.google_web_search = MockTool("google_web_search")

default_api = MockApi()


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the MCP Server!"}

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

class GoogleWebSearchRequest(BaseModel):
    query: str


# Endpoints
@app.post("/tools/list_directory")
def list_directory(request: ListDirectoryRequest):
    return default_api.list_directory(**request.dict())

@app.post("/tools/read_file")
def read_file(request: ReadFileRequest):
    return default_api.read_file(**request.dict())

@app.post("/tools/write_file")
def write_file(request: WriteFileRequest):
    return default_api.write_file(**request.dict())

@app.post("/tools/replace")
def replace(request: ReplaceRequest):
    return default_api.replace(**request.dict())

@app.post("/tools/run_shell_command")
def run_shell_command(request: RunShellCommandRequest):
    return default_api.run_shell_command(**request.dict())

@app.post("/tools/search_file_content")
def search_file_content(request: SearchFileContentRequest):
    return default_api.search_file_content(**request.dict())

@app.post("/tools/glob")
def glob(request: GlobRequest):
    return default_api.glob(**request.dict())

@app.post("/tools/planner")
def planner(request: PlannerRequest):
    return default_api.planner(**request.dict())

@app.post("/tools/orchestrator")
def orchestrator(request: OrchestratorRequest):
    return default_api.orchestrator(**request.dict())

@app.post("/tools/consensus")
def consensus(request: ConsensusRequest):
    return default_api.consensus(**request.dict())

@app.post("/tools/codereview")
def codereview(request: CodeReviewRequest):
    return default_api.codereview(**request.dict())

@app.post("/tools/debug")
def debug(request: DebugRequest):
    return default_api.debug(**request.dict())

@app.post("/tools/google_web_search")
def google_web_search(request: GoogleWebSearchRequest):
    return default_api.google_web_search(**request.dict())