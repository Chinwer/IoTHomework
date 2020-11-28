import sys
import math
import bitarray
import pyaudio
import numpy as np
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QDialog,
    QTextEdit,
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from packet import Packet
from fsk import modulate, bits_to_wave

class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.top = 200
        self.left = 300
        self.width = 800
        self.height = 600
        self.title = '编码调制程序'

        self.res_text = QTextEdit()
        self.res_text.setEnabled(False)
        self.input_text = QTextEdit()
        self.btn_gen = QPushButton('生成')
        self.btn_gen.clicked.connect(self.gen_bin_seq)
        self.btn_play = QPushButton('播放')

        self.init_ui()

    def init_ui(self):
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btn_gen)
        self.hbox.addWidget(self.btn_play)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.input_text)
        self.vbox.addWidget(self.res_text)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def gen_bin_seq(self):
        ba = bitarray.bitarray()
        text = self.input_text.toPlainText()
        _bytes = text.encode('utf-8')
        ba.frombytes(_bytes)
        self.res_text.setText(ba.to01())

        num = math.ceil(len(_bytes) / 256)
        for i in range(num):
            pkt = Packet(i, _bytes[i * 256: 256 * (i + 1)])
            data = pkt.make()
            bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
            self.play(modulate(bits_to_wave(bits)))

    def play(self, wave):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=48000,
            output=True
        )
        data = wave.astype(np.float32).tobytes()
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()


def main():
    app = QApplication(sys.argv)
    dialog = Dialog()
    app.exec_()


if __name__ == '__main__':
    main()
