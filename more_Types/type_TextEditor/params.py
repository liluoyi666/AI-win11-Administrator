
TYPE = "TextEditor"

TextEditor_user_manual=r"""
<扩展操作类型:TextEditor>
    <介绍>
    本操作类型名为TextEditor。
    可帮助你便捷地编写文本及代码文件。提供可视化效果较好的写入，追加，读取方法，以及较便捷的修改文件方式。
    使用该方法可以避免换行符的错误。
    </介绍>
    
    <read>
    {
        "type": "TextEditor",   
        "pattern": "read",       
        "create": "False",      # 默认为False，True表示文件不存在则创建   
        "path":"xxx",           # 绝对路径
        "number": "True",       # 是否显示每一行的编号，无该键则默认为true 
        "len": 10,              # 读取多少行，无该键或没这么多行可读则默认读取所有
        "encoder": "utf-8"      # 无该键则默认utf-8
    }
    如果"number": "True"，则输出:
    1>> 你还好吗？
    2>> 是的，我很好，怎么了。
    3>> 没什么。
    如果为"False"则无编号和>>。
    </read>
    
    <write>
    {
        "type": "TextEditor",   
        "pattern": "write",
        "create": "False",          # 默认为False，True表示文件不存在则创建
        "path": "xxx",              # 绝对路径
        "line1": "你还好吗？",
        "line2": "是的，我很好。",
        "line3": "",                # 可为空双引号
        ...
        "line10": "再见。",
        "line13": "祝你好运。",       # 此处跳过"line11"和"line12"键，则跳过的键默认为空双引号
        "encoder": "utf-8"          # 无该键则默认utf-8
    }
    每个数字键代表一行，你无需手动使用换行符。
    该方法完全覆盖原文件。
    </write>
    
    <change>
        {
        "type": "TextEditor",   
        "pattern": "change",
        "create": "False",          # 默认为False，True表示文件不存在则创建
        "path": "xxx",              # 绝对路径
        "line2": "嗯，我并不好。",     # 覆盖原本这一行
        "line11": "下次再见。",
        "line12": "祝你好运。",
        "line15": "。。。",          # 该行原本不存在，则添加该行。14行也不存在且被跳过，则默认为空双引号。
        "encoder": "utf-8"
        }
    使用该方法仅覆盖指定的行，未指定的行则保持。如果指定了未存在的行，则创建该行。
    该方法的行与read方法的行标签一一对应，可搭配使用。
    </change>
    
    <append>
        {
        "type": "TextEditor",   
        "pattern": "append",
        "create": "False",          # 默认为False，True表示文件不存在则创建
        "path": "xxx",              # 绝对路径
        "line1": "很多天后:",         # 将此处的第一行追加到文件的最后一行
        "line3": "欸？你还好吗。",     # 同样遵循跳过则为空双引号
        "line4": "当然。",
        "encoder": "utf-8"
        }
    该方法会将line1连接到文件的尾部，实现灵活的多行或单行追加功能。
    </append>
    
</扩展操作类型:TextEditor>
"""

