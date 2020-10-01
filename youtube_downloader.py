#!/usr/bin/python3
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QFormLayout, QFileDialog, QPushButton, QCheckBox, QComboBox
from PySide2.QtGui import QPixmap
import sys, getpass, platform, time
from youtube_dl import YoutubeDL

class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(600, 300)
        self.setWindowTitle("YouTube-Downloader")
        
        self.title_label: QLabel = QLabel("<center>YouTube Downloader</center>", self)
        self.title_label.setStyleSheet("""
        QLabel{
            font-size: 40px;
            font-weight: bold;
        }
        """)
        self.title_label.setGeometry(0, 20, self.width(), 60)
        self.form_widget: QWidget = QWidget(self)
        self.form_widget.setStyleSheet("""
        QWidget{
            font-size: 15px
        }
        """)
        self.form_widget_layout: QFormLayout = QFormLayout()
        self.url_input: QLineEdit = QLineEdit()
        self.form_widget_layout.addRow("Video URL:", self.url_input)
        self.extract_audio_checkbox: QCheckBox = QCheckBox("Only extract the audio") 
        self.form_widget_layout.addWidget(self.extract_audio_checkbox)
        self.filename_input: QLineEdit = QLineEdit()
        self.form_widget_layout.addRow("Filename (optional):", self.filename_input)
        self.storage_location_button: QPushButton = QPushButton(f"C:/Users/{getpass.getuser()}/Downloads" if "Windows" == platform.system() else f"/home/{getpass.getuser()}/Downloads" if "Linux" == platform.system() else "Bitte wähle einen Speicherort aus")
        self.storage_location_button.setStyleSheet("""
        QPushButton{
            text-align: left;
        } 
        """)
        self.storage_location_button.clicked.connect(self.change_storage_location)
        self.form_widget_layout.addRow("Storage Location:", self.storage_location_button)
        self.form_widget.setLayout(self.form_widget_layout)
        self.form_widget.setGeometry((self.width() - 550)/2, 80, 550, 200)
        self.submit_button: QPushButton = QPushButton("Download this Video", self)
        self.submit_button.clicked.connect(self.download_video)
        self.submit_button.setGeometry((self.width() - 400)/2 , 220, 400, 30)
        self.submit_button.setStyleSheet("""
        QPushButton{
            font-size: 15px
        }
        """)
        self.state_message_label: QLabel = QLabel(self)
        self.state_message_label.setGeometry((self.width() - 400)/2, 250, 400, 20)

    def change_storage_location(self) -> None:
        new_storage_location: str = QFileDialog.getExistingDirectory(None, "Please select a folder", self.storage_location_button.text())
        if new_storage_location != "":
            self.storage_location_button.setText(new_storage_location)

    def download_video(self) -> None:
        if not self.url_input.text().startswith(("www.youtube.com/watch?v=", "https://www.youtube.com/watch?v=")):
            self.state_message("Please please enter a valid video URL!", "red")
            return
        filename: str = self.filename_input.text() if self.filename_input.text() != "" else "%(title)s"
        ydl_opts: dict = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" if not self.extract_audio_checkbox.isChecked() else "bestaudio/best",
            "outtmpl": f"{self.storage_location_button.text()}/{filename}.%(ext)s",
        }
        if self.extract_audio_checkbox.isChecked():
            ydl_opts["postprocessors"] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        print("Start Downloading...")
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url_input.text()])
        except:
            self.state_message("An error occurred while downloading this video!", "red")
            print("An error occurred!")
            return           
        self.state_message("The video was downloaded successfully!", "green")
        self.url_input.setText("")
        self.filename_input.setText("")
        self.extract_audio_checkbox.setChecked(False)
        print("Downloading is completed!")

    def state_message(self, message: str, color: str) -> None:
        self.state_message_label.setStyleSheet(f"""
        QLabel{{
            color: {color};
        }}
        """)
        self.state_message_label.setText(f"<center>{message}</center>")

def main() -> None:
    app: QApplication = QApplication()
    main_widget: MainWidget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()