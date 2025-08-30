from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QRadioButton, QButtonGroup, QPushButton)

class ThemeSettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("테마 설정 화면")

        layout = QVBoxLayout()

        # 테마 선택 라디오 버튼
        self.light_mode_button = QRadioButton("라이트 모드")
        self.dark_mode_button = QRadioButton("다크 모드")

        self.theme_group = QButtonGroup()
        self.theme_group.addButton(self.light_mode_button)
        self.theme_group.addButton(self.dark_mode_button)

        layout.addWidget(self.light_mode_button)
        layout.addWidget(self.dark_mode_button)

        # 저장 버튼
        self.save_button = QPushButton("저장")
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
