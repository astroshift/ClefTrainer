# ------------------------------------------------
# Bass Clef (Treble soon) Training Application
# Take images from folder and then quiz user

import os
import sys
import random

from PyQt6.QtGui import *
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QApplication,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QStackedWidget,
)

bundle_dir = os.path.dirname(__file__)

try:
    from ctypes import windll
    myappid = u'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClefTrainer")

        self.setWindowIcon(
            QIcon(os.path.join(bundle_dir, 'icons', 'ct-icon.png')))

        pageLayout = QVBoxLayout(self)
        buttonLayout = QHBoxLayout(self)
        self.imageStack = QStackedWidget(self)

        self.note_list = \
            ('bass-clef\A.jpg', 'bass-clef\B.jpg', 'bass-clef\C.jpg',
             'bass-clef\D.jpg', 'bass-clef\E.jpg', 'bass-clef\F.jpg',
             'bass-clef\G.jpg', 'bass-clef\lowA.jpg',
             'bass-clef\lowB.jpg', 'bass-clef\lowC.jpg',
             'bass-clef\lowD.jpg', 'bass-clef\lowE.jpg',
             'bass-clef\lowF.jpg', 'bass-clef\lowG.jpg',
             'bass-clef\lowestC.jpg', 'bass-clef\lowestD.jpg',
             'bass-clef\lowestE.jpg'
             )

        notes = [QPushButton('A'), QPushButton('B'), QPushButton('C'),
                 QPushButton('D'), QPushButton('E'), QPushButton('F'),
                 QPushButton('G')
                 ]

        pageLayout.addWidget(self.imageStack)
        pageLayout.addLayout(buttonLayout)

        # iterate image list and add to stack
        for loc in self.note_list:
            pixmap = QPixmap(os.path.join(bundle_dir, loc))
            image = QLabel(self)
            image.setPixmap(pixmap)
            image.setScaledContents(True)
            self.imageStack.addWidget(image)

        # add all buttons and enable functionality
        for note in notes:
            buttonLayout.addWidget(note)
            note.clicked.connect(self.button_pressed)

        # generate a note name to guess and random number for further usage
        self.note_to_guess = None
        self.note_num = None
        self.generate_note()

        container = QWidget()
        container.setLayout(pageLayout)

        self.setCentralWidget(container)
        self.show()

    def button_pressed(self):
        sending_button = self.sender()
        if sending_button.text() == self.note_to_guess:
            self.generate_note()

    def generate_note(self):
        self.note_num = random.randint(0, 16)
        self.note_to_guess = self.note_list[self.note_num][-5]
        self.imageStack.setCurrentIndex(self.note_num)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
