import sys
import subprocess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QDialog, QRubberBand,
                             QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QSpacerItem, QSpinBox, QButtonGroup, QRadioButton)


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("oxipng")
        self.setGeometry(400, 300, 800, 600)

        self.cbInterlacing = QCheckBox('Interlacing')

        optimizationLabel = QLabel(self)
        optimizationLabel.setText("Optimization level: ")
        self.optimizationSpinBox = QSpinBox()
        self.optimizationSpinBox.setMaximum(6)
        self.optimizationSpinBox.setMinimum(0)
        optimizationLabelLayout = QHBoxLayout()
        optimizationLabelLayout.addWidget(optimizationLabel)
        optimizationLabelLayout.addWidget(self.optimizationSpinBox)

        removeMetadataLabel = QLabel(self)
        removeMetadataLabel.setText("Remove metadata: ")
        self.rbGroupRemoveMetadata = QButtonGroup()
        self.rbRemoveMetadataAll = QRadioButton("All")
        self.rbRemoveMetadataSafe = QRadioButton("Safe")
        self.rbGroupRemoveMetadata.addButton(self.rbRemoveMetadataAll)
        self.rbGroupRemoveMetadata.addButton(self.rbRemoveMetadataSafe)
        removeMetadataLayout = QHBoxLayout()
        removeMetadataLayout.addWidget(removeMetadataLabel)
        removeMetadataLayout.addWidget(self.rbRemoveMetadataSafe)
        removeMetadataLayout.addWidget(self.rbRemoveMetadataAll)

        groupBox = QGroupBox("Options")
        layout = QHBoxLayout()
        layout.addWidget(self.cbInterlacing)
        layout.addSpacing(20)
        layout.addLayout(optimizationLabelLayout)
        layout.addSpacing(20)
        layout.addLayout(removeMetadataLayout)
        groupBox.setLayout(layout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(groupBox, 0, 0)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
