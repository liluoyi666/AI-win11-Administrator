import json
import os

class TextEditor:
    @staticmethod
    def execute(params: dict) -> (str, str):
        pattern = params.get('pattern', '')
        path = params.get('path', '')
        create = params.get('create', False)
        encoder = params.get('encoder', 'utf-8')

        if not path or not pattern:
            return "", "Missing 'path' or 'pattern' in parameters"

        # 根据操作类型路由到对应方法
        try:
            if pattern == 'read':
                return TextEditor._read(params, path, create, encoder)
            elif pattern == 'write':
                return TextEditor._write(params, path, create, encoder)
            elif pattern == 'change':
                return TextEditor._change(params, path, create, encoder)
            elif pattern == 'append':
                return TextEditor._append(params, path, create, encoder)
            else:
                return "", f"Error: Unknown pattern '{pattern}'"
        except Exception as e:
            return "", f"Error: {str(e)}"

    @staticmethod
    def _ensure_dir(path: str):
        """用于创建文件"""
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @staticmethod
    def _load_file(path: str, create: bool, encoder: str) -> (list, str):
        """加载文件内容，返回行列表和错误信息"""
        if not os.path.exists(path):
            if create:
                TextEditor._ensure_dir(path)
                open(path, 'w', encoding=encoder).close()
                return [], ""
            return "", f"File not found: {path}"

        try:
            with open(path, 'r', encoding=encoder) as f:
                return [line.rstrip('\n') for line in f], ""
        except Exception as e:
            return "", f"Read error: {str(e)}"

    @staticmethod
    def _save_file(path: str, lines: list, encoder: str) -> str:
        """保存行列表到文件"""
        try:
            TextEditor._ensure_dir(path)
            with open(path, 'w', encoding=encoder) as f:
                f.write('\n'.join(lines))
            return ""
        except Exception as e:
            return f"Write error: {str(e)}"

    @staticmethod
    def _parse_line_keys(params: dict) -> list:
        """解析line1, line2...参数，返回有序内容列表"""
        line_items = []
        for key, value in params.items():
            if key.startswith('line'):
                try:
                    idx = int(key[4:])
                    line_items.append((idx, value))
                except ValueError:
                    continue  # 忽略无效行键

        if not line_items:
            return []

        # 按行号排序并填充空缺
        max_idx = max(idx for idx, _ in line_items)
        result = [''] * max_idx
        for idx, content in line_items:
            result[idx - 1] = content
        return result

    @staticmethod
    def _read(params: dict, path: str, create: bool, encoder: str) -> (str, str):
        # 加载文件
        lines, err = TextEditor._load_file(path, create, encoder)
        if err:
            return "", err

        # 处理读取参数
        show_number = params.get('number', True)
        if isinstance(show_number, str):
            show_number = show_number.lower() == 'true'

        max_lines = params.get('len')
        if max_lines is not None:
            try:
                max_lines = int(max_lines)
                lines = lines[:max_lines]
            except ValueError:
                pass  # 忽略无效长度

        # 构建输出
        output = []
        for i, line in enumerate(lines, 1):
            if show_number:
                output.append(f"{i}>>{line}")
            else:
                output.append(line)

        return '\n'.join(output), ""

    @staticmethod
    def _write(params: dict, path: str, create: bool, encoder: str) -> (str, str):
        new_lines = TextEditor._parse_line_keys(params)
        err = TextEditor._save_file(path, new_lines, encoder)
        return "", err

    @staticmethod
    def _change(params: dict, path: str, create: bool, encoder: str) -> (str, str):
        # 加载原文件
        lines, err = TextEditor._load_file(path, create, encoder)
        if err:
            return "", err

        # 解析修改内容
        changes = TextEditor._parse_line_keys(params)
        if not changes:
            return "", ""  # 无修改直接返回

        # 扩展文件行数到最大修改行
        max_line_needed = len(changes)
        if len(lines) < max_line_needed:
            lines.extend([''] * (max_line_needed - len(lines)))

        # 应用修改
        for i, content in enumerate(changes):
            if content:  # 只更新非空内容
                lines[i] = content

        # 保存并返回
        err = TextEditor._save_file(path, lines, encoder)
        return "", err

    @staticmethod
    def _append(params: dict, path: str, create: bool, encoder: str) -> (str, str):
        # 加载原文件
        lines, err = TextEditor._load_file(path, create, encoder)
        if err:
            return "", err

        # 解析追加内容并添加到末尾
        append_lines = TextEditor._parse_line_keys(params)
        lines.extend(append_lines)

        # 保存并返回
        err = TextEditor._save_file(path, lines, encoder)
        return "", err


if __name__ == "__main__":
    # 示例read操作
    read_params = {
        "type": "TextEditor",
        "pattern": "read",
        "path": "C:/AI-win11-Administrator/more_Types/type_TextEditor/test.txt",
        "number": "false"
    }

    # 示例write操作
    write_params = {
        "type": "TextEditor",
        "pattern": "write",
        "path": "C:/AI-win11-Administrator/more_Types/type_TextEditor/test.txt",
        "line1": "第一行内容",
        "line3": "第三行内容",
        "encoder": "utf-8"
    }

    stdout, stderr = TextEditor.execute(write_params)
    print("WRITE OPERATION:")
    print("stdout:", stdout)
    print("stderr:", stderr)

    stdout, stderr = TextEditor.execute(read_params)
    print("\nREAD OPERATION:")
    print("stdout:\n", stdout)
    print("stderr:", stderr)
