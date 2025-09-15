"""
Configuration Management for Agentic Coder MCP Server

This module provides configuration management for the agent ensemble,
including agent behavior settings, ensemble parameters, and runtime configuration.
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    max_subtasks: int = 10
    planning_strategies: list = None
    supported_languages: list = None
    code_standards: dict = None
    quality_thresholds: dict = None
    debugging_strategies: list = None
    test_types: list = None
    coverage_thresholds: dict = None
    
    def __post_init__(self):
        if self.planning_strategies is None:
            self.planning_strategies = ["sequential", "parallel", "iterative", "agile"]
        if self.supported_languages is None:
            self.supported_languages = ["python", "javascript", "typescript", "java", "go", "rust"]
        if self.code_standards is None:
            self.code_standards = {
                "python": "PEP8",
                "javascript": "ESLint", 
                "typescript": "TSLint"
            }
        if self.quality_thresholds is None:
            self.quality_thresholds = {
                "complexity": 10,
                "maintainability": 0.7,
                "test_coverage": 0.8,
                "security_score": 0.9
            }
        if self.debugging_strategies is None:
            self.debugging_strategies = ["systematic", "binary_search", "hypothesis_testing", "log_analysis"]
        if self.test_types is None:
            self.test_types = ["unit", "integration", "performance", "security", "usability"]
        if self.coverage_thresholds is None:
            self.coverage_thresholds = {
                "unit": 0.8,
                "integration": 0.6,
                "overall": 0.7
            }


@dataclass
class EnsembleConfig:
    """Configuration for the agent ensemble."""
    consensus_threshold: float = 0.7
    max_concurrent_tasks: int = 5
    task_timeout: int = 300  # seconds
    retry_attempts: int = 3
    log_level: str = "INFO"
    enable_monitoring: bool = True
    enable_metrics: bool = True
    metrics_interval: int = 60  # seconds


@dataclass
class ServerConfig:
    """Configuration for the MCP server."""
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    reload: bool = False
    log_level: str = "INFO"
    cors_origins: list = None
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]


class ConfigManager:
    """Manages configuration for the agentic coder MCP server."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv("MCP_CONFIG_PATH", "config.json")
        self.logger = logging.getLogger(__name__)
        
        # Default configurations
        self.agent_config = AgentConfig()
        self.ensemble_config = EnsembleConfig()
        self.server_config = ServerConfig()
        
        # Load configuration
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or environment variables."""
        # Try to load from file first
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config_data = json.load(f)
                self._apply_config(config_data)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load config from {self.config_path}: {e}")
        
        # Override with environment variables
        self._load_from_env()
        
        self.logger.info("Configuration loaded successfully")
    
    def _apply_config(self, config_data: Dict[str, Any]):
        """Apply configuration data to config objects."""
        # Agent configuration
        if "agent" in config_data:
            agent_data = config_data["agent"]
            self.agent_config = AgentConfig(**agent_data)
        
        # Ensemble configuration
        if "ensemble" in config_data:
            ensemble_data = config_data["ensemble"]
            self.ensemble_config = EnsembleConfig(**ensemble_data)
        
        # Server configuration
        if "server" in config_data:
            server_data = config_data["server"]
            self.server_config = ServerConfig(**server_data)
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Agent configuration
        if os.getenv("MCP_AGENT_MAX_SUBTASKS"):
            self.agent_config.max_subtasks = int(os.getenv("MCP_AGENT_MAX_SUBTASKS"))
        
        if os.getenv("MCP_AGENT_SUPPORTED_LANGUAGES"):
            self.agent_config.supported_languages = os.getenv("MCP_AGENT_SUPPORTED_LANGUAGES").split(",")
        
        # Ensemble configuration
        if os.getenv("MCP_CONSENSUS_THRESHOLD"):
            self.ensemble_config.consensus_threshold = float(os.getenv("MCP_CONSENSUS_THRESHOLD"))
        
        if os.getenv("MCP_MAX_CONCURRENT_TASKS"):
            self.ensemble_config.max_concurrent_tasks = int(os.getenv("MCP_MAX_CONCURRENT_TASKS"))
        
        if os.getenv("MCP_TASK_TIMEOUT"):
            self.ensemble_config.task_timeout = int(os.getenv("MCP_TASK_TIMEOUT"))
        
        if os.getenv("MCP_LOG_LEVEL"):
            self.ensemble_config.log_level = os.getenv("MCP_LOG_LEVEL")
        
        # Server configuration
        if os.getenv("MCP_HOST"):
            self.server_config.host = os.getenv("MCP_HOST")
        
        if os.getenv("MCP_PORT"):
            self.server_config.port = int(os.getenv("MCP_PORT"))
        
        if os.getenv("MCP_WORKERS"):
            self.server_config.workers = int(os.getenv("MCP_WORKERS"))
        
        if os.getenv("MCP_RELOAD"):
            self.server_config.reload = os.getenv("MCP_RELOAD").lower() == "true"
    
    def save_config(self):
        """Save current configuration to file."""
        config_data = {
            "agent": asdict(self.agent_config),
            "ensemble": asdict(self.ensemble_config),
            "server": asdict(self.server_config)
        }
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save config to {self.config_path}: {e}")
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent configuration as dictionary."""
        return {
            "planner": {
                "max_subtasks": self.agent_config.max_subtasks,
                "planning_strategies": self.agent_config.planning_strategies
            },
            "coder": {
                "supported_languages": self.agent_config.supported_languages,
                "code_standards": self.agent_config.code_standards
            },
            "reviewer": {
                "quality_thresholds": self.agent_config.quality_thresholds
            },
            "debugger": {
                "debugging_strategies": self.agent_config.debugging_strategies
            },
            "tester": {
                "test_types": self.agent_config.test_types,
                "coverage_thresholds": self.agent_config.coverage_thresholds
            }
        }
    
    def get_ensemble_config(self) -> Dict[str, Any]:
        """Get ensemble configuration as dictionary."""
        return asdict(self.ensemble_config)
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration as dictionary."""
        return asdict(self.server_config)
    
    def update_agent_config(self, agent_name: str, config_updates: Dict[str, Any]):
        """Update configuration for a specific agent."""
        if agent_name == "planner":
            if "max_subtasks" in config_updates:
                self.agent_config.max_subtasks = config_updates["max_subtasks"]
            if "planning_strategies" in config_updates:
                self.agent_config.planning_strategies = config_updates["planning_strategies"]
        
        elif agent_name == "coder":
            if "supported_languages" in config_updates:
                self.agent_config.supported_languages = config_updates["supported_languages"]
            if "code_standards" in config_updates:
                self.agent_config.code_standards = config_updates["code_standards"]
        
        elif agent_name == "reviewer":
            if "quality_thresholds" in config_updates:
                self.agent_config.quality_thresholds = config_updates["quality_thresholds"]
        
        elif agent_name == "debugger":
            if "debugging_strategies" in config_updates:
                self.agent_config.debugging_strategies = config_updates["debugging_strategies"]
        
        elif agent_name == "tester":
            if "test_types" in config_updates:
                self.agent_config.test_types = config_updates["test_types"]
            if "coverage_thresholds" in config_updates:
                self.agent_config.coverage_thresholds = config_updates["coverage_thresholds"]
        
        self.logger.info(f"Updated configuration for {agent_name}")
    
    def update_ensemble_config(self, config_updates: Dict[str, Any]):
        """Update ensemble configuration."""
        for key, value in config_updates.items():
            if hasattr(self.ensemble_config, key):
                setattr(self.ensemble_config, key, value)
        
        self.logger.info("Updated ensemble configuration")
    
    def update_server_config(self, config_updates: Dict[str, Any]):
        """Update server configuration."""
        for key, value in config_updates.items():
            if hasattr(self.server_config, key):
                setattr(self.server_config, key, value)
        
        self.logger.info("Updated server configuration")
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration."""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate agent configuration
        if self.agent_config.max_subtasks < 1:
            validation_results["errors"].append("max_subtasks must be at least 1")
            validation_results["valid"] = False
        
        if not self.agent_config.supported_languages:
            validation_results["warnings"].append("No supported languages configured")
        
        # Validate ensemble configuration
        if not 0 <= self.ensemble_config.consensus_threshold <= 1:
            validation_results["errors"].append("consensus_threshold must be between 0 and 1")
            validation_results["valid"] = False
        
        if self.ensemble_config.max_concurrent_tasks < 1:
            validation_results["errors"].append("max_concurrent_tasks must be at least 1")
            validation_results["valid"] = False
        
        if self.ensemble_config.task_timeout < 30:
            validation_results["warnings"].append("task_timeout is very low, may cause timeouts")
        
        # Validate server configuration
        if not 1 <= self.server_config.port <= 65535:
            validation_results["errors"].append("port must be between 1 and 65535")
            validation_results["valid"] = False
        
        if self.server_config.workers < 1:
            validation_results["errors"].append("workers must be at least 1")
            validation_results["valid"] = False
        
        return validation_results
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        return {
            "agent": {
                "max_subtasks": self.agent_config.max_subtasks,
                "supported_languages_count": len(self.agent_config.supported_languages),
                "planning_strategies_count": len(self.agent_config.planning_strategies),
                "test_types_count": len(self.agent_config.test_types)
            },
            "ensemble": {
                "consensus_threshold": self.ensemble_config.consensus_threshold,
                "max_concurrent_tasks": self.ensemble_config.max_concurrent_tasks,
                "task_timeout": self.ensemble_config.task_timeout,
                "monitoring_enabled": self.ensemble_config.enable_monitoring
            },
            "server": {
                "host": self.server_config.host,
                "port": self.server_config.port,
                "workers": self.server_config.workers,
                "reload": self.server_config.reload
            }
        }


# Global configuration instance
config_manager = ConfigManager()