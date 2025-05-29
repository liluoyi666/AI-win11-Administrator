# AI Command Line Interface Project
## Enhanced Project Overview
This project provides an AI-powered command line interface that interacts with a Windows 11 virtual machine through JSON-formatted commands. The system supports file operations, command execution, and comprehensive logging capabilities.
### Key Components
- **Core Modules**
  - `main.py`: Main entry point for the interaction cycle
  - `main_cycle.py`: Core logic for AI interaction loop
  - `brain/`: Contains core functionality modules
    - `executor.py`: Handles PowerShell command execution
    - `LLM_api.py`: Manages LLM API interactions
    - `String_Templates.py`: Contains prompt templates and syntax definitions

- **Supporting Files**
  - `README_zh.md`: Chinese version documentation
  - `requirements.txt`: Python dependencies
  - `test.py`: Test scripts
- **System Directories**
  - `logs/`: System log directory
    - `ai_log.txt`: AI operation log file
  - `.idea/`: IDE configuration files
  - `__pycache__/`: Python compiled files

## Advanced Features
- JSON Command Interface
- Multi-language Support with UTF-8 encoding
- Comprehensive Security with command validation
- Detailed Logging System for operation tracking

## System Requirements
- Python 3.9+
- PowerShell 7+
- LLM API access (configured in brain/LLM_api.py)

## Usage Instructions
1. Execute `main.py` to initiate the interaction cycle
2. The AI will process JSON-formatted commands
3. Monitor operations through `logs/ai_log.txt`
## Technical Notes
- Always use UTF-8 encoding for files containing Chinese characters
- Automatic error logging for troubleshooting
- Strict security validation for all executed commands

## Project Structure
AI-win11-Administrator/
©À©¤©¤ brain/
©¦   ©À©¤©¤ executor.py
©¦   ©À©¤©¤ LLM_api.py
©¦   ©¸©¤©¤ String_Templates.py
©À©¤©¤ logs/
©¦   ©¸©¤©¤ ai_log.txt
©À©¤©¤ .idea/
©À©¤©¤ __pycache__/
©À©¤©¤ main.py
©À©¤©¤ main_cycle.py
©À©¤©¤ README.md
©À©¤©¤ README_zh.md
©¸©¤©¤ requirements.txt
