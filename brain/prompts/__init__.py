from .String_Templates import executor_system_prompt,executor_user_msg
from .String_Templates import supervisor_system_prompt,supervisor_user_msg

from .String import  executor_grammar,supervisor_grammar,error_msg,single_ai

__all__ = ( executor_system_prompt, executor_user_msg,                      # 执行者提示词
            supervisor_system_prompt, supervisor_user_msg,                  # 监察者提示词
            supervisor_grammar, executor_grammar, error_msg, single_ai      # 通用字符串
            )