import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QHBoxLayout, QListWidget,
    QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from src.email_manager import EmailManager

class IDSMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDS-Mail-Professional")
        self.resize(600, 400)

        self.email_manager = EmailManager()

        self.layout = QVBoxLayout()

        # Génération email
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Domaine (ex: example.com)")
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Nombre d'emails")
        self.count_input.setFixedWidth(120)
        self.generate_btn = QPushButton("Générer")
        self.generate_btn.clicked.connect(self.generate_emails)

        gen_layout = QHBoxLayout()
        gen_layout.addWidget(QLabel("Domaine:"))
        gen_layout.addWidget(self.domain_input)
        gen_layout.addWidget(QLabel("Nombre:"))
        gen_layout.addWidget(self.count_input)
        gen_layout.addWidget(self.generate_btn)
        self.layout.addLayout(gen_layout)

        # Recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un email")
        self.search_input.textChanged.connect(self.update_email_list)
        self.layout.addWidget(self.search_input)

        # Liste emails
        self.email_list = QListWidget()
        self.layout.addWidget(self.email_list)

        # Boutons suppression
        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Supprimer l'email sélectionné")
        self.delete_btn.clicked.connect(self.delete_selected_email)
        btn_layout.addWidget(self.delete_btn)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)
        self.update_email_list()

    def generate_emails(self):
        domain = self.domain_input.text().strip()
        count_text = self.count_input.text().strip()

        if not domain:
            QMessageBox.warning(self, "Erreur", "Le domaine ne peut pas être vide.")
            return

        if not count_text.isdigit() or int(count_text) <= 0:
            QMessageBox.warning(self, "Erreur", "Le nombre d'emails doit être un entier positif.")
            return

        count = int(count_text)
        generated = self.email_manager.generate_emails(domain, count)
        QMessageBox.information(self, "Succès", f"{len(generated)} emails générés.")
        self.update_email_list()

    def update_email_list(self):
        search = self.search_input.text().strip()
        emails = self.email_manager.get_emails(search)
        self.email_list.clear()
        for email_id, email, domain, created_at in emails:
            self.email_list.addItem(f"{email_id}: {email} (domaine: {domain}, créé: {created_at[:19]})")

    def delete_selected_email(self):
        selected = self.email_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un email à supprimer.")
            return

        text = selected.text()
        email_id = int(text.split(":")[0])

        reply = QMessageBox.question(
            self, "Confirmer suppression",
            f"Voulez-vous vraiment supprimer l'email {text} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.email_manager.delete_email(email_id)
            self.update_email_list()


def main():
    app = QApplication(sys.argv)
    window = IDSMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
