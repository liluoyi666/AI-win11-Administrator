from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
你当前能进行的网络操作有哪些，请演示一下。
'''
    language="Chinese"

    system = main_cycle(log_path=r"logs\log_ai.txt")
    system.cycle(language=language,max_rounds=100,msg=msg)

if __name__ =="__main__":
    work()