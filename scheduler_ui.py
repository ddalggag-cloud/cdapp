from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QTimeEdit, QListWidget, QCheckBox,
                           QGroupBox, QGridLayout, QFrame, QScrollArea, QMessageBox)
from PyQt5.QtCore import QTime, Qt
from PyQt5.QtGui import QFont

class SchedulerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # 왼쪽 패널: 스케줄 목록
        left_panel = QGroupBox("스케줄 목록")
        left_layout = QVBoxLayout()
        
        self.schedule_list = QListWidget()
        self.schedule_list.setMinimumWidth(300)
        self.schedule_list.itemClicked.connect(self.schedule_selected)
        
        left_layout.addWidget(self.schedule_list)
        
        # 스케줄 삭제 버튼
        self.remove_button = QPushButton("선택한 스케줄 삭제")
        self.remove_button.setStyleSheet("background-color: #ff9999;")
        left_layout.addWidget(self.remove_button)
        
        left_panel.setLayout(left_layout)
        
        # 오른쪽 패널: 스케줄 설정
        right_panel = QGroupBox("스케줄 설정")
        right_layout = QVBoxLayout()
        
        # 요일 선택
        days_group = QGroupBox("요일 선택")
        days_layout = QGridLayout()
        self.day_checkboxes = []
        days = ["월", "화", "수", "목", "금", "토", "일"]
        for i, day in enumerate(days):
            checkbox = QCheckBox(day)
            checkbox.setStyleSheet("QCheckBox { padding: 5px; }")
            self.day_checkboxes.append(checkbox)
            days_layout.addWidget(checkbox, 0, i)
        days_group.setLayout(days_layout)
        right_layout.addWidget(days_group)
        
        # 시간 설정
        time_group = QGroupBox("시간 설정")
        time_layout = QHBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setStyleSheet("QTimeEdit { padding: 5px; min-width: 100px; }")
        time_layout.addWidget(self.time_edit)
        time_group.setLayout(time_layout)
        right_layout.addWidget(time_group)
        
        # 반복 설정
        repeat_group = QGroupBox("반복 설정")
        repeat_layout = QVBoxLayout()
        self.repeat_checkbox = QCheckBox("매주 반복")
        self.repeat_checkbox.setStyleSheet("QCheckBox { padding: 5px; }")
        repeat_layout.addWidget(self.repeat_checkbox)
        repeat_group.setLayout(repeat_layout)
        right_layout.addWidget(repeat_group)
        
        # 추가 버튼
        self.add_button = QPushButton("스케줄 추가")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #99cc99;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #88bb88;
            }
        """)
        right_layout.addWidget(self.add_button)
        
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        
        # 메인 레이아웃에 패널 추가
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        self.setLayout(main_layout)
        
    def schedule_selected(self, item):
        if not item:
            return
            
        # 스케줄이 선택되었을 때 설정 필드 업데이트
        schedule_text = item.text()
        days, time, repeat = self.parse_schedule(schedule_text)
        
        # 요일 체크박스 업데이트
        for checkbox in self.day_checkboxes:
            checkbox.setChecked(checkbox.text() in days)
        
        # 시간 업데이트
        self.time_edit.setTime(QTime.fromString(time, "HH:mm"))
        
        # 반복 여부 업데이트
        self.repeat_checkbox.setChecked(repeat == "매주 반복")
    
    def parse_schedule(self, schedule):
        # "월, 화, 수 14:30 (매주 반복)" 형식의 문자열 파싱
        try:
            parts = schedule.split(" ")
            days = parts[0].split(", ")
            time = parts[1]
            repeat = parts[2].strip("()")
            return days, time, repeat
        except:
            return [], "00:00", "1회"
            
    def clear_inputs(self):
        # 입력 필드 초기화
        for checkbox in self.day_checkboxes:
            checkbox.setChecked(False)
        self.time_edit.setTime(QTime(0, 0))
        self.repeat_checkbox.setChecked(False)
