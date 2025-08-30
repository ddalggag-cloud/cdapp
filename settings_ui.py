from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFormLayout, QComboBox, QTextEdit)

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("설정 화면")

        layout = QFormLayout()

        # SMTP 설정
        self.smtp_server_input = QLineEdit()
        self.smtp_port_input = QLineEdit()
        self.smtp_user_input = QLineEdit()
        self.smtp_password_input = QLineEdit()
        self.smtp_password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("SMTP 서버:", self.smtp_server_input)
        layout.addRow("포트:", self.smtp_port_input)
        layout.addRow("사용자 이름:", self.smtp_user_input)
        layout.addRow("비밀번호:", self.smtp_password_input)

        # 수신자 이메일 설정
        self.recipients_input = QTextEdit()
        layout.addRow("수신자 이메일 (쉼표로 구분):", self.recipients_input)

        # 저장 버튼
        self.save_button = QPushButton("저장")
        layout.addRow(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
