from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
我想测试一下你视角中的反斜杠和我的区别，请你输入8个反斜杠和4个反斜杠分别继续write_out和写入test.txt中，并记录你输入的个数，在命令行中输出时的个数，在文件中写入的个数。
记住，是你在输入时的视角中的8个反斜杠和4个反斜杠
'''

    msg1 = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
我开发了一个名为TextEditor的操作，请你根据介绍语法，测试这个操作类型。
我想测试一下该功能，请你使用该模块读取README.md的中文版信息，并写入到一个叫test.md的文件中，并逐步测试其他功能。
'''

    system = main_cycle(log_path=r"logs\log_ai.txt")
    system.cycle(max_rounds=30,msg=msg)

if __name__ =="__main__":
    work()