"""
以下为通用字符串
"""

# 监察者语法
supervisor_grammar=r"""
<输出结构>
```json{
    "confirm": "True",
    "to_executor" : "对执行者的话",
    "add_log": "执行操作时顺便写入日志"
}```
confirm必须存在
confirm应为"True"或"False"，注意大写，该值为字符串而不是布尔值。
</输出结构>
"""


# 执行者语法
executor_grammar = r"""
<注意>
.你的输入必须是markdown中的json格式
.json中bool型首字母无需大写，且无需双引号包裹
.禁止执行未经安全验证的文件
.powershell默认使用gbk编码，注意使用 -Encoding utf8避免中文乱码
.在你进行操作期间，开发者无法向你传递任何指令，当你遭遇不可解决的报错，请记录
.请不要忘记安全大于一切
</注意>

<输出结构>
```json{
    "type": "操作类型",
    ...,  
    "add_log": "执行操作时顺便写入日志"
}```
你的一次输入中可以包含多个该json结构，系统会按顺序执行这些json中的指令，需要确保每个json块分别被单独的```json```包裹。
你的输入一个输入中如果包含n个json，系统会给你一次性给你返回这n个json的执行结果，避免一次性输入前后因果关联较强的命令，否则可能出现连环报错。
任何情况下都必须存在type键，其他键具体由type决定。
add_log不存在不影响操作执行，add_log存在也不会影响任何类型的操作。记入日志时会自动添加时间以及换行，无需手动添加。日志文件由系统自动维护。
</输出结构>

<本系统自带操作类型>
    <powershell>
    {
        "type": "powershell",
        "command": "你要执行的命令"
    }
    powershell的状态会一直保存，确保你可以执行有前后关联的命令。
    
    {
        "type": "powershell",
        "restart": true
    }
    当由于长耗时命令或出现连续的>>标记等原因，导致powershell无法使用，可使用该方法重置powershell
    </powershell>

    </read_log>
    {
        "type": "read_log",
        "start": x,
        "end":y
    }
    以行为单位，输出为log[x:y]，如果start不存在则默认为0，如果end不存在则默认为max_len，且都可为负数。
    </read_log>

    <exit>
    {
        "type": "exit",
        "confirm": true
    }
    退出工作状态，进入聊天状态，如果完成了所有任务请使用该指令。
    </exit>
</本系统自带操作类型>
"""


# json解析失败返回信息
error_msg=r"""
json解析失败，请重新编辑。
建议检查转义与换行是否正确，如果输入过于复杂，请尝试分布操作。
如果写入多行文本，建议使用拓展操作类型。
请不要缺失必须键。
注意使用```json···```包裹json，以方便检测。
"""

single_ai=r"""
当前监察者为非工作状态。
系统会直接执行你的指令，请注意安全。
"""