import sys
from PyQt5.QtWidgets import QApplication
from Control_Center import setting,status,AIDesktopAssistant,AIDesktopAssistant1
def run(user,language,model_name,system,debug):
    app_setting = setting(user=user,language=language,model_name=model_name,system=system,
                          stderr_print=debug,stdout_print=debug)
    app_status = status()
    app = QApplication(sys.argv)
    ex = AIDesktopAssistant1(app_setting, app_status)
    ex.show()
    sys.exit(app.exec_())

if __name__ =="__main__":
    debug=True                  # 会打印调试信息/Debug information will be print

    user = "wqws"               # 你的名字/Your name
    language="Zh"               # 语言/Language
    model_name="deepseek-chat"  # 模型名称/Model name
    system='win11'              # 电脑系统(只能win)/Computer system(only win)

    run(user,language,model_name,system,debug)