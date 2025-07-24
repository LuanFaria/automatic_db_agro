import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QWidget,
    QMessageBox,
    QLabel,
    QFrame,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import usinas


class UsinaInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel de Processamento de Usinas")
        self.setGeometry(100, 100, 700, 500)

        self.lista_usina = ["Santa Adélia", "Estiva", "Aralco", "Cocal"]

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(30)

        # Título com barra lateral
        self.title_bar = QLabel("  Gerar Base BD_AGRO")
        self.title_bar.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.title_bar.setStyleSheet("""
            QLabel {
                color: #2E3A59;
                border-left: 6px solid #1976D2;
                padding-left: 12px;
            }
        """)
        self.layout.addWidget(self.title_bar)

        # Card de seleção
        self.card = QWidget()
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(30, 30, 30, 30)
        self.card_layout.setSpacing(20)
        self.card.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        """)

        # Usina
        self.usina_label = QLabel("Selecionar usina:")
        self.usina_label.setFont(QFont("Segoe UI", 11))
        self.card_layout.addWidget(self.usina_label)

        self.combo_box = QComboBox()
        self.combo_box.setFont(QFont("Segoe UI", 11))
        self.combo_box.addItems(self.lista_usina)
        self.combo_box.setStyleSheet(self.combo_style())
        self.card_layout.addWidget(self.combo_box)

        # Arquivo
        self.arquivo_label = QLabel("Selecionar planilha CSV:")
        self.arquivo_label.setFont(QFont("Segoe UI", 11))
        self.card_layout.addWidget(self.arquivo_label)

        self.arquivo_combo = QComboBox()
        self.arquivo_combo.setFont(QFont("Segoe UI", 11))

        arquivos_input = [f for f in os.listdir("input") if f.lower().endswith(".csv")]
        if not arquivos_input:
            arquivos_input = ["<nenhum arquivo encontrado>"]

        self.arquivo_combo.addItems(arquivos_input)
        self.arquivo_combo.setStyleSheet(self.combo_style())
        self.card_layout.addWidget(self.arquivo_combo)

        # Botão de processamento
        self.select_button = QPushButton("Gerar Planilha BD_AGRO")
        self.select_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.select_button.setStyleSheet(self.button_style())
        self.select_button.clicked.connect(self.selecionar_usina)
        self.card_layout.addWidget(self.select_button)

        self.layout.addWidget(self.card)

        # Estilo geral da janela
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F2F5;
            }
            QLabel {
                color: #333;
            }
        """)

    def combo_style(self):
        return """
            QComboBox {
                background-color: #FAFAFA;
                border: 1px solid #C5CAE9;
                border-radius: 6px;
                padding: 6px;
            }
            QComboBox:hover {
                border: 1px solid #1976D2;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """

    def selecionar_usina(self):
        usina = self.combo_box.currentText()
        view_usina = self.arquivo_combo.currentText()

        if not view_usina or view_usina == "<nenhum arquivo encontrado>":
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo CSV encontrado na pasta 'input'.")
            return

        try:
            view_usina_nome = os.path.splitext(view_usina)[0]

            if usina == "Santa Adélia":
                usinas.santa_adelia(view_usina_nome)
            elif usina == "Estiva":
                usinas.estiva(view_usina_nome)
            elif usina == "Aralco":
                usinas.aralco(view_usina_nome)
            elif usina == "Cocal":
                usinas.cocal(view_usina_nome)
            else:
                raise ValueError("Função para a usina selecionada não encontrada!")

            QMessageBox.information(self, "Sucesso", f"✅ Planilha BD_AGRO da usina {usina} exportada com sucesso!")

        except AttributeError:
            QMessageBox.critical(self, "Erro", f"Função para {usina} não definida no módulo 'usinas'.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UsinaInterface()
    window.show()
    sys.exit(app.exec_())
