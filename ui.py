from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QSettings, QTimer, QDateTime, QTime
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
                           QLineEdit, QFormLayout, QComboBox, QTextEdit, QRadioButton, 
                           QButtonGroup, QTabWidget, QListWidget, QHBoxLayout, QMessageBox,
                           QSystemTrayIcon, QMenu, QStyle, QGroupBox, QGridLayout, QCheckBox,
                           QTimeEdit, QScrollArea)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from scheduler_ui import SchedulerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("스크린 캡처 및 이메일 전송 도구")
        
        # QSettings를 사용하여 설정 저장
        self.settings = QSettings("MyApp", "Settings")
        
        # 시스템 트레이 아이콘 설정
        self.create_tray_icon()
        
        # 프로그램 실행 상태
        self.is_running = False

        # QSettings를 사용하여 테마 설정 저장
        self.settings = QSettings("MyApp", "ThemeSettings")
        self.apply_saved_theme()

        # 탭 위젯 생성
        self.tabs = QTabWidget()

        # 메인 탭
        self.main_tab = QWidget()
        self.main_layout = QVBoxLayout()
        self.start_button = QPushButton("시작")
        self.stop_button = QPushButton("중지")
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.stop_button)
        self.main_tab.setLayout(self.main_layout)
        self.tabs.addTab(self.main_tab, "메인")

        # 설정 탭
        self.settings_tab = QWidget()
        self.settings_layout = QFormLayout()
        self.smtp_server_input = QLineEdit()
        self.smtp_port_input = QLineEdit()
        self.smtp_user_input = QLineEdit()
        self.smtp_password_input = QLineEdit()
        self.smtp_password_input.setEchoMode(QLineEdit.Password)
        self.settings_layout.addRow("SMTP 서버:", self.smtp_server_input)
        self.settings_layout.addRow("포트:", self.smtp_port_input)
        self.settings_layout.addRow("사용자 이름:", self.smtp_user_input)
        self.settings_layout.addRow("비밀번호:", self.smtp_password_input)
        self.save_settings_button = QPushButton("저장")
        self.settings_layout.addRow(self.save_settings_button)
        self.settings_tab.setLayout(self.settings_layout)
        self.tabs.addTab(self.settings_tab, "설정")

        # 받는 사람 이메일 탭
        self.recipients_tab = QWidget()
        self.recipients_layout = QVBoxLayout()
        self.recipients_list = QListWidget()
        self.add_recipient_input = QLineEdit()
        self.add_recipient_input.setPlaceholderText("이메일 주소 입력")
        self.add_recipient_button = QPushButton("추가")
        self.remove_recipient_button = QPushButton("삭제")

        # 버튼 이벤트 연결
        self.add_recipient_button.clicked.connect(self.add_recipient)
        self.remove_recipient_button.clicked.connect(self.remove_recipient)

        self.recipients_layout.addWidget(QLabel("받는 사람 목록"))
        self.recipients_layout.addWidget(self.recipients_list)

        add_remove_layout = QHBoxLayout()
        add_remove_layout.addWidget(self.add_recipient_input)
        add_remove_layout.addWidget(self.add_recipient_button)
        self.recipients_layout.addLayout(add_remove_layout)

        self.recipients_layout.addWidget(self.remove_recipient_button)
        self.recipients_tab.setLayout(self.recipients_layout)
        self.tabs.addTab(self.recipients_tab, "받는 사람")

        # 로그 탭
        self.log_tab = QWidget()
        self.log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.clear_log_button = QPushButton("로그 초기화")
        self.log_layout.addWidget(self.log_output)
        self.log_layout.addWidget(self.clear_log_button)
        self.log_tab.setLayout(self.log_layout)
        self.tabs.addTab(self.log_tab, "로그")

        # 테마 설정 탭
        self.theme_tab = QWidget()
        self.theme_layout = QVBoxLayout()
        self.light_mode_button = QRadioButton("라이트 모드")
        self.dark_mode_button = QRadioButton("다크 모드")
        self.theme_group = QButtonGroup()
        self.theme_group.addButton(self.light_mode_button)
        self.theme_group.addButton(self.dark_mode_button)
        self.theme_layout.addWidget(self.light_mode_button)
        self.theme_layout.addWidget(self.dark_mode_button)
        self.save_theme_button = QPushButton("저장")
        self.save_theme_button.clicked.connect(self.save_theme)
        self.theme_layout.addWidget(self.save_theme_button)
        self.theme_tab.setLayout(self.theme_layout)
        self.tabs.addTab(self.theme_tab, "테마 설정")

        # 스케줄 탭 추가
        self.scheduler_tab = QWidget()
        self.scheduler_layout = QVBoxLayout()

        # SchedulerWidget 인스턴스 생성
        self.scheduler_widget = SchedulerWidget()
        self.scheduler_layout.addWidget(self.scheduler_widget)

        self.scheduler_tab.setLayout(self.scheduler_layout)
        self.tabs.addTab(self.scheduler_tab, "스케줄")

        # 스케줄 저장 및 로드 연결
        self.scheduler_widget.add_button.clicked.connect(self.add_schedule)
        self.scheduler_widget.remove_button.clicked.connect(self.remove_schedule)
        self.load_saved_settings()

        # 메인 레이아웃에 탭 추가
        self.setCentralWidget(self.tabs)

    def save_theme(self):
        if self.light_mode_button.isChecked():
            self.settings.setValue("theme", "light")
            self.apply_light_theme()
        elif self.dark_mode_button.isChecked():
            self.settings.setValue("theme", "dark")
            self.apply_dark_theme()

    def apply_saved_theme(self):
        theme = self.settings.value("theme", "light")
        if theme == "light":
            self.apply_light_theme()
        elif theme == "dark":
            self.apply_dark_theme()

    def apply_light_theme(self):
        self.setStyleSheet("")  # 기본 스타일로 설정

    def apply_dark_theme(self):
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")

    def add_recipient(self):
        email = self.add_recipient_input.text().strip()
        if email:
            if "@" in email and "." in email:  # 간단한 이메일 형식 검사
                self.recipients_list.addItem(email)
                self.add_recipient_input.clear()
                self.save_recipients()
            else:
                QMessageBox.warning(self, "오류", "올바른 이메일 주소를 입력해주세요.")

    def remove_recipient(self):
        current_item = self.recipients_list.currentItem()
        if current_item:
            self.recipients_list.takeItem(self.recipients_list.row(current_item))
            self.save_recipients()

    def save_recipients(self):
        recipients = []
        for i in range(self.recipients_list.count()):
            recipients.append(self.recipients_list.item(i).text())
        self.settings.setValue("recipients", recipients)
        QMessageBox.information(self, "알림", "받는 사람 목록이 저장되었습니다.")

    def load_saved_settings(self):
        # 받는 사람 목록 불러오기
        recipients = self.settings.value("recipients", [])
        if recipients:
            self.recipients_list.clear()
            self.recipients_list.addItems(recipients)
            
        # 스케줄 목록 불러오기
        schedules = self.settings.value("schedules", [])
        if schedules:
            self.scheduler_widget.schedule_list.clear()
            self.scheduler_widget.schedule_list.addItems(schedules)
            
    def add_schedule(self):
        selected_days = []
        for checkbox in self.scheduler_widget.day_checkboxes:
            if checkbox.isChecked():
                selected_days.append(checkbox.text())

        if not selected_days:
            QMessageBox.warning(self, "오류", "요일을 선택해주세요.")
            return

        time = self.scheduler_widget.time_edit.time().toString("HH:mm")
        repeat = "매주 반복" if self.scheduler_widget.repeat_checkbox.isChecked() else "1회"
        schedule_text = f"{', '.join(selected_days)} {time} ({repeat})"

        self.scheduler_widget.schedule_list.addItem(schedule_text)
        self.save_schedules()

    def remove_schedule(self):
        current_item = self.scheduler_widget.schedule_list.currentItem()
        if current_item:
            self.scheduler_widget.schedule_list.takeItem(
                self.scheduler_widget.schedule_list.row(current_item)
            )
            self.save_schedules()

    def save_schedules(self):
        schedules = []
        for i in range(self.scheduler_widget.schedule_list.count()):
            schedules.append(self.scheduler_widget.schedule_list.item(i).text())
        self.settings.setValue("schedules", schedules)
        
    def check_schedule(self):
        if not self.is_running:
            return
            
        current_time = QDateTime.currentDateTime()
        current_day = ["월", "화", "수", "목", "금", "토", "일"][current_time.date().dayOfWeek() - 1]
        current_time_str = current_time.toString("HH:mm")
        
        for i in range(self.scheduler_widget.schedule_list.count()):
            schedule = self.scheduler_widget.schedule_list.item(i).text()
            days, time, repeat = self.parse_schedule(schedule)
            
            if current_day in days and current_time_str == time:
                self.capture_and_send_email()
                
                # 1회성 스케줄인 경우 삭제
                if repeat == "1회":
                    self.scheduler_widget.schedule_list.takeItem(i)
                    self.save_schedules()
                    break
                    
    def parse_schedule(self, schedule):
        # "월, 화, 수 14:30 (매주 반복)" 형식의 문자열 파싱
        parts = schedule.split(" ")
        days = parts[0].split(", ")
        time = parts[1]
        repeat = parts[2].strip("()")
        return days, time, repeat
        
    def capture_and_send_email(self):
        # TODO: 실제 화면 캡처 및 이메일 전송 구현
        self.log_output.append(f"[{QDateTime.currentDateTime().toString()}] 스케줄에 따라 화면 캡처 및 이메일 전송")
            
    def create_tray_icon(self):
        # 시스템 트레이 아이콘 생성
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # 트레이 메뉴 생성
        self.tray_menu = QMenu()
        self.show_action = self.tray_menu.addAction("설정 화면 열기")
        self.show_action.triggered.connect(self.show)
        self.tray_menu.addSeparator()
        self.quit_action = self.tray_menu.addAction("종료")
        self.quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
    def start_monitoring(self):
        self.is_running = True
        self.hide()  # 메인 창 숨기기
        self.tray_icon.show()  # 트레이 아이콘 표시
        self.tray_icon.showMessage(
            "스크린 캡처 도구",
            "프로그램이 백그라운드에서 실행 중입니다.",
            QSystemTrayIcon.Information,
            2000
        )
        
    def stop_monitoring(self):
        self.is_running = False
        self.show()  # 메인 창 보이기
        self.tray_icon.hide()  # 트레이 아이콘 숨기기
        
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            
    def quit_application(self):
        self.settings.sync()  # 설정 저장
        self.tray_icon.hide()
        self.close()
