import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
import random


class ColoredCircleWidget(QWidget):

    def __init__(self, parent=None, circle_color: QColor = QColor('red')):
        super().__init__(parent)
        # self.color = color
        # Set initial properties
        self.circle_color = circle_color  # Red
        self.setAutoFillBackground(True)
        self.setMinimumSize(20, 20)

    # def mousePressEvent(self, event):
    #     # Change the circle's color when clicked
    #     self.circle_color = QColor(
    #         random.randint(0, 255),
    #         random.randint(0, 255),
    #         random.randint(0, 255)
    #     )
    #     self.update()  # Trigger a repaint

    def setColor(self, color: QColor):
        self.circle_color = color
        self.update()

    def paintEvent(self, event):
        # Paint the colored circle
        painter = QPainter(self)
        painter.setBrush(self.circle_color)
        painter.setPen(Qt.NoPen)

        width = self.width()
        height = self.height()

        # Ensure the circle fits within the widget
        radius = min(width, height) // 2

        painter.drawEllipse(
            (width - 2 * radius) // 2,
            (height - 2 * radius) // 2,
            2 * radius,
            2 * radius
        )
        painter.end()

def main():
    # Create a PyQt application
    app = QApplication(sys.argv)

    # Create an instance of the ColoredCircleWidget
    widget = ColoredCircleWidget(circle_color=QColor(0, 0, 255))
    widget.setWindowTitle("Custom Widget: Colored Circle - Click on it")
    widget.setColor(Qt.white)

    # Set the widget's size
    widget.setGeometry(100, 100, 300, 300)

    # Show the widget
    widget.show()

    # Run the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
