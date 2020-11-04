from PyQt5.QtWidgets import QMainWindow, QApplication
from Design.MainWindow import Ui_MainWindow
import sys


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        #  Navegação
        self.actionEncriptar_Mensagem.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.actionGerar_Chaves.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.actionDescriptar.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    App = Main()
    App.show()
    qt.exec_()
