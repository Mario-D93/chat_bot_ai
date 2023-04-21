from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QPushButton, QApplication, QFileDialog, QProgressDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPdfWriter, QPainter, QPageSize
from reportlab.pdfgen import canvas
from backend import ChatBot
import sys


class ChatWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.chatbot = ChatBot()

        self.setMinimumSize(1200, 900)

        # Output field widget
        self.output_field = QTextEdit(self)
        self.output_field.setGeometry(25, 0, 900, 700)
        self.output_field.setReadOnly(True)

        # Input field widget
        self.input_field = QTextEdit(self)
        self.input_field.setGeometry(25, 750, 900, 100)
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.input_field.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)


        # Send button
        self.button = QPushButton("Send", self)
        self.button.setGeometry(950, 750, 70, 40)
        self.button.clicked.connect(self.send_message)

        # Clear button
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(1030, 750, 70, 40)
        self.clear_button.clicked.connect(self.clear_chat_area)

        # Export as .csv button
        self.export_button = QPushButton("Export as .csv", self)
        self.export_button.setGeometry(950, 0, 110, 40)
        self.export_button.clicked.connect(self.export_csv)

        # Export as .pdf button
        self.pdf_button = QPushButton("Export as .pdf", self)
        self.pdf_button.setGeometry(950, 50, 110, 40)
        self.pdf_button.clicked.connect(self.export_pdf)

        self.show()

    def send_message(self):
        user_input = self.input_field.toPlainText().strip()
        self.output_field.append(f"<p style=color: #333333'><b>Me: </b> {user_input}</p>")

        self.input_field.clear()

        response = self.chatbot.get_response(user_input)
        self.output_field.append(f"<p style='color:#333333; background-color: #f2f2f2'><b>AI: </b>{response}</p><br>")

    def clear_chat_area(self):
        self.output_field.clear()

    def export_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export as .csv", ".", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.output_field.toPlainText())

    def export_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export as .pdf", ".", "PDF Files (*.pdf)")
        if file_name:
            pdf = QPdfWriter(file_name)
            pdf.setPageSize(QPageSize(self.output_field.size()))
            painter = QPainter(pdf)
            self.output_field.render(painter)
            painter.end()


app = QApplication(sys.argv)
main_window = ChatWindow()
sys.exit(app.exec())


