import json
import re

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
            # Attempt to fix common JSON issues
            try:
                # Remove invalid control characters
                json_string_clean = re.sub(r"[\x00-\x1F\x7F]", "", json_string)
                parsed_json = json.loads(json_string_clean)
                return parsed_json
            except json.JSONDecodeError:
                continue  # Try next match

    return None


import json
import re


def json_parser(llm_output):
    # 匹配最外层且首次出现的```json...```代码块
    json_pattern = r"""```json
{(.*?)}
```"""
    match = re.search(json_pattern, llm_output, re.DOTALL)
    if match:
        json_string = match.group(1).strip()
        try:
            # 尝试直接解析
            return json.loads('{'+json_string+'}')
        except json.JSONDecodeError:
            try:
                # 清理无效控制字符后解析
                cleaned = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
                return json.loads(cleaned)
            except json.JSONDecodeError:
                # 无法解析时返回None
                return None

    # 没有匹配到```json...```格式时返回None
    return None
if __name__ == "__main__":
    test_text = """
```json
{
    "type": "TextEditor",
    "pattern": "write",
    "path": "test.txt",
    "create": true,
    "line1": "***This will maximize the capabilities of AI***",
    "line2": "```json",
    "line3": "{",
    "line4": "    \\"type\\": \\"powershell\\",",
    "line5": "    \\"command\\": \\"你要执行的命令\\",",
    "line6": "    \\"add_log\\": \\"执行指令时顺便写入日志\\"",
    "line7": "}",
    "line8": "```",
    "encoder": "utf-8",
    "add_log": "将README.md中带有转义字符的部分写入test.txt"
}
```
"""

    result = json_parser(test_text)
    # result = extract_json_between_markers(test_text)
    print(result)