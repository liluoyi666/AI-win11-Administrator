import time
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import re

#json解构器
def extract_json_between_markers(llm_output):
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
            try:
                json_string_clean = re.sub(r"[\x00-\x1F\x7F]", "", json_string)
                parsed_json = json.loads(json_string_clean)
                return parsed_json
            except json.JSONDecodeError:
                continue

    return None

x1="""```json{
    "type": "powershell",
    "command": "Add-Content String.py -Value \"\"\"\n# 新增语法规则\nfile_operations=\"\"\"\n文件操作权限验证:\n{\n    \"type\": \"verify_permission\",\n    \"filepath\": \"要验证的文件路径\",\n    \"required_permission\": \"需要的权限级别\"\n}\n\n敏感操作确认机制:\n{\n    \"type\": \"confirm_action\",\n    \"action\": \"要确认的操作描述\",\n    \"confirmation\": \"用户确认信息\"\n}\n\n操作历史记录:\n{\n    \"type\": \"log_history\",\n    \"action\": \"执行的操作描述\",\n    \"details\": \"操作详细信息\"\n}\n\"\"\" -Encoding utf8"
}```"""

x2="""```json{
    "type": "powershell",
    "command": "Get-ChildItem"
}```"""

y1=extract_json_between_markers(x1)
y2=extract_json_between_markers(x2)

print(y1,'\n')
print(y2)