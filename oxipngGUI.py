import sys
import subprocess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QDialog,
                             QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QPushButton, QFileDialog, QLabel)


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("oxipng")
        self.setGeometry(400, 300, 800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
