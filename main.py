import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QWidget,
    QMessageBox,
    QLabel,
    QLineEdit,
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
import usinas  
class UsinaInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecionar Usina")
        self.setGeometry(100, 100, 500, 400)

        # Lista de usinas
        self.lista_usina = ["Santa Adélia", "Estiva", "Aralco", "Cocal"]

        # Configurar layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(20)

        # Adicionar título
        self.title_label = QLabel("Selecione a Usina")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # # Campo para o usuário inserir o valor de view_usina
        # self.view_usina_label = QLabel("Digite o valor de 'view_usina':")
        # self.view_usina_label.setFont(QFont("Arial", 12))
        # self.layout.addWidget(self.view_usina_label)

        self.view_usina_input = QLineEdit()
        self.view_usina_input.setFont(QFont("Arial", 12))
        self.view_usina_input.setPlaceholderText("Nome da planilha - Exemplo: estimativa_safra_202412101713")
        self.layout.addWidget(self.view_usina_input)

        # ComboBox para exibir as usinas
        self.combo_box = QComboBox()
        self.combo_box.setFont(QFont("Arial", 12))
        self.combo_box.addItems(self.lista_usina)
        self.layout.addWidget(self.combo_box)

        # Botão para confirmar a seleção
        self.select_button = QPushButton("Selecionar")
        self.select_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.select_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D7; 
                color: white; 
                border-radius: 8px; 
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            """
        )
        self.select_button.clicked.connect(self.selecionar_usina)
        self.layout.addWidget(self.select_button)

        # Personalizar cores
        self.set_palette()

    def set_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))  # Fundo azul claro
        palette.setColor(QPalette.WindowText, QColor("#0D47A1"))  # Texto azul escuro
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))  # Fundo do ComboBox
        palette.setColor(QPalette.Text, QColor("#0D47A1"))  # Texto do ComboBox
        palette.setColor(QPalette.Button, QColor("#2196F3"))  # Fundo do botão
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))  # Texto do botão
        self.setPalette(palette)

    def selecionar_usina(self):
        usina = self.combo_box.currentText()
        view_usina = self.view_usina_input.text().strip()

        if not view_usina:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um valor para 'view_usina'.")
            return

        try:
            if usina == "Santa Adélia":
                usinas.santa_adelia(view_usina)
            elif usina == "Estiva":
                usinas.estiva(view_usina)
            elif usina == "Aralco":
                usinas.aralco(view_usina)
            elif usina == "Cocal":
                usinas.cocal(view_usina)
            else:
                raise ValueError("Função para a usina selecionada não encontrada!")

            QMessageBox.information(self, "Sucesso", f"Planilha BD_AGRO da usina {usina} exportada com sucesso!")
        except AttributeError:
            QMessageBox.critical(self, "Erro", f"Função para {usina} não definida no módulo 'usinas'.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UsinaInterface()
    window.show()
    sys.exit(app.exec_())
