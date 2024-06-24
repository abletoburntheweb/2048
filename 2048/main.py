import json
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

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
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

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()

class Game2048(QWidget):
    mode_config = {
        '4x4': {'window_size': (600, 700), 'cell_size': 140, 'font_size': 35},
        '5x5': {'window_size': (700, 800), 'cell_size': 112, 'font_size': 30},
        '6x6': {'window_size': (800, 900), 'cell_size': 93, 'font_size': 25},
        '8x8': {'window_size': (900, 1000), 'cell_size': 70, 'font_size': 20},
    }
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.grid_size = int(mode[0])
        self.config = self.mode_config[mode]
        self.initUI()
        self.startGame()

    def initUI(self):
        self.setWindowTitle(f'2048 - {self.mode}')
        self.setFixedSize(*self.config['window_size'])
        self.setWindowIcon(QIcon('2048.ico'))
        self.setStyleSheet("QWidget { background-color: #f9f6f2; }")

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)

        self.labels = [[QLabel() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                label = self.labels[i][j]
                label.setFont(QFont('Sans Serif', self.config['font_size'], QFont.Bold))
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(self.config['cell_size'], self.config['cell_size'])
                label.setStyleSheet("""
                    QLabel {
                        background-color: #cdc1b4;
                        border-radius: 10px;
                        color: #776e65;
                    }
                """)
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

        self.show()

    def saveHighScore(self):
        with open('high_score.json', 'w') as f:
            json.dump({'high_score': self.high_score}, f)

    def loadHighScore(self):
        try:
            with open('high_score.json', 'r') as f:
                data = json.load(f)
                self.high_score = data.get('high_score', 0)
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def startGame(self):
        self.loadHighScore()
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.history = []
        self.addRandomTile()
        self.addRandomTile()
        self.updateUI()
        self.setFocus()

    def updateScore(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.saveHighScore()
        self.score_label.setText(f"Счёт: {self.score}")
        self.high_score_label.setText(f"Рекорд: {self.high_score}")

    def updateUI(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                label = self.labels[i][j]
                label.setText(str(value) if value != 0 else '')
                label.setStyleSheet(f"""
                    QLabel {{
                        background-color: {self.getTileColor(value)};
                        border-radius: 10px;
                        color: {self.getTileTextColor(value)};
                    }}
                """)
        self.updateScore(0)

    def getTileColor(self, value):
        colors = {
            0: '#cdc1b4', 2: '#eee4da', 4: '#ede0c8', 8: '#f2b179',
            16: '#f59563', 32: '#f67c5f', 64: '#f65e3b', 128: '#edcf72',
            256: '#edcc61', 512: '#edc850', 1024: '#edc53f', 2048: '#edc22e'
        }
        return colors.get(value, '#3c3a32')

    def getTileTextColor(self, value):
        return '#776e65' if value < 8 else '#f9f6f2'

    def addRandomTile(self):
        empty_tiles = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 4 if random.random() < 0.1 else 2

    def move(self, direction):
        self.history.append((self.score, [row[:] for row in self.board]))
        moved = False
        if direction == 'up':
            for j in range(self.grid_size):
                tiles = [self.board[i][j] for i in range(self.grid_size) if self.board[i][j] != 0]
                for k in range(len(tiles) - 1):
                    if tiles[k] == tiles[k + 1]:
                        tiles[k] *= 2
                        self.updateScore(tiles[k])
                        tiles[k + 1] = 0
                tiles = [tile for tile in tiles if tile != 0]
                tiles.extend([0] * (self.grid_size - len(tiles)))
                for i in range(self.grid_size):
                    if self.board[i][j] != tiles[i]:
                        self.board[i][j] = tiles[i]
                        moved = True
        elif direction == 'down':
            for j in range(self.grid_size):
                tiles = [self.board[i][j] for i in range(self.grid_size) if self.board[i][j] != 0]
                for k in range(len(tiles) - 1, 0, -1):
                    if tiles[k] == tiles[k - 1]:
                        tiles[k] *= 2
                        self.updateScore(tiles[k])
                        tiles[k - 1] = 0
                tiles = [tile for tile in tiles if tile != 0]
                tiles = [0] * (self.grid_size - len(tiles)) + tiles
                for i in range(self.grid_size):
                    if self.board[i][j] != tiles[i]:
                        self.board[i][j] = tiles[i]
                        moved = True
        elif direction == 'left':
            for i in range(self.grid_size):
                tiles = [self.board[i][j] for j in range(self.grid_size) if self.board[i][j] != 0]
                for k in range(len(tiles) - 1):
                    if tiles[k] == tiles[k + 1]:
                        tiles[k] *= 2
                        self.updateScore(tiles[k])
                        tiles[k + 1] = 0
                tiles = [tile for tile in tiles if tile != 0]
                tiles.extend([0] * (self.grid_size - len(tiles)))
                for j in range(self.grid_size):
                    if self.board[i][j] != tiles[j]:
                        self.board[i][j] = tiles[j]
                        moved = True
        elif direction == 'right':
            for i in range(self.grid_size):
                tiles = [self.board[i][j] for j in range(self.grid_size) if self.board[i][j] != 0]
                for k in range(len(tiles) - 1, 0, -1):
                    if tiles[k] == tiles[k - 1]:
                        tiles[k] *= 2
                        self.updateScore(tiles[k])
                        tiles[k - 1] = 0
                tiles = [tile for tile in tiles if tile != 0]
                tiles = [0] * (self.grid_size - len(tiles)) + tiles
                for j in range(self.grid_size):
                    if self.board[i][j] != tiles[j]:
                        self.board[i][j] = tiles[j]
                        moved = True

        if moved:
            self.addRandomTile()
            self.updateUI()
            if not self.canMove():
                self.showGameOverMessage()

    def undo(self):
        if self.history:
            self.score, self.board = self.history.pop()
            self.updateUI()

    def canMove(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return True
                if i < self.grid_size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return True
                if j < self.grid_size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return True
        return False

    def showGameOverMessage(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Игра окончена")
        msg_box.setText("Игра окончена. Ваш счёт: {}".format(self.score))
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.move('up')
        elif key == Qt.Key_Down:
            self.move('down')
        elif key == Qt.Key_Left:
            self.move('left')
        elif key == Qt.Key_Right:
            self.move('right')
        elif key == Qt.Key_Escape:
            self.close()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Z and (event.modifiers() & Qt.ControlModifier):
                self.undo()
                return True
        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())