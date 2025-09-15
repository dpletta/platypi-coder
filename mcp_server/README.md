# MCP Server

Welcome to the MCP (Model-Centric Programming) Server! This server provides a powerful suite of coding tools to AI models, enabling them to perform a wide range of software development tasks.

## Overview

The MCP Server is a FastAPI-based application that exposes a REST API for various coding tools. These tools are designed to be used by AI agents, such as those running on Ollama, to interact with a development environment, write and modify code, and even collaborate with other agents.

**Note:** The current implementation of the tools is mocked. In a real-world scenario, the tool endpoints would be connected to actual implementations.

## Features

*   **Core Coding Tools:** A comprehensive set of tools for file system operations, code execution, and searching.
*   **Planning & Orchestration:** Tools to break down complex tasks into plans and execute them step-by-step.
*   **Ensemble Coding:** A `consensus` tool that allows multiple AI agents to collaborate on solving problems.
*   **Code Quality & Debugging:** Integrated tools for code review and debugging.
*   **Web Search:** The ability for agents to search the web for information.

## Getting Started

1.  **Installation:**
    ```bash
    # Create a virtual environment
    python3 -m venv venv

    # Activate the virtual environment
    source venv/bin/activate

    # Install the required packages
    pip install -r requirements.txt
    ```

2.  **Running the Server:**
    ```bash
    uvicorn main:app --host 127.0.0.1 --port 8000
    ```

## API Documentation

The server provides automatic OpenAPI (Swagger) documentation for its API. Once the server is running, you can access it at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

This interactive documentation allows you to explore the available endpoints, see the request and response models, and even try out the API directly from your browser.

## Available Tools

All tools are available as POST endpoints under the `/tools/` path.

*(Details of each tool endpoint will be available in the OpenAPI documentation.)*