from .String_Templates_double import executor_system_prompt,executor_user_msg
from .String_Templates_double import supervisor_system_prompt,supervisor_user_msg

from .String_Templates_single import system_prompt, user_msg

from .String_public import  executor_grammar,supervisor_grammar,error_msg

__all__ = ( executor_system_prompt, executor_user_msg,          # 执行者提示词
            supervisor_system_prompt, supervisor_user_msg,      # 监察者提示词
            system_prompt, user_msg,                            # 单AI模式提示词
            supervisor_grammar, executor_grammar, error_msg     # 通用字符串
            )