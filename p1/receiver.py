import sys
import pyaudio
import threading
import numpy as np
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QDialog,
    QTextEdit,
    QApplication,
    QMessageBox,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from fsk import demodulate

class Dialog(QDialog):
    finished = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.top = 200
        self.left = 300
        self.width = 800
        self.height = 600
        self.title = '解码程序'

        self.frames = []
        self.recording = False

        self.res_text = QTextEdit()
        self.res_text.setEnabled(False)
        self.btn_start = QPushButton('开始录音')
        self.btn_start.clicked.connect(self.record)
        self.btn_stop = QPushButton('结束录音')
        self.btn_stop.clicked.connect(self.stop_record)

        self.finished.connect(self.set_result)

        self.init_ui()

    def init_ui(self):
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btn_start)
        self.hbox.addWidget(self.btn_stop)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.res_text)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def record(self):
        threading.Thread(target=self.start_record).start()

    def start_record(self):
        self.frames = []
        self.recording = True

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=48000,
            input=True,
        )

        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.get_result()

    def stop_record(self):
        self.recording = False

    def set_result(self, result):
        self.res_text.setText(result)
        QMessageBox.information(None, '提示', 'fuck you!!!')

    def get_result(self):
        data = np.frombuffer(b''.join(self.frames), dtype=np.int16)
        result = demodulate(data / (2 ** 15))
        baud = 10
        _r = []
        offset = int(48000 / (baud * 2))
        for i in range(len(result)//(48000 // baud)):
            idx = i * 48000 // baud + offset
            _r.append(int(result[idx]))
        self.finished.emit(''.join(map(lambda x: str(x), _r)))


def main():
    app = QApplication(sys.argv)
    dialog = Dialog()
    app.exec_()


if __name__ == '__main__':
    main()
