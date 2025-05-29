from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
我想测试一下写入长文本时是否正常，主文件夹中有项目的副本以及介绍(主文件夹的代码正在运行，无法读取)，通过读取这些信息，生成一个更详细视角效果更好的README.md。
另外，直接读取文件时会导致中文字符串乱码，可能需要使用 -Encoding utf8后缀。
在你进行操作期间，开发者无法向你传递任何指令，当你遭遇不可解决的报错，请创建一个文件并记录。
'''

    xxx = main_cycle(log_path=r"logs\log_ai.txt")
    xxx.cycle(max_rounds=30,msg=msg)

if __name__ =="__main__":
    work()