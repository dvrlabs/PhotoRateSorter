import os
import sys
import shutil
import glob
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class PhotoRateSorter(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creates a status bar.
        self.statusBar()

        # Create a menu bar
        self.menubar = self.menuBar()
        # One submenu is enough.
        self.fileMenu = self.menubar.addMenu('&Configure')

        # Create a label to hold the pixmap image
        self.photoLabel = QtWidgets.QLabel(self)
        self.photoLabel.setGeometry(100, 100, self.width(), self.height())

        # Define, create menubar actions
        self.addMenuAction("exit.png",
                           "&Exit",
                           "Ctrl+Q",
                           "Exit the program.",
                           qApp.quit)

        self.addMenuAction("folder.png",
                           "&Load",
                           "Ctrl+L",
                           "Load the photo of folders",
                           self.loadFolderPhotos)

        self.addMenuAction("output.png",
                           "&Output",
                           "Ctrl+O",
                           "Select the output folder",
                           self.loadOutputFolder)

        # Create back and forth buttons to browser the list of photos loaded.
        self.LeftPicScroll = QtWidgets.QPushButton(self)
        self.LeftPicScroll.setGeometry(1700, 100, 75, 75)
        self.LeftPicScroll.setText("<<")
        self.LeftPicScroll.setShortcut("Ctrl+,")
        self.LeftPicScroll.clicked.connect(self.scrollLeft)

        self.RightPicScroll = QtWidgets.QPushButton(self)
        self.RightPicScroll.setGeometry(1775, 100, 75, 75)
        self.RightPicScroll.setText(">>")
        self.RightPicScroll.setShortcut("Ctrl+.")
        self.RightPicScroll.clicked.connect(self.scrollRight)

        # Create a label to tell which photo out of X/MAX that the user is at
        self.locIndicator = QtWidgets.QLabel(self)
        self.locIndicator.setGeometry(1700, 25, 75, 75)
        self.locIndicator.setText("000/000")

        # Create the 5 buttons for rating 1 - 5, 1 bad, 5 great
        self.oneButton = QtWidgets.QPushButton(self)
        self.oneButton.setGeometry(1700, 175, 75, 75)
        self.oneButton.setText("1")
        self.oneButton.setShortcut("1")
        self.oneButton.clicked.connect(lambda: self.ratePhoto(1))

        self.twoButton = QtWidgets.QPushButton(self)
        self.twoButton.setGeometry(1700, 250, 75, 75)
        self.twoButton.setText("2")
        self.twoButton.setShortcut("2")
        self.twoButton.clicked.connect(lambda: self.ratePhoto(2))

        self.threeButton = QtWidgets.QPushButton(self)
        self.threeButton.setGeometry(1700, 325, 75, 75)
        self.threeButton.setText("3")
        self.threeButton.setShortcut("3")
        self.threeButton.clicked.connect(lambda: self.ratePhoto(3))

        self.fourButton = QtWidgets.QPushButton(self)
        self.fourButton.setGeometry(1700, 400, 75, 75)
        self.fourButton.setText("4")
        self.fourButton.setShortcut("4")
        self.fourButton.clicked.connect(lambda: self.ratePhoto(4))

        self.fiveButton = QtWidgets.QPushButton(self)
        self.fiveButton.setGeometry(1700, 475, 75, 75)
        self.fiveButton.setText("5")
        self.fiveButton.setShortcut("5")
        self.fiveButton.clicked.connect(lambda: self.ratePhoto(5))

    def addMenuAction(self, icon, name, shortcut, status, function):
        actName = f"{name[1:]}Action"
        setattr(self, actName, QAction(QIcon(icon), name, self))
        action = getattr(self, actName)
        action.setShortcut(shortcut)
        action.setStatusTip(status)
        action.triggered.connect(function)
        self.fileMenu.addAction(action)

    def loadFolderPhotos(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Folder of photos.')
        self.setStatusTip(f"Selected photo folder: {folderpath}")
        self.photos = glob.glob(f"{folderpath}/*")
        self.photos = [photo for photo in self.photos if "MOV" not in photo]

        self.currentListIndex = 0

        Image = QPixmap(self.photos[self.currentListIndex])
        scaledWidth = int(self.width()/1.25)
        scaledHeight = int(self.height()/1.25)
        Image = Image.scaled(scaledWidth, scaledHeight,
                             Qt.KeepAspectRatio, Qt.FastTransformation)
        self.photoLabel.setPixmap(Image)
        self.photoLabel.resize(scaledWidth, scaledHeight)

    def loadOutputFolder(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Folder of OUTPUT')
        directory = "OUTPUT"

        path = os.path.join(folderpath, directory)
        os.mkdir(path)

        path1 = os.path.join(path, "1")
        os.mkdir(path1)
        self.path1 = path1

        path2 = os.path.join(path, "2")
        os.mkdir(path2)
        self.path2 = path2

        path3 = os.path.join(path, "3")
        os.mkdir(path3)
        self.path3 = path3

        path4 = os.path.join(path, "4")
        os.mkdir(path4)
        self.path4 = path4

        path5 = os.path.join(path, "5")
        os.mkdir(path5)
        self.path5 = path5

        self.setStatusTip(f"OUTPUT FOLDER: {path}")

    def scrollLeft(self):
        if self.currentListIndex == 0:
            self.currentListIndex = len(self.photos) - 1
        else:
            self.currentListIndex -= 1

        Image = QPixmap(self.photos[self.currentListIndex])
        scaledWidth = int(self.width()/1.25)
        scaledHeight = int(self.height()/1.25)
        Image = Image.scaled(scaledWidth, scaledHeight,
                             Qt.KeepAspectRatio, Qt.FastTransformation)
        self.photoLabel.setPixmap(Image)
        self.photoLabel.resize(scaledWidth, scaledHeight)

        self.locIndicator.setText(
            f"{self.currentListIndex+1}/{len(self.photos) - 1}")

    def scrollRight(self):
        if self.currentListIndex == len(self.photos) - 1:
            self.currentListIndex = 0
        else:
            self.currentListIndex += 1

        Image = QPixmap(self.photos[self.currentListIndex])
        scaledWidth = int(self.width()/1.25)
        scaledHeight = int(self.height()/1.25)
        Image = Image.scaled(scaledWidth, scaledHeight,
                             Qt.KeepAspectRatio, Qt.FastTransformation)
        self.photoLabel.setPixmap(Image)
        self.photoLabel.resize(scaledWidth, scaledHeight)

        self.locIndicator.setText(
            f"{self.currentListIndex+1}/{len(self.photos) - 1}")

    def ratePhoto(self, rating):
        cpath = ""
        if rating == 1:
            cpath = self.path1
        if rating == 2:
            cpath = self.path2
        if rating == 3:
            cpath = self.path3
        if rating == 4:
            cpath = self.path4
        if rating == 5:
            cpath = self.path5

        shutil.copy(self.photos[self.currentListIndex], cpath)
        self.photos.pop(self.currentListIndex)
        self.scrollRight()


def main():
    app = QApplication(sys.argv)
    PRS = PhotoRateSorter()
    width = app.primaryScreen().size().width()
    height = app.primaryScreen().size().height()
    PRS.setGeometry(0, 0, width, height-50)
    PRS.setWindowTitle('Photo Rate Sorter')
    PRS.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
