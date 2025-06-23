import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter,
                             QGroupBox, QStatusBar, QAction, QMenu, QMenuBar, QComboBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QTextCursor

from Control_Center import setting,status
from Control_Center import work_cycle,chat_cycle

def get_time():
    return str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]

# 主线程
class AIDesktopAssistant(QMainWindow):
    def __init__(self, setting, status):
        super().__init__()
        self.setting = setting
        self.status = status
        self.initUI()
        self.init_work_thread()
        self.init_chat_thread()

# ----------------------------------------------------------------------------------------------------------------------
    # 初始化窗口

    def initUI(self):
        # 设置主窗口
        self.setWindowTitle('AI桌面助手')
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowIcon(QIcon('ai_icon.png'))

        # 创建菜单栏
        self.createMenuBar()

        # 创建主控件
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 创建状态栏
        status_bar = self.statusBar()
        self.status_label = QLabel(
            f"状态: {'工作中' if self.status.exit == 0 else '聊天中'} | AI数量: {1 if self.status.single_or_dual == 1 else 2}")
        status_bar.addWidget(self.status_label)

        # 创建左右分割视图
        splitter = QSplitter(Qt.Horizontal)

        # 左侧面板 - 聊天/工作区
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # 聊天/工作显示区
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 10))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)

        # 用户输入区
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("输入消息...")
        self.user_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)

        self.send_button = QPushButton("发送")
        self.send_button.setFixedSize(80, 30)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.send_button.clicked.connect(self.sendMessage)

        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)

        left_layout.addWidget(self.chat_display)
        left_layout.addLayout(input_layout)
        left_panel.setLayout(left_layout)

        # 右侧面板 - 控制区
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)

        # 工作控制组
        work_group = QGroupBox("工作控制")
        work_layout = QVBoxLayout()

        self.start_work_button = QPushButton("开始工作")
        self.start_work_button.setStyleSheet("background-color: #6495ED; color: white;")
        self.start_work_button.clicked.connect(self.startWork)

        self.stop_work_button = QPushButton("开始聊天")
        self.stop_work_button.setStyleSheet("background-color: #6495ED; color: white;")
        self.stop_work_button.clicked.connect(self.startChat)
        self.stop_work_button.setEnabled(False)

        self.add_comment_button = QPushButton("添加工作留言")
        self.add_comment_button.setStyleSheet("background-color: #6495ED; color: white;")
        self.add_comment_button.clicked.connect(self.addWorkComment)
        self.add_comment_button.setEnabled(True)

        work_layout.addWidget(self.start_work_button)
        work_layout.addWidget(self.stop_work_button)
        work_layout.addWidget(self.add_comment_button)
        work_group.setLayout(work_layout)

        # AI控制组
        ai_group = QGroupBox("AI控制")
        ai_layout = QVBoxLayout()

        ai_count_label = QLabel("AI数量:")

        self.ai_count_combo = QComboBox()
        self.ai_count_combo.addItem("1个AI")
        self.ai_count_combo.addItem("2个AI")
        self.ai_count_combo.setCurrentIndex(0 if self.status.single_or_dual == 1 else 1)
        self.ai_count_combo.currentIndexChanged.connect(self.changeAICount)

        self.ai_status_label = QLabel(f"当前: {1 if self.status.single_or_dual == 1 else 2}个AI")

        ai_layout.addWidget(ai_count_label)
        ai_layout.addWidget(self.ai_count_combo)
        ai_layout.addWidget(self.ai_status_label)
        ai_group.setLayout(ai_layout)

        # 系统信息组
        sys_group = QGroupBox("系统信息")
        sys_layout = QVBoxLayout()

        self.model_label = QLabel(f"模型: {self.setting.test_model}")
        self.temp_label = QLabel(f"生成自由度: {self.setting.temperature}")
        self.lang_label = QLabel(f"语言: {self.setting.language}")
        self.user_label = QLabel(f"用户: {self.setting.user}")

        sys_layout.addWidget(self.model_label)
        sys_layout.addWidget(self.temp_label)
        sys_layout.addWidget(self.lang_label)
        sys_layout.addWidget(self.user_label)
        sys_group.setLayout(sys_layout)

        right_layout.addWidget(work_group)
        right_layout.addWidget(ai_group)
        right_layout.addWidget(sys_group)
        right_panel.setLayout(right_layout)

        # 添加左右面板到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 300])

        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 添加初始消息
        self.addMessage("系统", "AI桌面助手已启动", "system")


    def createMenuBar(self):
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        exit_action = QAction(QIcon('exit.png'), '退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menubar.addMenu('视图')

        dark_mode_action = QAction('深色模式', self, checkable=True)
        dark_mode_action.triggered.connect(self.toggleDarkMode)
        view_menu.addAction(dark_mode_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

    def addMessage(self, sender, message, msg_type="user"):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)

        # 根据消息类型设置样式
        if msg_type == "system":
            color = "#6A5ACD"  # 紫色
            prefix = "[系统] "
        elif msg_type == "executor":
            color = "#1E90FF"  # 蓝色
            prefix = "[执行者] "
        elif msg_type == "supervisor":
            color = "#32CD32"  # 绿色
            prefix = "[监查者] "
        elif msg_type == "output":
            color = "#FF8C00"  # 橙色
            prefix = "[输出] "
        elif msg_type == "error":
            color = "#FF4500"  # 红色
            prefix = "[错误] "
        else:
            color = "#000000"  # 黑色
            prefix = "[用户] "

        # 添加消息到聊天框
        self.chat_display.setTextColor(QColor(color))
        self.chat_display.setFontWeight(QFont.Bold)
        self.chat_display.insertPlainText(prefix)

        self.chat_display.setFontWeight(QFont.Normal)
        self.chat_display.setTextColor(QColor("#333333"))
        self.chat_display.insertPlainText(message + "\n\n")

        # 滚动到底部
        self.chat_display.ensureCursorVisible()

    def init_work_thread(self):
        """初始化工作线程并连接信号"""
        self.work_thread = work_cycle()
        self.work_thread.send_status(self.setting, self.status)

        # 连接工作线程的信号到主窗口的槽函数
        self.work_thread.Round_num.connect(self.update_round_num)
        self.work_thread.executor_output.connect(self.update_executor_output)
        self.work_thread.supervisor_output.connect(self.update_supervisor_output)
        self.work_thread.system_stdout.connect(self.update_system_stdout)
        self.work_thread.system_stderr.connect(self.update_system_stderr)
        self.work_thread.work_exit.connect(self.thread_exited)
        self.work_thread.Setting.connect(self.update_settings)

    def init_chat_thread(self):
        """初始化工作线程并连接信号"""
        self.chat_thread = chat_cycle()
        self.work_thread.send_status(self.setting, self.status)

        # 连接工作线程的信号到主窗口的槽函数
        self.chat_thread.Round_num.connect(self.update_round_num)
        self.chat_thread.executor_output.connect(self.update_executor_output)
        self.chat_thread.supervisor_output.connect(self.update_supervisor_output)
        self.chat_thread.system_stderr.connect(self.update_system_stderr)
        self.chat_thread.work_exit.connect(self.thread_exited)
        self.chat_thread.Setting.connect(self.update_settings)

        # 初始化为聊天模式
        self.status.exit=1
        self.chat_thread.send_status(self.setting,self.status)
        self.chat_thread.start()

# ----------------------------------------------------------------------------------------------------------------------
    # 主线程对工作线程的控制

    def startWork(self):
        self.status_label.setText(f"状态: 即将开始工作 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")
        self.chat_thread.Exit()

    def startChat(self):
        self.status_label.setText(f"状态: 即将开始聊天 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")
        self.work_thread.Exit()


    def addWorkComment(self):
        """添加工作留言到工作线程"""
        message = self.user_input.text().strip()
        if message:
            self.addMessage("用户", f"[工作留言]{message}")
            self.user_input.clear()

            self.work_thread.add_msg(f"{get_time()}{message}")

    def changeAICount(self, index):
        self.status.single_or_dual = 1 if index == 0 else 2
        self.ai_status_label.setText(f"当前: {index + 1}个AI")
        self.status_label.setText(f"状态: {'工作中' if self.status.exit == 0 else '聊天中'} | AI数量: {index + 1}")

        self.work_thread.num_AI()
        self.chat_thread.num_AI()

    def sendMessage(self):
        message = f"({get_time()}){self.user_input.text().strip()}"
        if message:
            self.addMessage("用户", message)
            self.user_input.clear()

            self.chat_thread.send_user_msg(message)


# ----------------------------------------------------------------------------------------------------------------------
    # 线程对主线程的控制
    def update_round_num(self, round_num):
        """更新轮次显示"""
        self.status_label.setText(
            f"状态:  轮次: {round_num} | AI数量: {1 if self.status.single_or_dual == 1 else 2}")

    def update_executor_output(self, output):
        """更新执行者输出"""
        self.addMessage("执行者", output, "executor")

    def update_supervisor_output(self, output):
        """更新监察者输出"""
        self.addMessage("监察者", output, "supervisor")

    def update_system_stdout(self, output):
        """更新系统标准输出"""
        self.addMessage("系统输出", output, "output")

    def update_system_stderr(self, output):
        """更新系统错误输出"""
        self.addMessage("系统错误", output, "error")

    def thread_exited(self, exit_code):
        self.status.exit = exit_code

        if exit_code == 1:
            print("to 1")
            self.chat_thread.send_status(self.setting, self.status)
            self.chat_thread.start()

            self.start_work_button.setEnabled(True)
            self.send_button.setEnabled(True)
            self.stop_work_button.setEnabled(False)
            self.addMessage("系统", "工作已停止，进入聊天状态", "system")
            self.status_label.setText(f"状态: 聊天中 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")

        if exit_code == 0:
            print("to 0")
            self.work_thread.send_status(self.setting, self.status)
            self.work_thread.start()

            self.send_button.setEnabled(False)
            self.start_work_button.setEnabled(False)
            self.stop_work_button.setEnabled(True)
            self.addMessage("系统", "聊天已中断，进入工作状态", "system")
            self.status_label.setText(f"状态: 工作中 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")

    def update_settings(self, settings):
        """更新设置"""
        self.setting = settings

# ----------------------------------------------------------------------------------------------------------------------
    # 其他功能
    # 深色模式
    def toggleDarkMode(self, checked):
        if checked:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.setPalette(palette)
        else:
            # 浅色模式
            QApplication.setPalette(QApplication.style().standardPalette())

    def showAbout(self):
        self.addMessage("系统", "AI桌面助手 v1.0\n基于Python和PyQt5开发\n提供AI辅助工作和聊天功能", "system")

    def closeEvent(self, event):
        # 停止工作线程
        self.setting.close()

        if self.work_thread.isRunning():
            self.work_thread.terminate()
            self.work_thread.wait()

        # 停止聊天线程
        if self.chat_thread.isRunning():
            self.chat_thread.terminate()
            self.chat_thread.wait()

        self.work_thread

        # 接受关闭事件
        event.accept()

if __name__ == '__main__':
    # 示例设置和状态
    app_setting = setting()
    app_status = status()

    app = QApplication(sys.argv)
    ex = AIDesktopAssistant(app_setting, app_status)
    ex.show()
    sys.exit(app.exec_())