from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
请你尝试使用TextEditor的操作方法，读取README.md文件，并将其带有大量转义字符的几行抄写到test.txt。
'''
    language="Chinese"

    system = main_cycle(log_path=r"logs\log_ai.txt")
    system.cycle(language=language,max_rounds=100,msg=msg)

if __name__ =="__main__":
    work()