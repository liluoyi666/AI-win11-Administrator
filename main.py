from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
我开发了一个名为TextEditor的操作方法，并发现一次性写入大量文本时，会出现json解析失败的情况。
请你读取README.md，分别测试将不同的行抄写到test.txt。以此测试到底是什么东西导致json解析失败
似乎和转义字符有关，注意尝试转义字符多的行，也可能与特殊字符有关
'''

    msg1 = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
我开发了一个名为TextEditor的操作，请你根据介绍语法，测试这个操作类型。
我想测试一下该功能，请你使用该模块读取README.md的中文版信息，并写入到一个叫test.md的文件中，并逐步测试其他功能。
'''

    system = main_cycle(log_path=r"logs\log_ai.txt")
    system.cycle(max_rounds=100,msg=msg)

if __name__ =="__main__":
    work()