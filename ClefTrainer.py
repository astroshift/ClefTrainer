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
    QComboBox,
)

# base path
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

        self.notes = [QPushButton('A'), QPushButton('B'), QPushButton('C'),
                      QPushButton('D'), QPushButton('E'), QPushButton('F'),
                      QPushButton('G')
                      ]

        # used to save clef images
        self.imageStack = QStackedWidget(self)
        self.chosen_clef = []

        # guessed note is made globally available
        self.note_to_guess = None

        # select which clef (default none), begin by prompting user
        self.user_choice = None
        self.spawn_prompt()

    def spawn_prompt(self):
        init_prompt = QWidget()
        prompt_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        '''
        ## primitive rounds implementation, come back later
        rounds_layout = QHBoxLayout()
        
    
        self.selected_rounds = 0

        dropdown_menu = QComboBox()
        for i in range(0, 100):
            dropdown_menu.addItem(str(i))
            dropdown_menu.activated(i).connect(self.dropdown_select())

        rounds_layout.addWidget(QLabel("Rounds Played: "))
        rounds_layout.addWidget(dropdown_menu)
        '''

        buttons = [QPushButton('Treble'), QPushButton('Bass')]
        buttons[0].clicked.connect(self.select_treble)
        buttons[1].clicked.connect(self.select_bass)
        for x in buttons:
            button_layout.addWidget(x)

        prompt_layout.addLayout(button_layout)
        init_prompt.setLayout(prompt_layout)

        self.setCentralWidget(init_prompt)
        self.show()

    def select_treble(self):
        self.spawn_clef('treble-clef')

    def select_bass(self):
        self.spawn_clef('bass-clef')

    def generate_note(self):
        # randomize note with number for repeat usage
        note_num = random.randint(0, 16)
        self.note_to_guess = self.chosen_clef[note_num][0]
        self.imageStack.setCurrentIndex(note_num)

    def check_guess(self):
        # compare pressed note with guessed note
        sending_button = self.sender()
        if sending_button.text() == self.note_to_guess:
            self.generate_note()

    def spawn_clef(self, user_choice):
        pageLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        self.chosen_clef = os.listdir(os.path.join(bundle_dir, user_choice))

        # iterate image list and add to stack
        for loc in self.chosen_clef:
            pixmap = QPixmap(os.path.join(bundle_dir, user_choice, loc))
            image = QLabel(self)
            image.setPixmap(pixmap)
            image.setScaledContents(True)
            self.imageStack.addWidget(image)

        # preemptively generate new note for guessing
        self.generate_note()

        # add all buttons and enable functionality
        for note in self.notes:
            buttonLayout.addWidget(note)
            note.clicked.connect(self.check_guess)

        pageLayout.addWidget(self.imageStack)
        pageLayout.addLayout(buttonLayout)

        container = QWidget()
        container.setLayout(pageLayout)

        self.setCentralWidget(container)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
