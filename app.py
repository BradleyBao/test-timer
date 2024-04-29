from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QMenu, QAction, QMessageBox, QSystemTrayIcon, QMessageBox, QGraphicsColorizeEffect
from PyQt5.QtCore import QThread, pyqtSignal, QSharedMemory, Qt, QTime, QTimer, QUrl
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QColor
from PyQt5.QtMultimedia import QSoundEffect 
from PyQt5.QtWinExtras import QWinTaskbarButton, QWinTaskbarProgress

from timer_ui import Ui_MainWindow
from setting import Ui_SettingInference
import sys, os, json, time, platform
from logging_config import logger

class TestTimer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(TestTimer, self).__init__(parent) 
        self.setupUi(self) 
        self.setup()
        self.show() 

        self.windows_setup() 

    def windows_setup(self):
        if platform.system() == "Windows":
            self._TASK_PROGRESS_BAR_WIN_BTN = QWinTaskbarButton(self)
            self._TASK_BAR_PROGRESS = self._TASK_PROGRESS_BAR_WIN_BTN.progress()
            self._TASK_PROGRESS_BAR_WIN_BTN.setWindow(self.windowHandle())
            self._task_progress_bar_status = False

    def setup(self):
        self.setWindowTitle("Test Timer")
        self.setWindowIcon(QIcon("sources/logos/logo.png"))

        self.running_procedure = None
        self.setting_window = SettingInf(self) 
        self.setting_window.run_procedure_from_setting.connect(self.start_procedure)
        window_width = self.size().width()
        # print(window_width)
        id1 = QFontDatabase.addApplicationFont("sources/fonts/cos_font.ttf")
        id2 = QFontDatabase.addApplicationFont("sources/fonts/Roboto-Regular.ttf")
        # families = QFontDatabase.applicationFontFamilies(id2)
        # print(families[0])
        # self.title.setFont(QFont("Federation Starfleet Hull 23rd", 120))
        self.special_font = True
        # title_size = int(window_width / 18) - len(self.title.text())*2
        
        # display_size = int(window_width / 10)
        display_size = 120
        # subtitle_size = int(window_width / 18) - len(self.subtitle.text())*2 

        # titles_size = min(title_size, subtitle_size)
        titles_size = 50

        self.display_screen.setFont(QFont("Roboto", display_size))
        self.subtitle.setFont(QFont("Roboto", titles_size))
        self.title.setFont(QFont("Roboto", titles_size))
        # self.title.setText("")
        self.display_screen.setText("Test Timer")

    # def resizeEvent(self, event):
    #     window_width = self.size().width() 
    #     title_size = int(window_width / 18) - len(self.title.text())*2
    #     display_size = int(window_width / 10) - len(self.display_screen.text())*2
    #     subtitle_size = int(window_width / 18) - len(self.subtitle.text())*2

    #     titles_size = min(title_size, subtitle_size)

    #     self.title.setFont(QFont("Roboto", titles_size))

    #     if self.special_font:
    #         self.display_screen.setFont(QFont("Federation Starfleet Hull 23rd", display_size))

    #     else:
    #         self.display_screen.setFont(QFont("Roboto", display_size))
    #     self.subtitle.setFont(QFont("Roboto", titles_size))
        
    def windowsProgressBarIndeterminate(self):
        if platform.system() == 'Windows':
            # If currently running
            if self._task_progress_bar_status:
                self.windowsProgressBarStop()

            self._TASK_BAR_PROGRESS.setRange(0, 0)
            self._TASK_BAR_PROGRESS.show()
            self._task_progress_bar_status = True

    def windowsProgressBarPercentage(self):
        if platform.system() == 'Windows':
            if self._task_progress_bar_status:
                self.windowsProgressBarStop()

            self._TASK_BAR_PROGRESS.setRange(0, 100)
            self._TASK_BAR_PROGRESS.show()
            self._task_progress_bar_status = True

    def windowsProgressBarStop(self):
        if platform.system() == 'Windows':
            self._TASK_BAR_PROGRESS.stop()
            self._TASK_BAR_PROGRESS.hide()
            self._TASK_BAR_PROGRESS.reset()
            self._TASK_BAR_PROGRESS.resume()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F3:
            self.setting_window.show() 

        elif event.key() == Qt.Key_F11:
            self.showNormal() if self.isFullScreen() else self.showFullScreen() 

    def start_procedure(self, procedure:dict):
        self.running_procedure = Procedure(procedure) 
        self.running_procedure.update_text_info.connect(self.update_text)
        self.running_procedure.update_main_timer.connect(self.update_time)
        self.running_procedure.update_timer_info.connect(self.update_timer_info_board)
        self.running_procedure.update_text_color.connect(self.update_text_color) 
        self.running_procedure.update_timer_color.connect(self.update_timer_color) 
        self.running_procedure.update_size_text_timer.connect(self.update_size_of_text_timer)
        self.running_procedure.update_bg.connect(self.update_bg_func)
        self.running_procedure.windows_progress_bar_sig.connect(self.windows_progress_bar_sys)
        self.running_procedure.windows_progress_bar_value.connect(self.windows_progress_bar_value_with_range)
        self.running_procedure.windows_progress_bar_status.connect(self.windows_progress_bar_status)
        self.running_procedure.start() 

    def update_text(self, str1, str2):
        
        self.title.setText(str1)
        self.subtitle.setText(str2) 

    def update_time(self, hour, min, second):
        self.display_screen.setText(f"{hour}:{min}:{second}") 

    def update_timer_info_board(self, info:str):
        self.display_screen.setText(info) 
        # window_width = self.size().width() 
        # display_size = int(window_width / 10) - len(self.display_screen.text())*2
        # self.display_screen.setFont(QFont("Roboto", display_size))
        self.special_font = False 

    def update_text_color(self, lst1, lst2): 
        color_effect_1 = QGraphicsColorizeEffect()
        color_effect_1.setColor(QColor(lst1[0], lst1[1], lst1[2], lst1[3]))
        color_effect_2 = QGraphicsColorizeEffect()
        color_effect_2.setColor(QColor(lst2[0], lst2[1], lst2[2], lst2[3])) 

        self.title.setGraphicsEffect(color_effect_1) 
        self.subtitle.setGraphicsEffect(color_effect_2) 

    def update_timer_color(self, lst): 
        color_effect = QGraphicsColorizeEffect() 
        color_effect.setColor(QColor(lst[0], lst[1], lst[2], lst[3])) 
        self.display_screen.setGraphicsEffect(color_effect) 

    def update_size_of_text_timer(self, title_size:int, subtitle_size:int, timer_size:int): 
        self.title.setFont(QFont("Roboto", title_size)) 
        self.subtitle.setFont(QFont("Roboto", subtitle_size)) 
        self.display_screen.setFont(QFont("Roboto", timer_size)) 

    def update_bg_func(self, bg:list):
        self.setStyleSheet("QMainWindow, #centralwidget {\n"
        f"    background-color: rgb({bg[0]}, {bg[1]}, {bg[2]}) \n"
        "}") 

    def windows_progress_bar_sys(self, type:int): 
        if type == 0:
            # Indeterminate
            self.windowsProgressBarIndeterminate() 

        elif type == 1:
            # Stop 
            self.windowsProgressBarStop() 

        elif type == 2:
            # Range 
            self.windowsProgressBarPercentage() 

    def windows_progress_bar_status(self, status:int): 
        if status == 0:
            # Pause 
            self._TASK_BAR_PROGRESS.pause() 

        elif status == 1:
            # Resume 
            self._TASK_BAR_PROGRESS.resume() 

        elif status == 2:
            # Stop 
            self._TASK_BAR_PROGRESS.stop() 

    def windows_progress_bar_value_with_range(self, value:int):
        if platform.system() == "Windows":
            self._TASK_BAR_PROGRESS.setValue(int(value))

class Procedure(QThread):

    update_text_info = pyqtSignal(str, str) 
    update_main_timer = pyqtSignal(str, str, str)

    update_timer_info = pyqtSignal(str) 
    update_text_color = pyqtSignal(list, list) 
    update_timer_color = pyqtSignal(list) 

    update_size_text_timer = pyqtSignal(int, int, int) 
    update_bg = pyqtSignal(list)

    windows_progress_bar_sig = pyqtSignal(int)
    windows_progress_bar_value = pyqtSignal(int) 

    windows_progress_bar_status = pyqtSignal(int) 

    def __init__(self, procedure:dict) -> None:
        super(Procedure, self).__init__()
        self.procedure = procedure 
        self.blk_text_thread = None
        self.sound_effect = QSoundEffect() 
        self.starting_title_1 = self.procedure["1st_starting_title"] 
        self.starting_subtitle_1 = self.procedure["1st_starting_subtitle"] 

        self.starting_waiting_time_hour, self.starting_waiting_time_minute, self.starting_waiting_time_second = [int(i) for i in self.procedure['starting_waiting_time'].split(":")]
        

        self.starting_title_color = self.procedure['starting_title_color']
        self.starting_subtitle_color = self.procedure['starting_subtitle_color']
        self.starting_display_color = self.procedure['starting_timer_color']
        self.starting_title_2 = self.procedure['2nd_starting_title']
        self.starting_subtitle_2 = self.procedure['2nd_starting_subtitle']
        self.in_progress_title = self.procedure['in_progress_title']
        self.in_progress_title_color = self.procedure['in_progress_title_color']
        self.in_progress_subtitle = self.procedure['in_progress_subtitle']
        self.in_progress_subtitle_color = self.procedure['in_progress_subtitle_color']
        
        self.main_hour, self.main_minute, self.main_seconds = [int(i) for i in self.procedure['main_timer'].split(":")] 

        self.main_timer_color = self.procedure['main_timer_color']
        self.last_countdown_label_yes_no = self.procedure['last_cd_op'] 
        self.last_countdown_title = self.procedure['last_cd_title']
        self.last_countdown_subtitle = self.procedure['last_cd_subtitle']
        self.last_countdown_color = self.procedure['last_cd_color']
        self.end_title = self.procedure['end_title']
        self.end_subtitle = self.procedure['end_subtitle']
        self.starting_display = self.procedure['starting_display'] 

        self.title_size = self.procedure['title_size']
        self.subtitle_size = self.procedure['subtitle_size'] 
        self.timer_size = self.procedure['timer_size'] 

        self.background_color = self.procedure["background_color"]
        

    def set_sizes(self, title:int, subtitle:int, timer:int): 
        self.update_size_text_timer.emit(title, subtitle, timer)

    def prepare_procedure(self):
        logger.info("Preparing Procedure Started")
        self.set_sizes(self.title_size, self.subtitle_size, self.timer_size)
        self.update_bg.emit(list(self.background_color)) 
        self.update_text_color.emit(list(self.starting_title_color), list(self.starting_subtitle_color))
        self.update_text_info.emit(self.starting_title_1, self.starting_subtitle_1) 
        self.update_timer_color.emit(list(self.starting_display_color)) 
        self.update_timer_info.emit(self.starting_display)
        self.windows_progress_bar_sig.emit(0)
        self.silent_countdown(self.starting_waiting_time_hour, self.starting_waiting_time_minute, self.starting_waiting_time_second)
        logger.info("Preparing Procedure Engaged")
        

    def silent_countdown(self, hours, minutes, seconds):
        """
        Countdown System - Accurate 
        """
        # Convert hours, minutes, and seconds to total seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds 
        remaining_seconds = total_seconds
        warning_time = 10
        warning_time2 = 5

        flag1 = True
        flag2 = True
        
        # Get the current time in seconds since epoch
        start_time = time.time()
        
        while remaining_seconds > 0 or remaining_minutes > 0 or remaining_hours > 0:
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            
            # Calculate remaining time
            remaining_seconds = max(total_seconds - elapsed_time, 0)
            
            # Convert remaining seconds to hours, minutes, and seconds
            remaining_hours = int(remaining_seconds // 3600)
            remaining_minutes = int((remaining_seconds % 3600) // 60)
            remaining_seconds = int(remaining_seconds % 60)
            
            if flag1 and total_seconds > 10 and remaining_seconds <= warning_time and remaining_minutes == 0 and remaining_hours == 0:
                flag1 = False
                self.time_reminder_light() 

            if flag2 and total_seconds > 5 and remaining_seconds <= warning_time2 and remaining_minutes == 0 and remaining_hours == 0:
                flag2 = False
                self.time_reminder_light2()
                

            # Display remaining time
            print(f"Time remaining: {remaining_hours} hours, {remaining_minutes} minutes, {remaining_seconds} seconds", end="\r")
            
            # Sleep for a short interval to avoid busy-waiting
            time.sleep(0.1)
        
        logger.info(f"Silent Countdown of {hours} hours {minutes} minutes {seconds} seconds have completed. ")


    def countdown(self, hours, minutes, seconds):
        """
        Countdown System - Accurate 
        """
        # Convert hours, minutes, and seconds to total seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds 
        remaining_seconds = total_seconds
        warning_time = 30

        flag = True
        
        # Get the current time in seconds since epoch
        start_time = time.time()
        
        while remaining_seconds > 0 or remaining_minutes > 0 or remaining_hours > 0:
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            
            # Calculate remaining time
            remaining_seconds = max(total_seconds - elapsed_time, 0) 

            self.windows_progress_bar_value.emit(int((1 - (remaining_seconds) / total_seconds)*100))
            
            # Convert remaining seconds to hours, minutes, and seconds
            remaining_hours = int(remaining_seconds // 3600)
            remaining_minutes = int((remaining_seconds % 3600) // 60)
            remaining_seconds = int(remaining_seconds % 60)

            self.update_main_timer.emit(f"{remaining_hours:02d}", f"{remaining_minutes:02d}", f"{remaining_seconds:02d}")
            
            if flag and total_seconds > 30 and remaining_seconds <= warning_time and remaining_minutes == 0 and remaining_hours == 0:
                flag = False
                self.time_reminder_blink()

            # Display remaining time
            # print(f"Time remaining: {remaining_hours} hours, {remaining_minutes} minutes, {remaining_seconds} seconds", end="\r")
            
            # Sleep for a short interval to avoid busy-waiting
            time.sleep(0.1)
        
        logger.info(f"Main Countdown of {hours} hours {minutes} minutes {seconds} seconds have completed. ")

    def time_reminder_light(self):
        self.update_text_info.emit(self.starting_title_2, "") 
        # self.update_timer_info.emit("") 
        time.sleep(1.5)
        self.update_text_info.emit(self.starting_title_2, self.starting_subtitle_2) 
        
        # self.showTimer() 

    def time_reminder_light2(self):
        self.update_text_color.emit(list(self.in_progress_title_color), list(self.in_progress_subtitle_color)) 
        self.update_text_info.emit(self.in_progress_title, "") 
        self.update_timer_info.emit("") 
        time.sleep(1.5) 
        self.update_text_info.emit(self.in_progress_title, self.in_progress_subtitle) 
        
        time.sleep(2)

        self.play_sound(QUrl.fromLocalFile("sources/sound/start.wav"), False) 

        self.update_timer_color.emit(list(self.main_timer_color)) 

        self.blk_text_thread = BlinkText(5) 
        self.blk_text_thread.blink_text_sig.connect(self.blink_timer_back) 
        self.blk_text_thread.start() 

    def blink_timer_back(self, blink:bool):
        if blink:
            self.update_main_timer.emit(f"{self.main_hour:02d}", f"{self.main_minute:02d}", f"{self.main_seconds:02d}") 
            

        else:
            self.update_timer_info.emit("") 
            
    def time_reminder_blink(self):
        if self.last_countdown_label_yes_no:
            self.play_sound(QUrl.fromLocalFile("sources/sound/30_seconds.wav"), False) 

            self.update_text_color.emit(list(self.last_countdown_color), list(self.last_countdown_color))

            self.update_text_info.emit(self.last_countdown_title, self.last_countdown_subtitle)
            self.blink_text(10) 

    def showTimer(self): 
        
        self.update_main_timer.emit(f"{self.main_hour:02d}", f"{self.main_minute:02d}", f"{self.main_seconds:02d}") 

    def blink_text(self, cd:int): 
        self.blk_text_thread = BlinkText(75) 
        self.blk_text_thread.blink_text_sig.connect(self.blink_back) 
        self.blk_text_thread.start() 

    def blink_back(self, blink:bool):
        if blink:
            self.update_text_info.emit(self.last_countdown_title, self.last_countdown_subtitle) 

        else:
            self.update_text_info.emit("", "") 

    def play_sound(self, file_url:QUrl, loop:bool):
        self.sound_effect.setSource(file_url) 

        if loop:
            self.sound_effect.setLoopCount(time) 

        self.sound_effect.play() 


    def progress_procedure(self):
        logger.info("Main Procedure Started")
        self.update_text_info.emit(self.in_progress_title, self.in_progress_subtitle)
        self.windows_progress_bar_sig.emit(2)
        self.countdown(self.main_hour, self.main_minute, self.main_seconds)
        self.windows_progress_bar_status.emit(2) 
        logger.info("Main Procedure Engaged")

    def run(self):
        self.prepare_procedure() 
        self.progress_procedure() 
        self.play_sound(QUrl.fromLocalFile("sources/sound/end.wav"), False) 
        
class BlinkText(QThread):
    blink_text_sig = pyqtSignal(bool)
    def __init__(self, cd:int):
        super(BlinkText, self).__init__()
        self.cd = cd

    def run(self):
        Flag = False
        for i in range(self.cd):
            self.blink_text_sig.emit(Flag)
            Flag = not Flag
            time.sleep(.4)


class SettingInf(QMainWindow, Ui_SettingInference):

    run_procedure_from_setting = pyqtSignal(dict)

    def __init__(self, parent = TestTimer):
        super(SettingInf, self).__init__(parent) 
        self.setupUi(self) 
        self.setup() 

    def setup(self):
        self.plans.clear() 
        self.set_plan_info_status(False) 
        self.check_and_create_json_file("plans.json")
        self.new_plan.clicked.connect(self.add_plan) 
        self.plans.itemClicked.connect(self.show_plan) 
        self.plans.itemDoubleClicked.connect(self.edit_plan) 
        self.save_plan.clicked.connect(self.save_current_plan)
        self.PushButton.clicked.connect(self.run_procedure) 
        self.read_data()

    def read_data(self):
        
        for each_procedure in self.DATA:
            if each_procedure == "ID":
                continue

            self.plans.addItem(each_procedure) 

    def run_procedure(self):

        if self.plans.currentItem():

            name = self.plans.currentItem().text() 
            self.run_procedure_from_setting.emit(self.DATA[name]) 

            self.hide() 


    def check_and_create_json_file(self, file_path):
        """
        Checks if a JSON file exists at the specified path.
        If not, creates an empty JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            None
        """
        
        if os.path.isfile(file_path):
            logger.info(f"File '{file_path}' exists and is readable.")
        else:
            logger.warning(f"File '{file_path}' is missing or not readable. Creating the file...")
            with open(file_path, 'w') as json_file:
                json.dump({}, json_file) 

        with open(file_path, "r") as json_file:
            self.DATA = json.load(json_file) 
        # print(self.DATA)

        # Check if the key "new_key" exists in the JSON data
        if "ID" not in self.DATA:
            # If not, create the key and set its value
            self.__ID = self.DATA["ID"] = 1

        else:
            self.__ID = self.DATA["ID"] 

    def save_json(self):
        with open("plans.json", "w") as json_file:
            json.dump(self.DATA, json_file) 

        logger.info("User data has been saved. ")

    def add_plan(self):
        name = f"Plan {self.__ID}"
        self.plans.addItem(name) 

        self.DATA[name] = {
            "1st_starting_title" : "", 
            "1st_starting_subtitle" : "", 
            "starting_waiting_time" : "", 
            "starting_title_color" : (), 
            "starting_subtitle_color" : (), 
            "starting_timer_color" : (), 
            "2nd_starting_title" : "", 
            "2nd_starting_subtitle" : "", 
            "in_progress_title" : "", 
            "in_progress_title_color" : (), 
            "in_progress_subtitle" : "", 
            "in_progress_subtitle_color" : (), 
            "main_timer" : "", 
            "main_timer_color" : (), 
            "last_cd_op" : False, 
            "last_cd_title" : "", 
            "last_cd_subtitle" : "", 
            "last_cd_color" : (), 
            "end_title" : "", 
            "end_subtitle" : "", 
            "starting_display" : "", 
            "background_color" : (), 
            "title_size" : 50, 
            "subtitle_size" : 50, 
            "timer_size" : 120, 
        }

        # print(self.DATA)

        self.__ID += 1 

    def show_plan(self):
        self.set_plan_info_status(False)
        # print(self.__ID)
        self.display_plan_info()

    def edit_plan(self):
        self.display_plan_info()
        self.set_plan_info_status(True) 

    def display_plan_info(self):
        name = self.plans.currentItem().text() 
        if name in self.DATA:
            try:
                self.plan_name.setText(name)
                self.starting_title_1.setText(self.DATA[name]["1st_starting_title"]) 
                self.starting_subtitle_1.setText(self.DATA[name]["1st_starting_subtitle"])

                starting_waiting_time = self.DATA[name]['starting_waiting_time']

                if not starting_waiting_time:
                    self.starting_waiting_time.setTime(QTime(0, 0, 0))

                else:
                    starting_waiting_time_lst = [int(i) for i in starting_waiting_time.split(":")]
                    self.starting_waiting_time.setTime(QTime(starting_waiting_time_lst[0], starting_waiting_time_lst[1], starting_waiting_time_lst[2]))

                starting_title_color = self.DATA[name]['starting_title_color']

                if not starting_title_color:
                    self.starting_title_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.starting_title_color.color.setRgb(starting_title_color[0], starting_title_color[1], starting_title_color[2], starting_title_color[3]) 

                starting_subtitle_color = self.DATA[name]['starting_subtitle_color'] 

                if not starting_subtitle_color:
                    self.starting_subtitle_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.starting_subtitle_color.color.setRgb(starting_subtitle_color[0], starting_subtitle_color[1], starting_subtitle_color[2], starting_subtitle_color[3])

                starting_timer_color = self.DATA[name]['starting_timer_color']

                if not starting_timer_color:
                    self.starting_display_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.starting_display_color.color.setRgb(starting_timer_color[0], starting_timer_color[1], starting_timer_color[2], starting_timer_color[3])
                
                self.starting_title_2.setText(self.DATA[name]['2nd_starting_title']) 
                self.starting_subtitle_2.setText(self.DATA[name]['2nd_starting_subtitle']) 
                self.in_progress_title.setText(self.DATA[name]['in_progress_title'])

                in_progress_title_color = self.DATA[name]['in_progress_title_color'] 

                if not in_progress_title_color:
                    self.in_progress_title_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.in_progress_title_color.color.setRgb(in_progress_title_color[0], in_progress_title_color[1], in_progress_title_color[2], in_progress_title_color[3])
                    
                
                self.in_progress_subtitle.setText(self.DATA[name]['in_progress_subtitle'])

                in_progress_subtitle_color = self.DATA[name]['in_progress_subtitle_color'] 

                if not in_progress_subtitle_color:
                    self.in_progress_subtitle_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.in_progress_subtitle_color.color.setRgb(in_progress_subtitle_color[0], in_progress_subtitle_color[1], in_progress_subtitle_color[2], in_progress_subtitle_color[3]) 
                


                main_timer = self.DATA[name]['main_timer']

                if not starting_waiting_time:
                    self.main_timer.setTime(QTime(0, 0, 0))

                else:
                    main_timer_lst = [int(i) for i in main_timer.split(":")]
                    self.main_timer.setTime(QTime(main_timer_lst[0], main_timer_lst[1], main_timer_lst[2]))

                main_timer_color = self.DATA[name]['main_timer_color']

                if not main_timer_color:
                    self.main_timer_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.main_timer_color.color.setRgb(main_timer_color[0], main_timer_color[1], main_timer_color[2], main_timer_color[3])
                

                self.last_countdown_yes_no.setChecked(self.DATA[name]['last_cd_op']) 

                self.last_countdown_title.setText(self.DATA[name]['last_cd_title'])
                self.last_countdown_subtitle.setText(self.DATA[name]['last_cd_subtitle'])
                
                last_cd_color = self.DATA[name]['last_cd_color']
                
                if not last_cd_color:
                    self.last_countdown_color.color.setRgb(0, 0, 0, 0) 

                else:
                    self.last_countdown_color.color.setRgb(last_cd_color[0], last_cd_color[1], last_cd_color[2], last_cd_color[3])
                
                self.end_title.setText(self.DATA[name]['end_title'])
                self.end_subtitle.setText(self.DATA[name]['end_subtitle'])
                self.starting_display.setText(self.DATA[name]['starting_display']) 

                # Title Size 
                self.title_size.setValue(self.DATA[name]["title_size"]) 
                self.subtitle_size.setValue(self.DATA[name]["subtitle_size"]) 
                self.timer_size.setValue(self.DATA[name]["timer_size"]) 

                background_color = self.DATA[name]["background_color"] 

                if not background_color:
                    self.background_color.color.setRgb(255, 255, 255, 0) 

                else:
                    self.background_color.color.setRgb(background_color[0], background_color[1], background_color[2], background_color[3]) 

            except KeyError:
                logger.warning("Invalid Plans: Certain Variables of the plan are missing; please save the current plan.  ")

        else: 
            logger.error("Can not find the current plan. ")
            

    def save_current_plan(self): 
        starting_title_1 = self.starting_title_1.text()
        starting_title_2 = self.starting_title_2.text()
        starting_subtitle_1 = self.starting_subtitle_1.text()
        starting_subtitle_2 = self.starting_subtitle_2.text()
        in_progress_title = self.in_progress_title.text()
        in_progress_subtitle = self.in_progress_subtitle.text()
        last_countdown_label_yes_no = self.last_countdown_yes_no.isChecked()
        last_countdown_title = self.last_countdown_title.text()
        last_countdown_subtitle = self.last_countdown_subtitle.text()
        plan_name = self.plan_name.text()
        end_title = self.end_title.text()
        end_subtitle = self.end_subtitle.text()
        starting_title_color:tuple = self.starting_title_color.color.getRgb()
        starting_subtitle_color:tuple = self.starting_subtitle_color.color.getRgb()
        in_progress_title_color:tuple = self.in_progress_title_color.color.getRgb()
        in_progress_subtitle_color:tuple = self.in_progress_subtitle_color.color.getRgb()
        main_timer_hour:int = self.main_timer.getTime().hour()
        main_timer_minute:int = self.main_timer.getTime().minute()
        main_timer_second:int = self.main_timer.getTime().second()
        starting_waiting_time_hour:int = self.starting_waiting_time.getTime().hour()
        starting_waiting_time_minute:int = self.starting_waiting_time.getTime().minute()
        starting_waiting_time_second:int = self.starting_waiting_time.getTime().second() 
        starting_display = self.starting_display.text()
        starting_display_color:tuple = self.starting_display_color.color.getRgb()
        main_timer_color:tuple = self.main_timer_color.color.getRgb()
        last_countdown_color:tuple = self.last_countdown_color.color.getRgb() 
        title_size = self.title_size.value() 
        subtitle_size = self.subtitle_size.value() 
        timer_size = self.timer_size.value() 
        background_color = self.background_color.color.getRgb() 

        name = self.plans.currentItem().text() 

        self.DATA[name]["1st_starting_title"] = starting_title_1 
        self.DATA[name]["1st_starting_subtitle"] = starting_subtitle_1 
        self.DATA[name]['starting_waiting_time'] = f"{starting_waiting_time_hour}:{starting_waiting_time_minute}:{starting_waiting_time_second}" 
        self.DATA[name]['starting_title_color'] = starting_title_color
        self.DATA[name]['starting_subtitle_color'] = starting_subtitle_color
        self.DATA[name]['starting_timer_color'] = starting_display_color
        self.DATA[name]['2nd_starting_title'] = starting_title_2
        self.DATA[name]['2nd_starting_subtitle'] = starting_subtitle_2
        self.DATA[name]['in_progress_title'] = in_progress_title
        self.DATA[name]['in_progress_title_color'] = in_progress_title_color
        self.DATA[name]['in_progress_subtitle'] = in_progress_subtitle
        self.DATA[name]['in_progress_subtitle_color'] = in_progress_subtitle_color
        self.DATA[name]['main_timer'] = f"{main_timer_hour}:{main_timer_minute}:{main_timer_second}"
        self.DATA[name]['main_timer_color'] = main_timer_color
        self.DATA[name]['last_cd_op'] = last_countdown_label_yes_no 
        self.DATA[name]['last_cd_title'] = last_countdown_title
        self.DATA[name]['last_cd_subtitle'] = last_countdown_subtitle
        self.DATA[name]['last_cd_color'] = last_countdown_color
        self.DATA[name]['end_title'] = end_title
        self.DATA[name]['end_subtitle'] = end_subtitle
        self.DATA[name]['starting_display'] = starting_display
        self.DATA[name]['title_size'] = title_size
        self.DATA[name]['subtitle_size'] = subtitle_size
        self.DATA[name]['timer_size'] = timer_size
        self.DATA[name]['background_color'] = background_color
        

        self.DATA[plan_name] = self.DATA.pop(name) 

        self.plans.currentItem().setText(plan_name) 

        self.save_json() 

    def set_plan_info_status(self, status:bool): 
        self.starting_title_1.setEnabled(status) 
        self.starting_title_2.setEnabled(status) 
        self.starting_subtitle_1.setEnabled(status) 
        self.starting_subtitle_2.setEnabled(status) 
        self.in_progress_title.setEnabled(status)
        self.in_progress_subtitle.setEnabled(status)
        self.last_countdown_yes_no.setEnabled(status)
        self.last_countdown_title.setEnabled(status) 
        self.last_countdown_subtitle.setEnabled(status)
        self.plan_name.setEnabled(status) 
        self.save_plan.setEnabled(status)
        self.end_title.setEnabled(status) 
        self.end_subtitle.setEnabled(status) 
        self.starting_title_color.setEnabled(status) 
        self.starting_subtitle_color.setEnabled(status) 
        self.in_progress_title_color.setEnabled(status) 
        self.in_progress_subtitle_color.setEnabled(status) 
        self.last_countdown_yes_no.setEnabled(status) 
        self.main_timer.setEnabled(status) 
        self.starting_waiting_time.setEnabled(status) 
        self.starting_display.setEnabled(status) 
        self.starting_display_color.setEnabled(status)
        self.main_timer_color.setEnabled(status) 
        self.last_countdown_color.setEnabled(status)
        self.title_size.setEnabled(status)
        self.subtitle_size.setEnabled(status)
        self.timer_size.setEnabled(status)
        self.background_color.setEnabled(status)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    
    window = TestTimer()
    sys.exit(app.exec_())