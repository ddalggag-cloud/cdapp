from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton)

class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그 화면")

        layout = QVBoxLayout()

        # 로그 출력 영역
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # 로그 초기화 버튼
        self.clear_log_button = QPushButton("로그 초기화")
        layout.addWidget(self.clear_log_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
