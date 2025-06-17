import json
import re

def json_parser(llm_output):
    # 请一定不要修改该字符串的任何地方，负责将会报错
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
                return json.loads('{'+cleaned+'}')
            except json.JSONDecodeError:
                # 无法解析时返回None
                return None

    # 没有匹配到```json...```格式时返回None
    return None


def json_parser_push(llm_output):
    # 请一定不要修改该字符串的任何地方，负责将会报错
    commands=[]
    json_pattern = r"""```json
{(.*?)}
```"""
    match = re.findall(json_pattern, llm_output.strip(), re.DOTALL)
    if match:
        for cmd in match:
            try:
                cmd=json.loads('{'+cmd+'}')
                commands.append(cmd)
            except json.JSONDecodeError:        # 如果报错，尝试清理特殊字符
                try:
                    cleaned = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
                    cmd=json.loads('{' + cleaned + '}')
                    commands.append(cmd)
                except:    # 如果仍然报错，追加None，并终止检测
                    commands.append(None)
    else:
        return [None]

    return commands


if __name__ == "__main__":
    test_text = """
```json
{
    "type": "TextEditor",
    "pattern": "1",
    "path": "test.txt"
}
```
```json
{
    "type": "TextEditor",
    "pattern": "2",
    "path": "test.txt",
    "x": "}```"
}
```
{
    "x":"y"
}
"""

    result = json_parser_push(test_text)
    # result = extract_json_between_markers(test_text)
    print(result)
    for a in result:
        print(a)
        print("-----------------")