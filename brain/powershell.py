import subprocess
import threading
import queue
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import uuid


class PowerShellSession:
    def __init__(self):
        self.process = None
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.lock = threading.Lock()  # 线程锁防止并发冲突
        self._initialize_session()  # 初始化会话

    # 初始化或重新初始化会话
    def _initialize_session(self):
        self._cleanup_existing_process()  # 清理现有进程
        self.stdout_queue = queue.Queue()  # 重置输出队列
        self.stderr_queue = queue.Queue()  # 重置错误队列
        self._start_process()  # 启动新进程
        self._start_output_reader()  # 启动输出读取线程

    # 清理现有进程
    def _cleanup_existing_process(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                self.process.wait(timeout=3)
            except Exception as e:
                print(f"清理进程时出错: {e}")
            finally:
                if self.process.poll() is None:
                    self.process.terminate()

    # 生成powershell类
    def _start_process(self):
        self.process = subprocess.Popen(
            ['powershell.exe', '-NoExit'],
            stdin=subprocess.PIPE,  # 输入通道
            stdout=subprocess.PIPE,  # 输出通道
            stderr=subprocess.PIPE,  # 错误通道
            text=True,
            bufsize=1,
            universal_newlines=True
        )

    # 输出读取线程
    def _start_output_reader(self):
        # 定义一个用于读取的函数
        def reader(queue, stream):
            while True:
                try:
                    line = stream.readline()
                except Exception as e:
                    line = f'<读取powershell时，该行出现错误[{e}]>'
                if not line:  # 流关闭时退出循环
                    break
                queue.put(line)

        # 定义两个保护进程，并启动
        threading.Thread(target=reader, args=(self.stdout_queue, self.process.stdout), daemon=True).start()
        threading.Thread(target=reader, args=(self.stderr_queue, self.process.stderr), daemon=True).start()

    # 重启PowerShell会话
    def restart_session(self):
        with self.lock:
            self._initialize_session()
            return "PowerShell会话已重启", ""

    def execute_command(self, command_dict, timeout=30):
        # 检查是否需要重启
        if command_dict.get("restart", False):
            return self.restart_session()

        with self.lock:  # 确保命令顺序执行
            if self.process.poll() is not None:  # 如果进程不存在
                raise RuntimeError("PowerShell process is not running")

            command = command_dict["command"]
            if command == 'exit':
                self.close()
                return "会话已关闭", ""

            end_marker = str(uuid.uuid4())
            start_time = time.time()
            beijing_time = datetime.now(ZoneInfo("Asia/Shanghai"))
            full_cmd = f'''{command}\n
'''  # 请不要修改此处的换行
            # 组合命令
            self.process.stdin.write(full_cmd)  # 输入
            self.process.stdin.write(f"# 以上输出源于({beijing_time})开始执行的命令'{end_marker}'\n")
            self.process.stdin.flush()

            output = []
            while True:
                try:
                    line = self.stdout_queue.get(timeout=10)
                    output.append(line.strip())
                    if end_marker in line:
                        break

                except queue.Empty:
                    if time.time() - start_time > timeout:
                        output.append(
                            f"超出{timeout}秒未获得新的输出，若执行了长耗时指令，在该指令完成之前若继续输入新的指令，后续指令加入队列。")
                        break

            # 读取错误流中的内容
            stderr_output = []
            while not self.stderr_queue.empty():
                stderr_output.append(self.stderr_queue.get().strip())
            return '\n'.join(output), '\n'.join(stderr_output)

    def close(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                self.process.wait(timeout=5)
            except:
                self.process.terminate()


if __name__ == "__main__":
    powershell = PowerShellSession()
    try:
        # 正常执行命令
        result, err = powershell.execute_command({"command": "echo 'Hello World'"})
        print("1:\n", result)

        # 重启会话
        result, err = powershell.execute_command({"restart": True})
        print("2:\n", result)

        # 重启后执行新命令
        result, err = powershell.execute_command({"command": "Get-Date"})
        print("3:\n", result)

        # 创建文件的长耗时操作
        result, err = powershell.execute_command({
                                                     "command": '''Set-Content -Path SimpleRNN.py -Value \"import torch\nimport torch.nn as nn\n\nclass SimpleRNN(nn.Module):\n    def __init__(self, input_size, hidden_size, num_layers, num_classes):\n        super(SimpleRNN, self).__init__()\n        self.hidden_size = hidden_size\n        self.num_layers = num_layers\n        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)\n        self.fc = nn.Linear(hidden_size, num_classes)\n    \n    def forward(self, x):\n        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)\n        out, _ = self.rnn(x, h0)\n        out = self.fc(out[:, -1, :])\n        return out\" -Encoding utf8'''})
        print("4:\n", result)

        # 再次重启会话
        result, err = powershell.execute_command({"restart": True})
        print("5:\n", result)

        # 验证新会话是否正常工作
        result, err = powershell.execute_command({"command": "ls"})
        print("6:\n", result)

    finally:
        powershell.close()