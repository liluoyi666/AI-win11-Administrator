
# Developer Guide: Adding More Operation Types for AI

**[<u>跳转到中文版</u>](#开发者指南-为AI开发更多的操作类型)**

**This folder provides AI administrators with additional operation types beyond the system defaults. If you wish to enable AI administrators to perform more complex operations, follow this tutorial to develop more useful operation types.**

## Development Requirements:
### Naming:

- Your ***type*** must not conflict with existing types. ***Currently available: [powershell, read_log, exit, TextEditor]***
- Must not exclude the ***add_log*** key

### Input and Output:

- Input must be a single ***dict*** type containing all information expressed by the AI
- Must always return two strings: ***stdout*** and ***stderr***

### Notes:

- Ensure clean and manageable file structure
- Ensure input/output formats comply with specifications
- Your operation manual must be understandable by AI
- If the feature uses independent threads, must implement a close() method

## Development Process:

### 1. Create a package named ***type_YourType*** in the [<u>***more_Types***</u>]() directory
### 2. Implement your operation method in ***type_YourType*** - [<u>***See Example***</u>](type_TextEditor/code.py)
### 3. Name your operation type and design an AI operation manual - [<u>***See Example***</u>](type_TextEditor/params.py)
### 4. Register the operation name, manual, and function/class in your package's [<u>***type_YourType/\_\_init\_\_.py***</u>](type_TextEditor/__init__.py):
```python
from .params import Name_TextEditor, TextEditor_user_manual
from .code import TextEditor

__all__ = (Name_TextEditor, TextEditor_user_manual, TextEditor)
#           Name               Usage Guide             Class Body
```
### 5. Register them in [<u>***more_Types/\_\_init\_\_.py***</u>](__init__.py):
```python
from .type_TextEditor import Name_TextEditor, TextEditor_user_manual, TextEditor

__all__ = (Name_TextEditor, TextEditor_user_manual, TextEditor)
#           Name               Usage Guide             Class Body
```
### 6. Import these three elements in the project's main file [<u>***main_cycle.py***</u>](../dustbin/main_cycle_dual.py):
```python
from brain import log

from more_Types import Name_TextEditor, TextEditor_user_manual, TextEditor
# -> Import here

class main_cycle:
    def __init__(self, user='wqws', model_name="deepseek-coder", log_path=r"logs\log_ai.txt"):
```

### 7. Around line 57 of [<u>***main_cycle.py***</u>](../dustbin/main_cycle_dual.py), add your operation method to the dictionary. Ensure the value is a function or class method, not the class itself:
```python
    def cycle(self,language,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True):

        method = {}
        method["powershell"] = self.powershell.execute_command
        method["read_log"] = self.log.read
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute
        # -> Add here. Key is name, value is function/class method (no parentheses)
        
        grammar= grammar + TextEditor_user_manual
```

### 8. Around line 59 of [<u>***main_cycle.py***</u>](../dustbin/main_cycle_dual.py), concatenate your operation manual to the AI prompt:
```python
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute
        
        grammar= grammar + TextEditor_user_manual # -> Concatenate here using "+"
        
        while True:
            self.round_num+=1 
```

### 9. Once everything is ready, you can start running the system.

For further questions, please contact the project initiator.
# --------------------------------------------------------------------------------------------------------------------------------

<a id="开发者指南-为AI开发更多的操作类型"></a>
# 开发者指南: 为AI开发更多的操作类型

**[<u>Jump to Chinese Version</u>](#developer-guide-adding-more-operation-types-for-ai)**

**本文件夹将为AI管理员提供除系统自带操作类型的更多操作类型，如果你希望让AI管理员完成更复杂的操作，可以查看该教程，为他开发更有用的操作类型。**

## 开发要求：
### 命名:

- 你的***type***不能与已有的相同，***目前已有[powershell,read_log,exit,TextEditor]***
- 不能排斥***add_log***键

### 输入与输出：

- 输入只能为一个***dict***类型，AI表达所有信息都包含在里面
- 任何情况下必须返回两个字符串:***stdout***和***stderr***

### 注意：

- 需确保文件结构整齐，易于管理
- 需确保输入输出格式符合规定
- 你的操作手册必须确保AI能够看懂
- 如果该功能有独立线程，必须有close()方法

## 开发流程：

### 1. 在[<u>***more_Types***</u>]()目录下创建名为***type_YourType***的软件包
### 2. 在***type_YourType***中实现你的操作方法-[<u>***点击查看示例***</u>](type_TextEditor/code.py)
### 3. 为你的操作类型命名，并为AI设计一个操作手册-[<u>***点击查看示例***</u>](type_TextEditor/params.py)
### 4. 将操作类型名称，操作手册，函数或类注册在你的软件包的 [<u>***type_YourType/\_\_init\_\_.py***</u>](type_TextEditor/__init__.py)中:
```python
from .params import Name_TextEditor,TextEditor_user_manual
from .code import TextEditor

__all__ = (Name_TextEditor,TextEditor_user_manual,TextEditor)
#           名称              使用指南                类本体
```
### 5. 再将他们注册到[<u>***more_Types/\_\_init\_\_.py***</u>](__init__.py)中:
```python
from .type_TextEditor import Name_TextEditor,TextEditor_user_manual,TextEditor

__all__ = (Name_TextEditor,TextEditor_user_manual,TextEditor)
#           名称              使用指南                类本体
```
### 6. 在项目主文件夹的 [<u>***main_cycle.py***</u>](../dustbin/main_cycle_dual.py)中导入这三个元素:
```python
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor
# ->就是在这里

class main_cycle:
    def __init__(self,user='wqws',model_name="deepseek-coder",log_path=r"logs\log_ai.txt"):
```

### 7. 大概在[<u>***main_cycle.py***</u>](../dustbin/main_cycle_dual.py)第57，将你的操作方法添加到字典中，请确保在字典中的是一个函数或类的方法，而不是类本体:
```python
    def cycle(self,language,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True):

        method = {}
        method["powershell"] = self.powershell.execute_command
        method["read_log"] = self.log.read
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute
        # ->就是在这里，key是名字，value是函数或类的方法，请不要保留函数或方法的括号
        
        grammar= grammar + TextEditor_user_manual
```

### 8. 大概在[<u>***main_cycle.py***</u>](../dustbin/main_cycle_dual.py)第59行，把你的操作手册连接在给AI的提示词后面:
```python
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute
        
        grammar= grammar + TextEditor_user_manual  # ->就是这里，使用"+"连接你的操作手册
        
        while True:
            self.round_num+=1

```

### 9. 在一切准备就绪之后，你就可以开始运行了。

如果有更多疑惑，请尝试联系项目的发起者。
