# *开发者指南: 为AI开发更多的操作类型*

**本文件夹将为AI管理员提供除系统自带操作类型的更多操作类型，如果你希望让AI管理员完成更复杂的操作，可以查看该教程，为他开发更有用的操作类型。**

## 开发要求：
### 命名:

- 你的***type***不能与已有的相同，***目前已有[powershell,read_log,exit,TextEditor]***
- 不能排斥***add_log***键

### 输入与输出：

- 输入只能为一个***dict***类型
- 任何情况下必须返回两个字符串:***stdout***和***stderr***

### 注意：

- 需确保代码格式符合要求
- 语法介绍能让AI理解
- 如果该功能有独立线程，必须有close()方法

## 开发流程：

1. 在***more_Types***目录下创建名为***type_YourType***的软件包
2. 在***type_YourType***中实现你的操作方法-[<u>***点击查看示例***</u>](type_TextEditor/code.py)
3. 为你的操作类型命名，并为AI设计一个操作手册-[<u>***点击查看示例***</u>](type_TextEditor/params.py)
4. 将操作类型名称，操作手册，函数或类注册在你的软件包的 [<u>***\_\_init\_\_.py***</u>](type_TextEditor/__init__.py)中:
```python
from .params import Name_TextEditor,TextEditor_user_manual
from .code import TextEditor

__all__ = (Name_TextEditor,TextEditor_user_manual,TextEditor)
#           名称              使用指南                类本体
```
5. 再将他们注册到[<u>***more_Types/\_\_init\_\_.py***</u>](__init__.py)中:
```python
from .type_TextEditor import Name_TextEditor,TextEditor_user_manual,TextEditor

__all__ = (Name_TextEditor,TextEditor_user_manual,TextEditor)
#           名称              使用指南                类本体
```
6. 在项目主文件夹的 [<u>***main_cycle.py***</u>](../main_cycle.py)中导入这三个元素:
```python
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor
# ->就是在这里

class main_cycle:
    def __init__(self,user='wqws',model_name="deepseek-coder",log_path=r"logs\log_ai.txt"):
```

7. 大概在第40，将你的操作方法添加到字典中:
```python
    def cycle(self,language,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True):

        method = {}
        method["powershell"] = self.powershell.execute_command
        method["read_log"] = self.log.read
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute
        # ->就是在这里，key是名字，value是操作的函数
        
        while True:
```

8. 大概在第57行，把你的操作手册连接在给AI的提示词后面:
```python
            system_msg = system_prompt.format(
                user= self.user,
                language=language,
                Time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
                num=self.round_num,
                msg=msg
            ) + grammar + TextEditor_user_manual# ->就是这里，使用"+"连接你的操作手册

            cmd_output = user_msg.format(
                stdout= self.stdout,
```

9. 在一切准备就绪之后，你就可以开始运行了。