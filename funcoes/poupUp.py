from PyQt5.QtWidgets import QMessageBox


class Error(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Erro")

    def definir_texto(self, texto):
        self.setText(texto)