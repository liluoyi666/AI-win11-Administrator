from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
我想测试一下，写入文件在什么情况下可以正确显示换行，什么时候命令行中会出现连续的>>标记。
请你在test.txt中记录换行方式(双反斜n，单反斜n，`n，反斜杠r，直接回车)，是否正确显示换行，输入时命令行是否出现连续>>。
测试时输入line1到line5,并记录为一个表格。
另外，直接读取文件时会导致中文字符串乱码，可能需要使用 -Encoding utf8后缀。
在你进行操作期间，开发者无法向你传递任何指令，当你遭遇不可解决的报错，请创建一个文件并记录。
'''

    xxx = main_cycle(log_path=r"logs\log_ai.txt")
    xxx.cycle(max_rounds=30,msg=msg)

if __name__ =="__main__":
    work()