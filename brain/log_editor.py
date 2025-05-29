"""
承担日志写入和读取功能
"""

class log:
    def __init__(self, filename):
        self.filename = filename
        self.buffer = []  # 缓存待写入的日志行

    def write(self, time, msg):
        content=f"[{time}]- {msg}"
        self.buffer.append(content + '\n')  # 自动添加换行符

    def read(self,json:dict):
        self.flush_buffer()
        start = 0
        end = None
        if "start" in json:
            start = json["start"]
        if "end" in json:
            end = json["end"]

        try:
            with open(self.filename, 'r',encoding="utf-8") as f:
                logs=f.read().split("\n")

                if end is None:
                    end =len(logs)

                logs=logs[start:end]
                return "".join(logs),""
        except FileNotFoundError:
            return "",'文件不存在或路径错误'

    def flush_buffer(self):
        if self.buffer:
            try:
                with open(self.filename, 'a',encoding="utf-8") as f:
                    f.writelines(self.buffer)
                self.buffer = []
            except Exception as e:
                print(f"写入日志文件失败: {e}")

    def __del__(self):
        self.flush_buffer()

if __name__ == "__main__":
    import time
    from datetime import datetime
    from zoneinfo import ZoneInfo
    Log=log("log.txt")
    Log.write(str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19],'你好')
    Log.write(str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19], '你在干嘛')
    Log.write(str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19], '???')
    Log.write(str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19], '你还好吗')
    print('1:',Log.read({"start":1,"end":-1}))
    print('2:',Log.read({"start":1}))
    print('3:',Log.read({"end":2}))
    Log.write(str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19], '什么鬼')
    time.sleep(30)