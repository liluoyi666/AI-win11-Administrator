# AI Command Line Interface Project
## Overview
This project provides an AI-powered command line interface that allows interaction with a Windows 11 virtual machine through JSON-formatted commands. The system enables file operations, command execution, and logging capabilities.

```
Execute system commands:
{
    "type": "powershell",
    "command": "your commands",
}
```

## Project Structure
- `main.py`: Main entry point that initiates the interaction cycle
- `main_cycle.py`: Core logic for handling the interaction loop with the AI
- `brain/`: Module containing core functionality
  - `executor.py`: Handles PowerShell command execution
  - `LLM_api.py`: Manages LLM API interactions
  - `String_Templates.py`: Contains prompt templates and grammar definitions
- `logs/`: Directory for system logs
  - `ai_log.txt`: Log file for AI operations
## Features
- JSON-based command interface
- PowerShell command execution
- LLM integration for intelligent responses
- Comprehensive logging system
- UTF-8 encoding support for multilingual content
## Requirements
- Python 3.9+
- PowerShell 7+
- LLM API access (configured in brain/LLM_api.py)
## Usage
1. Run `main.py` to start the interaction cycle
2. The AI will process commands in JSON format
3. View logs in `logs/ai_log.txt` for operation history
## Notes
- Chinese characters require `-Encoding utf8` parameter when reading files
- Error handling includes automatic logging for troubleshooting
- Security validation is enforced for all executed commands
