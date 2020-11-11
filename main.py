from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from Design.MainWindow import Ui_MainWindow
from funcoes.poupUp import Error
from funcoes.criptografia import gerar_chaves, cifrar_mensagem, descriptar_mensagem
import sys


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        #Variaveis do Sistema
        self.chavePublica = None
        self.chavePrivada = None
        self.msg = Error()
        self.statusMsg = True
        self.carregar_cfg()

        self.stackedWidget.setCurrentIndex(1)  # Define a tela inicial
        self.ln_chaveSistema_chavePublica.textChanged.connect(lambda: self.salvar_cfg())
        self.ln_chaveSistema_chavePrivada.textChanged.connect(lambda: self.salvar_cfg())

        #  Navegação
        self.actionEncriptar.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionGerar_Chaves.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.actionDescriptar.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        # Janela - Gerenciamento de Chaves
        self.btn_nChave_gerarChave.clicked.connect(lambda: self.criar_nova_chave())
        self.btn_nChave_inserirSistema.clicked.connect(lambda: self.inserir_chave_sistema())
        self.btn_nChave_exportChave.clicked.connect(lambda: self.exportar_chave())
        self.btn_chaveSistema_editarChave.clicked.connect(lambda: self.editar_chave_sistema())

        #  Janela - Descriptografar
        self.btn_descriptografar_editChave.clicked.connect(lambda: self.editar_chave_temporaria())
        self.btn_descriptografar_descriptar.clicked.connect(lambda: self.descriptografar_mensagem())
        self.btn_descriptografar_exportar.clicked.connect(lambda: self.exportar_texto(self.txed_descriptografar_texto))

        #  Janela - Criptografar
        self.btn_criptografar_encriptar.clicked.connect(lambda: self.criptografar_mensagem())
        self.txed_criptografar_texto.textChanged.connect(lambda: self.limitar_texto())
        self.btn_criptografar_exportar.clicked.connect(lambda: self.exportar_texto(self.txed_criptografar_texto))
        self.btn_criptografar_limpar.clicked.connect(lambda: self.limpar_txed_criptografia())

    def atualizar(self):  # Atualiza os campos onde são exibidas as chaves do sistema
        self.ln_descriptografar_chavePrivada.setText(self.chavePrivada)
        self.ln_descriptografar_chavePublica.setText(self.chavePublica)
        self.ln_chaveSistema_chavePrivada.setText(self.chavePrivada)
        self.ln_chaveSistema_chavePublica.setText(self.chavePublica)
        self.ln_criptografar_chavePublica.setText(self.chavePublica)

    def criar_nova_chave(self):  # Gera novas chaves RSA
        chaves = gerar_chaves()
        chave_privada = chaves[1]
        chave_publica = chaves[0]
        self.ln_nChave_chavePrivada.setEnabled(True)
        self.ln_nchave_chavePublica.setEnabled(True)
        self.ln_nChave_chavePrivada.setText(str(chave_privada))
        self.ln_nchave_chavePublica.setText(str(chave_publica))

    def inserir_chave_sistema(self):  # Define a chave gerada como padrão do sistema
        self.chavePrivada = self.ln_nChave_chavePrivada.text()
        self.chavePublica = self.ln_nchave_chavePublica.text()
        self.atualizar()

    def exportar_chave(self):  # Exporta as chaves geradas para um arquivo .txt
        dir_ = QFileDialog.getSaveFileName(None, 'Save File:', 'keys', "Text files (*.txt)")
        try:
            if self.ln_nChave_chavePrivada.text() != "" and self.ln_nchave_chavePublica.text() != "":
                with open(dir_[0], "w") as Key:
                    Key.write("Chave Privada: {}".format(self.ln_nChave_chavePrivada.text()))
                    Key.write("\nChave Publica: {}\n".format(self.ln_nchave_chavePublica.text()))
        except FileNotFoundError:
            pass

    def exportar_texto(self, texto):
        dir_ = QFileDialog.getSaveFileName(None, 'Save File:', 'Mensagem', "Text files (*.txt)")
        try:
            if texto.toPlainText() != "":
                with open(dir_[0], "w") as Mensagem:
                    Mensagem.write(texto.toPlainText())
        except FileNotFoundError:
            pass

    def editar_chave_sistema(self):  # Edita e salva a chave padrão do sistema
        if self.btn_chaveSistema_editarChave.isChecked():
            self.ln_chaveSistema_chavePrivada.setReadOnly(False)
            self.ln_chaveSistema_chavePublica.setReadOnly(False)
        else:
            self.ln_chaveSistema_chavePrivada.setReadOnly(True)
            self.ln_chaveSistema_chavePublica.setReadOnly(True)

        self.chavePrivada = self.ln_chaveSistema_chavePrivada.text()
        self.chavePublica = self.ln_chaveSistema_chavePublica.text()
        self.atualizar()
        self.salvar_cfg()

    def editar_chave_temporaria(self):  # Edita as chaves usadas na Descriptografia
        if self.btn_descriptografar_editChave.isChecked():
            self.ln_descriptografar_chavePublica.setEnabled(True)
            self.ln_descriptografar_chavePrivada.setEnabled(True)
        else:
            self.ln_descriptografar_chavePublica.setEnabled(False)
            self.ln_descriptografar_chavePrivada.setEnabled(False)

    def salvar_cfg(self):  # Salva as chaves padrão do sistema para serem carregadas ao iniciar
        with open("cfg.txt", "w") as Key:
            Key.write(self.chavePrivada)
            Key.write("\n" + self.chavePublica)

    def carregar_cfg(self):  # Carrega as chaves padrão do sistema caso existam
        keys = []
        try:
            with open("cfg.txt", "r") as Key:
                try:
                    for i in Key.readlines():
                        keys.append(i)
                    self.chavePrivada = keys[0].replace("\n", "")
                    self.chavePublica = keys[1]
                    self.atualizar()
                except IndexError:
                    pass
        except FileNotFoundError:
            pass

    def criptografar_mensagem(self):  # Criptografa a mensagem informada
        try:
            self.statusMsg = False
            self.txed_criptografar_texto.setReadOnly(True)
            chave_publica = self.limpar_chaves(self.ln_criptografar_chavePublica.text())
            mensagem = self.txed_criptografar_texto.toPlainText()
            mensagem_criptografada = cifrar_mensagem(mensagem, chave_publica[1], chave_publica[0])
            self.txed_criptografar_texto.setText(self.gerar_string(mensagem_criptografada))
        except ValueError:
            self.msg.definir_texto("Informe uma Chave")
            self.msg.show()

    def descriptografar_mensagem(self):  # Descriptografa a mensagem informada
        try:
            chave_privada = self.limpar_chaves(self.ln_descriptografar_chavePrivada.text())
            mensagem = self.gerar_lista(self.txed_descriptografar_texto.toPlainText())
            mensagem_descriptografada = descriptar_mensagem(mensagem, chave_privada[1], chave_privada[0])
            self.txed_descriptografar_texto.setText(mensagem_descriptografada)
        except ValueError:
            self.msg.definir_texto("Informe as Chaves")
            self.msg.show()

    def limpar_chaves(self, chaves):  # Remove as chave da lista às tranformando em uma strings separadas
        key_1 = ""
        key_2 = ""
        key = chaves.replace("[", "")
        key = key.replace("]", "")
        key = key.replace(" ", "")
        for frase in key:
            if frase == ",":
                break
            key_1 += frase
        key = key.replace("{},".format(key_1), "")
        for frase in key:
            key_2 += frase
        return int(key_1), int(key_2)

    def gerar_string(self, mensagem):  # Remove a mensagem criptografada da lista e a transforma em uma string legivel
        msg = ""
        for i in mensagem:
            msg += str(i) + " "
        return msg

    def gerar_lista(self, mensagem):  # Converte a string de texto em uma lista para executar a descriptografia
        lista = [""]
        count = 0
        for i in mensagem:
            if i == " ":
                count += 1
                lista.append("")
            else:
                lista[count] += i
        del(lista[-1])
        return lista

    def limitar_texto(self):
        if self.statusMsg == True:
            mensagem = self.txed_criptografar_texto.toPlainText()
            if len(mensagem) > 128:
                mensg = []
                strin = ""
                for i in mensagem:
                    mensg.append(i)
                while len(mensg) > 128:
                    mensg.pop(-1)
                for i in mensg:
                    strin += i
                self.msg.definir_texto("Tamanho máximo de caracteres atingido atingido.\n(max.128)")
                self.msg.show()
                self.txed_criptografar_texto.setText(strin)

    def limpar_txed_criptografia(self):
        self.statusMsg = False
        self.txed_criptografar_texto.setReadOnly(False)
        self.txed_criptografar_texto.setText("")

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    App = Main()
    App.show()
    qt.exec_()
