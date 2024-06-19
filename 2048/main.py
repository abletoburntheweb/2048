import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QMessageBox, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QEvent

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('2048 - Главное меню')
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('2048.ico'))
        self.setStyleSheet("QWidget { background-color: #f9f6f2; }")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        self.title = QLabel("2048")
        self.title.setFont(QFont('Sans Serif', 50, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.play_button = QPushButton("Играть")
        self.play_button.setFont(QFont('Sans Serif', 30, QFont.Bold))
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #8f7a66;
                color: #f9f6f2;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:pressed {
                background-color: #7a6a57;
            }
        """)
        self.play_button.clicked.connect(self.showModeSelection)
        self.layout.addWidget(self.play_button)

        self.exit_button = QPushButton("Выход")
        self.exit_button.setFont(QFont('Sans Serif', 30, QFont.Bold))
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #8f7a66;
                color: #f9f6f2;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:pressed {
                background-color: #7a6a57;
            }
        """)
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    def showModeSelection(self):
        self.mode_selection = ModeSelection()
        self.mode_selection.show()
        self.close()

class ModeSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('2048 - Выбор режима')
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('2048.ico'))
        self.setStyleSheet("QWidget { background-color: #f9f6f2; }")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        self.title = QLabel("Выберите режим игры")
        self.title.setFont(QFont('Sans Serif', 30, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.buttons = {
            '4x4': QPushButton("4x4"),
            '5x5': QPushButton("5x5"),
            '6x6': QPushButton("6x6"),
            '8x8': QPushButton("8x8"),
        }

        for key, button in self.buttons.items():
            button.setFont(QFont('Sans Serif', 30, QFont.Bold))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #8f7a66;
                    color: #f9f6f2;
                    border: none;
                    border-radius: 10px;
                    padding: 15px;
                }
                QPushButton:pressed {
                    background-color: #7a6a57;
                }
            """)
            button.clicked.connect(lambda checked, k=key: self.startGame(k))
            self.layout.addWidget(button)

        self.setLayout(self.layout)

    def startGame(self, mode):
        self.game = Game2048(mode)
        self.game.show()
        self.close()

class Game2048(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.grid_size = int(mode[0])
        self.initUI()
        self.startGame()

    def initUI(self):
        self.setWindowTitle(f'2048 - {self.mode}')
        self.setFixedSize(600, 700)
        self.setWindowIcon(QIcon('2048.ico'))
        self.setStyleSheet("QWidget { background-color: #f9f6f2; }")

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)

        self.labels = [[QLabel() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                label = self.labels[i][j]
                label.setFont(QFont('Sans Serif', 35 if self.grid_size == 4 else 30, QFont.Bold))
                label.setAlignment(Qt.AlignCenter)
                label.setMinimumSize(600 // self.grid_size - 20, 600 // self.grid_size - 20)
                label.setStyleSheet("QLabel { background-color: #cdc1b4; border-radius: 10px; }")
                self.grid_layout.addWidget(label, i, j)

        self.score_label = QLabel("Счёт: 0")
        self.high_score_label = QLabel("Рекорд: 0")
        self.score_label.setFont(QFont('Sans Serif', 20, QFont.Bold))
        self.high_score_label.setFont(QFont('Sans Serif', 20, QFont.Bold))
        self.score_label.setAlignment(Qt.AlignCenter)
        self.high_score_label.setAlignment(Qt.AlignCenter)

        self.undo_button = QPushButton("Отмена")
        self.undo_button.setFont(QFont('Sans Serif', 20, QFont.Bold))
        self.undo_button.clicked.connect(self.undo)
        self.undo_button.setStyleSheet("""
            QPushButton {
                background-color: #8f7a66;
                color: #f9f6f2;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:pressed {
                background-color: #7a6a57;
            }
        """)

        self.restart_button = QPushButton("Перезапуск")
        self.restart_button.setFont(QFont('Sans Serif', 20, QFont.Bold))
        self.restart_button.clicked.connect(self.startGame)
        self.restart_button.setStyleSheet("""
            QPushButton {
                background-color: #8f7a66;
                color: #f9f6f2;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:pressed {
                background-color: #7a6a57;
            }
        """)

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.score_label)
        self.top_layout.addWidget(self.high_score_label)
        self.top_layout.setSpacing(50)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.undo_button)
        self.button_layout.addWidget(self.restart_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.setSpacing(20)

        self.setLayout(self.main_layout)

        self.undo_button.installEventFilter(self)

        self.show()

    def startGame(self):
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.high_score = 0
        self.history = []
        self.addRandomTile()
        self.addRandomTile()
        self.updateUI()

    def addRandomTile(self):
        emptyTiles = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.board[i][j] == 0]
        if emptyTiles:
            i, j = random.choice(emptyTiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def updateUI(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                label = self.labels[i][j]
                label.setText(str(value) if value else "")
                label.setStyleSheet("QLabel { background-color: %s; color: %s; border-radius: 10px; }" % (self.getTileColor(value)[0], self.getTileColor(value)[1]))
        self.score_label.setText(f"Счёт: {self.score}")
        self.high_score_label.setText(f"Рекорд: {self.high_score}")

    def getTileColor(self, value):
        color_dict = {
            0:    ("#cdc1b4", "#776e65"),
            2:    ("#eee4da", "#776e65"),
            4:    ("#ede0c8", "#776e65"),
            8:    ("#f2b179", "#f9f6f2"),
            16:   ("#f59563", "#f9f6f2"),
            32:   ("#f67c5f", "#f9f6f2"),
            64:   ("#f65e3b", "#f9f6f2"),
            128:  ("#edcf72", "#f9f6f2"),
            256:  ("#edcc61", "#f9f6f2"),
            512:  ("#edc850", "#f9f6f2"),
            1024: ("#edc53f", "#f9f6f2"),
            2048: ("#edc22e", "#f9f6f2"),
        }
        return color_dict.get(value, ("#3c3a32", "#f9f6f2"))

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            self.history.append((self.copyBoard(), self.score, self.high_score))
            moved = False
            if key == Qt.Key_Left:
                moved = self.moveLeft()
            elif key == Qt.Key_Right:
                moved = self.moveRight()
            elif key == Qt.Key_Up:
                moved = self.moveUp()
            elif key == Qt.Key_Down:
                moved = self.moveDown()

            if moved:
                self.addRandomTile()
                self.updateUI()
                if self.isGameOver():
                    self.showGameOver()
                elif self.hasWon():
                    self.showGameWon()
            else:
                self.history.pop()

    def copyBoard(self):
        return [row[:] for row in self.board]

    def moveLeft(self):
        moved = False
        for i in range(self.grid_size):
            new_row = [x for x in self.board[i] if x != 0]
            new_row += [0] * (self.grid_size - len(new_row))
            for j in range(self.grid_size - 1):
                if new_row[j] == new_row[j + 1] and new_row[j] != 0:
                    new_row[j] *= 2
                    new_row[j + 1] = 0
                    self.score += new_row[j]
                    if self.score > self.high_score:
                        self.high_score = self.score
                    moved = True
            new_row = [x for x in new_row if x != 0]
            new_row += [0] * (self.grid_size - len(new_row))
            if self.board[i] != new_row:
                self.board[i] = new_row
                moved = True
        return moved

    def moveRight(self):
        self.board = [row[::-1] for row in self.board]
        moved = self.moveLeft()
        self.board = [row[::-1] for row in self.board]
        return moved

    def moveUp(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.moveLeft()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def moveDown(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.moveRight()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def isGameOver(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return False
                if i < self.grid_size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j < self.grid_size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
        return True

    def hasWon(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def showGameOver(self):
        msg = QMessageBox()
        msg.setWindowTitle("Игра окончена")
        msg.setText("Игра окончена!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.startGame()

    def showGameWon(self):
        msg = QMessageBox()
        msg.setWindowTitle("Победа!")
        msg.setText("Поздравляем! Вы достигли 2048!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.startGame()

    def undo(self):
        if self.history:
            self.board, self.score, self.high_score = self.history.pop()
            self.updateUI()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down, Qt.Key_Escape):
            self.keyPressEvent(event)
            return True
        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())