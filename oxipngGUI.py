import sys
import subprocess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QDialog, QRubberBand,
                             QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QSpacerItem, QSpinBox, QButtonGroup, QRadioButton)

options = {
    "optimization": 2,
    "interlacing": 1,
    "strip": "safe"
}


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("oxipng")
        self.setGeometry(400, 300, 800, 600)

        self.cbInterlacing = QCheckBox('Interlacing')
        self.cbInterlacing.setChecked(True)

        optimizationLabel = QLabel(self)
        optimizationLabel.setText("Optimization level: ")
        self.optimizationSpinBox = QSpinBox()
        self.optimizationSpinBox.setMaximum(6)
        self.optimizationSpinBox.setMinimum(0)
        self.optimizationSpinBox.setValue(2)
        optimizationLabelLayout = QHBoxLayout()
        optimizationLabelLayout.addWidget(optimizationLabel)
        optimizationLabelLayout.addWidget(self.optimizationSpinBox)

        removeMetadataLabel = QLabel(self)
        removeMetadataLabel.setText("Remove metadata: ")
        self.rbGroupRemoveMetadata = QButtonGroup()
        self.rbRemoveMetadataAll = QRadioButton("All")
        self.rbRemoveMetadataSafe = QRadioButton("Safe")
        self.rbRemoveMetadataSafe.setChecked(True)
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
        self.setOptions()

    def setOptions(self):
        options['interlacing'] = 1 if self.cbInterlacing.isChecked() else 0
        options['optimization'] = self.optimizationSpinBox.value()
        options['strip'] = 'safe' if self.rbRemoveMetadataSafe.isChecked() else 'all'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
