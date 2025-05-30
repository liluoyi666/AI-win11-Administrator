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


def parse_json_blocks(text: str) -> list:
    """
    解析文本中被 ```json {...} ``` 包裹的多个JSON块

    参数:
        text: 包含JSON块的文本

    返回:
        解析后的JSON对象列表
    """
    json_blocks = []
    # 正则表达式模式匹配 ```json 开头和 ``` 结尾的块
    pattern = r'```json\s*([\s\S]*?)\s*```'
    matches = re.finditer(pattern, text)

    for match in matches:
        json_str = match.group(1).strip()
        try:
            # 尝试直接解析
            parsed = json.loads(json_str)
        except json.JSONDecodeError as e:
            # 处理常见的无效JSON格式
            try:
                # 尝试修复单引号问题
                if "'" in json_str and '"' not in json_str:
                    json_str = json_str.replace("'", '"')
                    parsed = json.loads(json_str)
                else:
                    # 尝试其他恢复策略或忽略
                    continue
            except Exception:
                # 无法恢复，跳过此块
                break
        json_blocks.append(parsed)

    return json_blocks
if __name__ == "__main__":
    test_text = """
{
    "type": "TextEditor",
    "pattern": "append",
    "path": "test.txt",
    "line1": "",
    "line2": "## 使用方法",
    "line3": "系统接受JSON格式的命令，并在PowerShell等环境中执行。以下是一些常见操作的JSON示例：",
    "line4": "",
    "line5": "### 使用PowerShell命令行",
    "line6": "```",
    "line7": "示例代码请见原始README.md文件",
    "line8": "```",
    "encoder": "utf-8",
    "add_log": "向test.md文件追加简化的使用方法部分内容"
}
"""

    result = json.loads(test_text)
    print(result)