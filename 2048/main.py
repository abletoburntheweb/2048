import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Game2048(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.startGame()

    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)
        self.setWindowTitle('2048')
        self.setFixedSize(500, 500)
        self.setStyleSheet("QWidget { background-color: #bbada0; }")

        self.labels = [[QLabel() for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                label = self.labels[i][j]
                label.setFont(QFont('Sans Serif', 35, QFont.Bold))
                label.setAlignment(Qt.AlignCenter)
                label.setMinimumSize(100, 100)
                self.grid.addWidget(label, i, j)

        self.show()

    def startGame(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.addRandomTile()
        self.addRandomTile()
        self.updateUI()

    def addRandomTile(self):
        emptyTiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if emptyTiles:
            i, j = random.choice(emptyTiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def updateUI(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                label = self.labels[i][j]
                label.setText(str(value) if value else "")
                label.setStyleSheet("QLabel { background-color: %s; color: %s; border-radius: 10px; }" % (self.getTileColor(value)[0], self.getTileColor(value)[1]))

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
        if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            moved = False
            if event.key() == Qt.Key_Left:
                moved = self.moveLeft()
            elif event.key() == Qt.Key_Right:
                moved = self.moveRight()
            elif event.key() == Qt.Key_Up:
                moved = self.moveUp()
            elif event.key() == Qt.Key_Down:
                moved = self.moveDown()

            if moved:
                self.addRandomTile()
                self.updateUI()
                if self.isGameOver():
                    self.showGameOver()
                elif self.hasWon():
                    self.showGameWon()

    def moveLeft(self):
        moved = False
        for i in range(4):
            new_row = [x for x in self.board[i] if x != 0]
            new_row += [0] * (4 - len(new_row))
            for j in range(3):
                if new_row[j] == new_row[j + 1] and new_row[j] != 0:
                    new_row[j] *= 2
                    new_row[j + 1] = 0
                    moved = True
            new_row = [x for x in new_row if x != 0]
            new_row += [0] * (4 - len(new_row))
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
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
        return True

    def hasWon(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def showGameOver(self):
        msg = QMessageBox()
        msg.setWindowTitle("Сообщение")
        msg.setText("Игра окончена!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.startGame()

    def showGameWon(self):
        msg = QMessageBox()
        msg.setWindowTitle("Победа!")
        msg.setText("Вы достигли 2048!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.startGame()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game2048()
    sys.exit(app.exec_())