from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import numpy as np
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from playsound import playsound
from pathlib import Path


# Tentukan direktori dasar (tempat script berada)
BASE_DIR = Path(__file__).parent
SOUND_DIR = BASE_DIR / "Suara"
IMAGE_DIR = BASE_DIR

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(793, 417)
        MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        
        # Set icon aplikasi (gunakan path relatif)
        app_icon = QtGui.QIcon(str(IMAGE_DIR / "Logoapk.png"))
        MainWindow.setWindowIcon(app_icon)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Tombol Play
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 260, 131, 51))
        self.pushButton.setObjectName("pushButton")
        
        # Tombol Exit
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(640, 310, 131, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        
        # Label "Detected Colour"
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 320, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # Tampilan kamera (GraphicsView)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 10, 481, 301))
        self.graphicsView.setObjectName("graphicsView")
        
        # Tombol On Cam
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 260, 131, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        
        # TextEdit untuk menampilkan warna
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(190, 320, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        
        # Logo UCa
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(520, 0, 241, 241))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(str(IMAGE_DIR / "Logo UCa.png")))
        self.label_2.setObjectName("label_2")
        
        # Tampilan waktu
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(550, 240, 194, 22))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        
        # Tombol Reset
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(510, 310, 131, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 26))
        self.menubar.setObjectName("menubar")
        
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aplikasi Pendeteksi Warna"))
        self.pushButton.setText(_translate("MainWindow", "Play"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.label.setText(_translate("MainWindow", "Detected Colour"))
        self.pushButton_3.setText(_translate("MainWindow", "On Cam"))
        self.pushButton_4.setText(_translate("MainWindow", "Reset"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


def detect_color_at_point(frame, point):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_bounds = {
        'Merah': ([170, 120, 70], [180, 255, 255]),
        'Hijau': ([50, 25, 25], [70, 255, 255]),
        'Biru': ([90, 50, 50], [120, 255, 255]),
        'Kuning': ([25, 50, 50], [35, 255, 255]),
        'Ungu': ([137, 25, 25], [145, 255, 255])
    }

    detected_color = "Unknown"
    hsv_value = hsv_frame[point[1], point[0]]
    hsv_value = np.clip(hsv_value, 0, 255)  # Pastikan nilai valid

    for color_name, (lower, upper) in color_bounds.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        if np.all(lower_bound <= hsv_value) and np.all(hsv_value <= upper_bound):
            detected_color = color_name
            break
    
    return detected_color


def play_sound_for_color(color):
    sounds = {
        'Merah': SOUND_DIR / "Merah.mp3",
        'Hijau': SOUND_DIR / "Hijau.mp3",
        'Biru': SOUND_DIR / "Biru.mp3",
        'Kuning': SOUND_DIR / "Kuning.mp3",
        'Ungu': SOUND_DIR / "Ungu.mp3"
    }

    sound_path = sounds.get(color)
    if sound_path and sound_path.exists():
        try:
            playsound(str(sound_path))
        except Exception as e:
            print(f"Error playing sound for {color}: {e}")
    else:
        print(f"Sound file not found or not supported: {sound_path}")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cap = None
        self.last_detected_color = "Unknown"
        self.output_generated = False

        # Koneksi tombol
        self.pushButton.clicked.connect(self.play_button_clicked)
        self.pushButton_2.clicked.connect(self.exit_button_clicked)
        self.pushButton_3.clicked.connect(self.on_cam_button_clicked)
        self.pushButton_4.clicked.connect(self.reset_button_clicked)
        self.actionExit.triggered.connect(self.exit_button_clicked)
        self.actionAbout.triggered.connect(self.about_message)

        # Timer untuk update waktu
        self.timer_time = QtCore.QTimer(self)
        self.timer_time.timeout.connect(self.update_time)
        self.timer_time.start(1000)

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.fromString(current_time, "yyyy-MM-dd HH:mm:ss"))

    def on_cam_button_clicked(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                QMessageBox.warning(self, "Warning", "Gagal membuka kamera!")
                self.cap = None
                return
            self.label.setText("Kamera Menyala")
            self.timer_frame = QtCore.QTimer(self)
            self.timer_frame.timeout.connect(self.update_frame)
            self.timer_frame.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.timer_frame.stop()
            self.cap.release()
            self.cap = None
            QMessageBox.warning(self, "Warning", "Tidak dapat membaca dari kamera!")
            return

        # Gambar titik di tengah
        frame_center = (int(frame.shape[1] // 2), int(frame.shape[0] // 2))
        cv2.circle(frame, frame_center, 5, (0, 255, 0), -1)

        scene = QGraphicsScene()
        scene.addPixmap(self.convert_cv_qt(frame))
        self.graphicsView.setScene(scene)

    def play_button_clicked(self):
        if self.cap is None or not self.cap.isOpened():
            QMessageBox.warning(self, "Warning", "Silakan klik 'On Cam' terlebih dahulu!")
            return

        self.label.setText("Playing...")
        frame_center = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2))

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Gagal membaca frame.")
                break

            detected_color = detect_color_at_point(frame, frame_center)
            self.label.setText(f"Detected Colour: {detected_color}")
            self.textEdit.setPlainText(detected_color)

            # Gambar titik deteksi
            cv2.circle(frame, frame_center, 5, (0, 255, 0), -1)
            scene = QGraphicsScene()
            scene.addPixmap(self.convert_cv_qt(frame))
            self.graphicsView.setScene(scene)

            # Mainkan suara jika warna berubah
            if detected_color != self.last_detected_color and detected_color != "Unknown":
                play_sound_for_color(detected_color)
                self.last_detected_color = detected_color
                self.output_generated = True
                self.cap.release()
                break

        self.output_generated = False

    def reset_button_clicked(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.last_detected_color = "Unknown"
        self.output_generated = False
        self.label.setText("Detected Colour")
        self.textEdit.clear()
        self.graphicsView.setScene(None)
        self.on_cam_button_clicked()

    def convert_cv_qt(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_img)

    def exit_button_clicked(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        QApplication.quit()

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

    def about_message(self):
        QMessageBox.about(self, "About", 
            "Aplikasi Pendeteksi Warna ini dibuat oleh:\n\n"
            "Muhamad Naufal\n"
            "Mahasiswa Teknik Informatika\n"
            "Universitas Cendekia Abditama\n"
            "NIM: 12001011\n\n"
            "Pembimbing: Dr. Muhammad Subali, S.Si, M.T")


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()