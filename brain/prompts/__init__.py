from .String_Templates_double import executor_system_prompt,executor_grammar,executor_user_msg,error_msg
from .String_Templates_double import supervisor_system_prompt,supervisor_user_msg,supervisor_grammar

from .String_Templates_single import system_prompt, grammar, user_msg

__all__ = ( executor_system_prompt,executor_grammar,executor_user_msg,error_msg,    # 执行者提示词
            supervisor_system_prompt,supervisor_user_msg,supervisor_grammar,        # 监察者提示词
            system_prompt, grammar, user_msg)                                       # 单AI模式提示词