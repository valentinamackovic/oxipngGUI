import sys
import subprocess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QDialog, QRubberBand, QWidget,
                             QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QSpacerItem, QSpinBox, QButtonGroup, QRadioButton)

options = {
    "optimization": "2",
    "interlacing": "1",
    "strip": "safe"
}

pictures = []


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

# OPTIONS-------
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

        self.moreOptionsButton = QPushButton("...")
        self.moreOptionsButton.setStyleSheet("QPushButton { background-color: transparent}"
                                             "QPushButton:pressed { background-color: transparent }")

        optionsGroupBox = QGroupBox("Options")
        optionsLayout = QHBoxLayout()
        optionsLayout.addWidget(self.cbInterlacing)
        optionsLayout.addSpacing(20)
        optionsLayout.addLayout(optimizationLabelLayout)
        optionsLayout.addSpacing(20)
        optionsLayout.addLayout(removeMetadataLayout)
        optionsLayout.addWidget(self.moreOptionsButton)
        optionsGroupBox.setLayout(optionsLayout)

# PICTURES CONTAINER-------
        self.addPictureButton = QPushButton("Add picture")
        self.addPictureButton.clicked.connect(self.openFileNamesDialog)
        self.compressPicturesButton = QPushButton("Compress")
        self.compressPicturesButton.clicked.connect(self.compressWithOxipng)
        self.compressPicturesButton.setDisabled(True)

        picturesGroupBox = QGroupBox("")
        picturesLayout = QVBoxLayout()
        self.picturesGrid = QGridLayout()
        picturesLayout.addLayout(self.picturesGrid)
        picturesLayout.addStretch(1)
        picturesLayout.addWidget(self.addPictureButton)
        picturesLayout.addWidget(self.compressPicturesButton)
        picturesGroupBox.setLayout(picturesLayout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(optionsGroupBox, 0, 0)
        mainLayout.addWidget(picturesGroupBox, 1, 0, 2, 0)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)
        self.setOptions()

    def setOptions(self):
        options['interlacing'] = "1" if self.cbInterlacing.isChecked() else "0"
        options['optimization'] = str(self.optimizationSpinBox.value())
        options['strip'] = 'safe' if self.rbRemoveMetadataSafe.isChecked() else 'all'

    def openFileNamesDialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.svg)")
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            pictures.append(fileNames[0])
            self.displayPictures()
            self.compressPicturesButton.setDisabled(False)

    def displayPictures(self):
        pictureBox = QLabel()
        pixmap = QPixmap(pictures[0])
        pixmapScaled = pixmap.scaled(70, 70)
        pictureBox.setPixmap(pixmapScaled)
        self.picturesGrid.addWidget(pictureBox)

    def compressWithOxipng(self):
        oxipngCommand = ["oxipng", "-o",
                         options["optimization"], "-i",
                         options["interlacing"], "--strip", options["strip"]]

        for picture in pictures:
            oxipngCommand.append(picture)
            compress = subprocess.Popen(oxipngCommand, stdout=subprocess.PIPE)
            output = compress.communicate()[0]
            print(output)

        for i in reversed(range(self.picturesGrid.count())):
            if(self.picturesGrid.itemAt(i).widget() != None):
                self.picturesGrid.itemAt(i).widget().deleteLater()

        self.compressPicturesButton.setDisabled(True)


class MoreOptionsWindow(QWidget):
    def __init__(self, parent=None):
        super(MoreOptionsWindow, self).__init__(parent)

        self.cbBackup = QCheckBox('Save a backup file')
        self.cbStdout = QCheckBox('Write to stdout instead of a file')
        self.cbFixErrors = QCheckBox(
            'Attempt to fix errors when decoding rather than returning Err')
        self.cbPretend = QCheckBox('Do not actually write any output')
        self.cbClobber = QCheckBox('Overwrite existing output files')
        self.cbCreate = QCheckBox(
            'Create new output files if they do not exist')
        self.cbForce = QCheckBox(
            'Write to output even if there was no improvement')
        self.cbPreserveAttr = QCheckBox(
            'Ensure that the output file has the sam epermission as the input file does')

        self.setWindowTitle("oxipng")
        self.setGeometry(400, 400, 600, 600)

        # add checkboxes to layout
        optionsGroupBox = QGroupBox("All Options")
        layout = QVBoxLayout()
        layout.addSpacing(5)
        layout.addWidget(self.cbBackup)
        layout.addSpacing(5)
        layout.addWidget(self.cbForce)
        layout.addSpacing(5)
        layout.addWidget(self.cbCreate)
        layout.addSpacing(5)
        layout.addWidget(self.cbClobber)
        layout.addSpacing(5)
        layout.addWidget(self.cbPretend)
        layout.addSpacing(5)
        layout.addWidget(self.cbPreserveAttr)
        layout.addSpacing(5)
        layout.addWidget(self.cbFixErrors)
        layout.addSpacing(5)
        layout.addWidget(self.cbStdout)
        layout.addStretch(1)
        optionsGroupBox.setLayout(layout)

        mainLayout = QGridLayout()
        self.backToMainWindowButton = QPushButton("Go back")
        self.backToMainWindowButton.setMaximumWidth(100)
        mainLayout.addWidget(self.backToMainWindowButton, 0, 0)
        mainLayout.addWidget(optionsGroupBox, 1, 0)

        self.setLayout(mainLayout)


class Application(QMainWindow):
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)
        self.setWindowTitle("oxipng")
        self.setGeometry(400, 300, 800, 600)
        self.startMainWindow()

    def startMainWindow(self):
        self.MainWindow = MainWindow(self)
        self.setWindowTitle("oxipng")
        self.setCentralWidget(self.MainWindow)
        self.MainWindow.moreOptionsButton.clicked.connect(
            self.startOptionsWindow)
        self.show()

    def startOptionsWindow(self):
        self.OptionsWindow = MoreOptionsWindow(self)
        self.setWindowTitle("oxipng/options")
        self.setCentralWidget(self.OptionsWindow)
        self.OptionsWindow.backToMainWindowButton.clicked.connect(
            self.startMainWindow)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Application()
    # mainWindow.show()
    app.exec_()
