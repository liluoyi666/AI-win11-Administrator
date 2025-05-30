import json
import re

def extract_json_between_markers(llm_output):
    # 该代码来自https://github.com/SakanaAI/AI-Scientist.git，特别感谢

    json_pattern = r"```json(.*?)```"
    matches = re.findall(json_pattern, llm_output, re.DOTALL)

    if not matches:
        json_pattern = r"\{.*?\}"
        matches = re.findall(json_pattern, llm_output, re.DOTALL)

    for json_string in matches:
        json_string = json_string.strip()
        try:
            parsed_json = json.loads(json_string)
            return parsed_json
        except json.JSONDecodeError:
            # Attempt to fix common JSON issues
            try:
                # Remove invalid control characters
                json_string_clean = re.sub(r"[\x00-\x1F\x7F]", "", json_string)
                parsed_json = json.loads(json_string_clean)
                return parsed_json
            except json.JSONDecodeError:
                continue  # Try next match

    return None

if __name__ == "__main__":

    x1 = """
```json{
    "type": "powershell",
    "command": "Get-ChildItem -Recurse | Where-Object { $_.Name -match 'README' } | Select-Object -ExpandProperty FullName",
    "add_log": "为enhanced_README.md添加更详细的技术文档和架构说明"
}```
"""
    x2 = """
```json{
    "type": "powershell",
    "command": "Get-ChildItem -Recurse | Where-Object { $_.Name -match 'README' } | Select-Object -ExpandProperty FullName",
    "add_log": "为enhanced_README.md添加更详细的技术文档和架构说明"
}```
"""

    y=extract_json_between_markers(x1)
    print(y)
    y=json.loads(x1)
    print(y)
