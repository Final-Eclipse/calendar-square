from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QIcon
from datetime import datetime

# Reference
# https://www.google.com/search?q=calendar+red+line+at+top&udm=2&sxsrf=AE3TifMiXMsgHrR3oa2W-EQ15y6KAKIeHw%3A1766561107641

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Timer that updates the time every second
        self.set_time = QTimer()
        self.set_time.timeout.connect(self.update_current_time)
        self.set_time.start(1000)

        # Saves notes to file every time a change is made to the text
        self.text_area.textChanged.connect(self.save_calendar_notes)

        # Initializes self.text_area with calendar_notes.txt's contents
        self.get_calendar_notes()

    def initUI(self):
        self.setMinimumSize(300, 325)
        self.setWindowTitle("Calendar")
        self.setWindowIcon(QIcon("calendar_square/calendar_square.ico"))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Adds glow to container, which applies the glow to all calendar widgets
        calendar_glow_container = QWidget()
        calendar_glow_container_layout = QVBoxLayout()
        calendar_glow_container.setLayout(calendar_glow_container_layout)
        glow = self.create_text_glow_effect()
        calendar_glow_container.setGraphicsEffect(glow)
        main_layout.addWidget(calendar_glow_container, 1)

        # Create calendar_central_widget and calendar_layout
        calendar_central_widget = QWidget()
        calendar_layout = QVBoxLayout()
        calendar_central_widget.setLayout(calendar_layout)
        calendar_glow_container_layout.addWidget(calendar_central_widget)

        self.create_calendar_widgets()
        calendar_layout.addWidget(self.month_label, 1)
        calendar_layout.addWidget(self.middle_area, 1)
        calendar_layout.addWidget(self.day_label, 1)

        self.create_text_area()
        main_layout.addWidget(self.text_area, 1)
    
    def create_text_glow_effect(self) -> QGraphicsDropShadowEffect:
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        glow.setColor(QColor("#FFFFFF"))

        return glow

    def create_text_shadow_effect(self) -> QGraphicsDropShadowEffect:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0))

        return shadow

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 0, Qt.SolidLine))

        gradiant = QLinearGradient(0, 0, 0, self.height())  # start at x1, y1, and end at x2, y2 
        gradiant.setColorAt(0.0, QColor(254, 119, 213))
        gradiant.setColorAt(0.2, QColor(255, 130, 204))
        gradiant.setColorAt(0.4, QColor(255, 147, 182))
        gradiant.setColorAt(0.6, QColor(255, 140, 151))
        gradiant.setColorAt(0.8, QColor(255, 134, 129))
        gradiant.setColorAt(1.0, QColor(255, 136, 115))

        painter.setBrush(QBrush(gradiant))
        painter.drawRect(0, 0, self.width(), self.height())

    def create_text_area(self):
        self.text_area = QTextEdit()
        self.text_area.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: #FFFFFF; font-size: 40px")  # Makes text area background transparent
        self.text_area.setPlaceholderText("Type here")
        self.text_area.setFont(QFont("Chewy", 40, QFont.Thin))
        self.text_area.hide()

    def create_calendar_widgets(self):
        self.create_month_label()
        self.create_middle_area()
        self.create_day_label()

    def create_middle_area(self):
        self.middle_area = QWidget()
        qh_layout = QHBoxLayout()
        qh_layout.setContentsMargins(0, 0, 0, 0)
        qh_layout.setSpacing(0)

        self.create_day_of_the_month_label()
        qh_layout.addWidget(self.day_of_the_month_label)
        self.middle_area.setLayout(qh_layout)

        glow = self.create_text_glow_effect()
        self.middle_area.setGraphicsEffect(glow)

    def create_month_label(self):
        month = self.get_current_time()[0]

        self.month_label = QLabel(month)  
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setFont(QFont("Chewy", 40, QFont.Thin))
        self.month_label.setStyleSheet("color: white")
        self.month_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.month_label.setContentsMargins(0, 0, 0, 0)

        text_shadow = self.create_text_shadow_effect()
        self.month_label.setGraphicsEffect(text_shadow)

    def create_day_of_the_month_label(self):
        day_of_the_month = self.get_current_time()[2]

        self.day_of_the_month_label = QLabel(day_of_the_month)
        self.day_of_the_month_label.setFont(QFont("Chewy", 50, QFont.Thin))
        self.day_of_the_month_label.setStyleSheet("color: white")
        self.day_of_the_month_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.day_of_the_month_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.day_of_the_month_label.setContentsMargins(0, 0, 0, 0)

        # Shadow effect to text
        text_shadow = self.create_text_shadow_effect()
        self.day_of_the_month_label.setGraphicsEffect(text_shadow)

    def create_day_label(self):
        day = self.get_current_time()[1]

        self.day_label = QLabel(day)
        self.day_label.setFont(QFont("Chewy", 25, QFont.Thin))
        self.day_label.setStyleSheet("color: white")
        self.day_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        text_shadow = self.create_text_shadow_effect()
        self.day_label.setGraphicsEffect(text_shadow)

    # Gets the system's current month, day, and day of the month
    # Is only called when initially creating calendar widgets
    def get_current_time(self) -> tuple:
        current_time = datetime.now()

        month = current_time.strftime("%b")
        day = current_time.strftime("%A")
        day_of_the_month = current_time.strftime("%d")

        return month, day, day_of_the_month
    
    # Updates the current time every second
    def update_current_time(self):
        days = {
            "Mon": "Monday",
            "Tue": "Tuesday",
            "Wed": "Wednesday",
            "Thu": "Thursday",
            "Fri": "Friday",
            "Sat": "Saturday",
            "Sun": "Sunday",
        }

        current_time = QDate.currentDate().toString()

        month = current_time[4:7]
        day = current_time[0:3]
        day = days[day]
        day_of_the_month = current_time[8:10]

        self.month_label.setText(month)
        self.day_label.setText(day)
        self.day_of_the_month_label.setText(day_of_the_month)

    def show_or_hide_text_area(self, event):
        window_size = event.size()
        window_width = window_size.width()
        window_height = window_size.height()

        if window_width > 400 and window_height > 400:
            self.text_area.show()
        else:
            self.text_area.hide()

    # Keeps the window square
    def resizeEvent(self, event):  
        self.show_or_hide_text_area(event=event)
        self.resize_font(event=event)

    def resize_font(self, event):
        min_and_max_font_sizes = {
            "month_label": (40, 150),
            "day_of_the_month_label": (50, 160),
            "day_label": (25, 135)
        }

        for label_name, min_max_font in min_and_max_font_sizes.items():
            label_widget = getattr(self, label_name)
            new_font_size = int(event.size().width() * 0.03)        

            if new_font_size > min_max_font[1]:
                new_font_size = min_max_font[1]
            elif new_font_size < min_max_font[0]:
                new_font_size = min_max_font[0]

            font = label_widget.font()
            font.setPointSize(new_font_size)
            label_widget.setFont(font)
  
    # Initializes self.text_area with previously typed notes
    def get_calendar_notes(self):
        with open("calendar_square/calendar_notes.txt", "r") as file:
            current_notes = file.read()
        self.text_area.setText(current_notes)

    # Saves the current notes to calendar_notes.txt
    def save_calendar_notes(self):
        new_notes = self.text_area.toPlainText()
        with open("calendar_square/calendar_notes.txt", "w") as file:
            file.write(new_notes)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()