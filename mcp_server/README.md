# Agentic Coder MCP Server

Welcome to the Agentic Coder MCP Server! This is a sophisticated Model-Centric Programming (MCP) server that leverages an ensemble of specialized AI agents to provide intelligent coding assistance, automated development workflows, and collaborative problem-solving capabilities.

## 🚀 Overview

The Agentic Coder MCP Server represents a next-generation approach to AI-assisted software development. Instead of relying on a single AI model, it employs a coordinated ensemble of specialized agents, each with distinct capabilities and expertise areas. This architecture enables more sophisticated problem-solving, better quality assurance, and more reliable outcomes.

## 🏗️ Architecture

### Agent Ensemble

The server features five specialized agents working in collaboration:

1. **Planner Agent** - Task decomposition and strategic planning
2. **Coder Agent** - Code implementation and software development
3. **Reviewer Agent** - Code quality assessment and validation
4. **Debugger Agent** - Error analysis and problem resolution
5. **Tester Agent** - Test generation and quality assurance

### Core Components

- **Agent Manager**: Orchestrates agent collaboration and task distribution
- **Configuration System**: Manages agent behavior and ensemble settings
- **Monitoring System**: Tracks performance, metrics, and system health
- **Consensus Mechanism**: Ensures quality through multi-agent validation

## ✨ Features

### Intelligent Planning
- Automatic task decomposition into manageable sub-tasks
- Strategic planning with multiple execution approaches
- Dependency analysis and timeline estimation
- Risk assessment and mitigation strategies

### Collaborative Coding
- Multi-agent code generation and implementation
- Real-time code review and quality assessment
- Automated debugging and error resolution
- Comprehensive testing and validation

### Quality Assurance
- Multi-perspective code review
- Security vulnerability detection
- Performance analysis and optimization
- Best practices validation

### Advanced Monitoring
- Real-time performance metrics
- Agent activity tracking
- System health monitoring
- Comprehensive logging and analytics

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp_server
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the system:**
   ```bash
   # Optional: Create custom configuration
   cp config.json.example config.json
   # Edit config.json with your preferences
   ```

## 🚀 Running the Server

### Basic Usage
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Custom Configuration
```bash
MCP_CONFIG_PATH=./config.json uvicorn main:app --host 127.0.0.1 --port 8000
```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Documentation**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

## 🔧 Available Tools

### Core File System Tools
- `list_directory` - List directory contents
- `read_file` - Read file contents with optional limits
- `write_file` - Write content to files
- `replace` - Replace text in files
- `run_shell_command` - Execute shell commands
- `search_file_content` - Search for content in files
- `glob` - Find files matching patterns

### Agentic Tools
- `planner` - Intelligent task planning and decomposition
- `orchestrator` - Multi-agent task orchestration
- `consensus` - Collaborative solution validation
- `codereview` - Comprehensive code review
- `debug` - Automated debugging and error resolution
- `test` - Test generation and execution

### Management Tools
- `ensemble_status` - Get agent ensemble status
- `metrics` - System performance metrics
- `config` - Configuration management
- `health` - System health check

## ⚙️ Configuration

The server supports extensive configuration through:

### Environment Variables
```bash
# Agent Configuration
MCP_AGENT_MAX_SUBTASKS=10
MCP_AGENT_SUPPORTED_LANGUAGES=python,javascript,typescript

# Ensemble Configuration
MCP_CONSENSUS_THRESHOLD=0.7
MCP_MAX_CONCURRENT_TASKS=5
MCP_TASK_TIMEOUT=300

# Server Configuration
MCP_HOST=127.0.0.1
MCP_PORT=8000
MCP_WORKERS=1
MCP_LOG_LEVEL=INFO
```

### Configuration File
Create a `config.json` file with:
```json
{
  "agent": {
    "max_subtasks": 10,
    "supported_languages": ["python", "javascript", "typescript"],
    "quality_thresholds": {
      "complexity": 10,
      "maintainability": 0.7,
      "test_coverage": 0.8
    }
  },
  "ensemble": {
    "consensus_threshold": 0.7,
    "max_concurrent_tasks": 5,
    "task_timeout": 300
  },
  "server": {
    "host": "127.0.0.1",
    "port": 8000,
    "workers": 1
  }
}
```

## 📊 Monitoring and Metrics

### Real-time Metrics
Access system metrics at `/metrics`:
- Task execution statistics
- Agent performance data
- System resource usage
- Health status indicators

### Health Monitoring
Check system health at `/health`:
- Agent availability
- System resource status
- Error rates and performance

### Structured Logging
All activities are logged with structured JSON format:
- Task execution logs
- Agent activity tracking
- Error reporting
- Performance metrics

## 🔄 Usage Examples

### Basic Task Planning
```python
import requests

# Plan a complex task
response = requests.post("http://127.0.0.1:8000/tools/planner", json={
    "task": "Implement a REST API for user management with authentication"
})

plan = response.json()
print(f"Task decomposed into {len(plan['sub_tasks'])} sub-tasks")
```

### Collaborative Code Review
```python
# Review code using multiple agents
response = requests.post("http://127.0.0.1:8000/tools/codereview", json={
    "code": """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
"""
})

review = response.json()
print(f"Consensus score: {review['consensus_score']}")
print(f"Recommendations: {review['recommendations']}")
```

### Automated Testing
```python
# Generate and run tests
response = requests.post("http://127.0.0.1:8000/tools/test", json={
    "description": "Test the user authentication system",
    "requirements": ["unit_tests", "integration_tests", "security_tests"]
})

test_results = response.json()
print(f"Generated {len(test_results['test_cases'])} test cases")
print(f"Success rate: {test_results['testing_summary']['success_rate']}")
```

## 🏥 Health and Monitoring

### System Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Performance Metrics
```bash
curl http://127.0.0.1:8000/metrics
```

### Agent Status
```bash
curl http://127.0.0.1:8000/tools/ensemble_status
```

## 🔧 Development

### Project Structure
```
mcp_server/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── agent_manager.py   # Agent orchestration
│   ├── planner_agent.py   # Planning agent
│   ├── coder_agent.py     # Coding agent
│   ├── reviewer_agent.py  # Review agent
│   ├── debugger_agent.py  # Debug agent
│   └── tester_agent.py    # Test agent
├── config.py              # Configuration management
├── monitoring.py          # Metrics and logging
├── main.py               # FastAPI application
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Adding New Agents
1. Create a new agent class inheriting from `BaseAgent`
2. Implement required methods (`_define_capabilities`, `execute_task`)
3. Register the agent in the `AgentManager`
4. Add configuration options in `config.py`

### Extending Functionality
- Add new tool endpoints in `main.py`
- Implement agent-specific capabilities
- Extend monitoring and metrics collection
- Add new configuration options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the configuration options
- Check system health and metrics
- Review logs for error details

## 🔮 Future Enhancements

- Integration with external LLM providers
- Advanced consensus algorithms
- Real-time collaboration features
- Enhanced security and authentication
- Plugin system for custom agents
- Integration with CI/CD pipelines