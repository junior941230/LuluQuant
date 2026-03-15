import sys
from PyQt6.QtWidgets import QApplication
from frontEnd.frontEnd import MainWindowController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindowController()
    window.show()
    a = app.exec()
    window.close()
    sys.exit(a)
