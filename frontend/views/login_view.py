from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QHBoxLayout, QLayout, QMessageBox
from view_models.login_view_model import LoginViewModel
from views import HomeView

class LoginView(QWidget):
    def __init__(self, parent, viewmodel: LoginViewModel):
        super().__init__(parent)
        self.viewmodel = viewmodel
        self.username = ""
        self.password = ""
        self.parent_window = parent
        self.setWindowTitle("Login Page")
        self.login_message = LoginMessage(self)
        
        layout = QVBoxLayout()
        layout.addLayout(UsernameLayout(self))
        layout.addLayout(PasswordLayout(self))
        layout.addWidget(self.login_message)
        
        layout.addWidget(LoginButton(self.send_login_request))
        self.setLayout(layout)

    def update_username(self):
        # Called when username text changes
        self.username = self.username_textbox.toPlainText()

    def update_password(self):
        # Called when password text changes
        self.password = self.password_textbox.toPlainText()

    def send_login_request(self):
        self.viewmodel.login(self.username, self.password)
        if self.viewmodel.logged:
            self.parent_window.setWidget(HomeView(parent=self.parent_window))
            msg = QMessageBox()
            msg.setText(self.viewmodel.login_message)    
            msg.exec()
        else:
            self.login_message.show()

class UsernameLayout(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.addWidget(UsernameLabel())
        parent.username_textbox = UsernameTextBox(parent)
        self.addWidget(parent.username_textbox)

class PasswordLayout(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.addWidget(PasswordLabel())
        parent.password_textbox = PasswordTextBox(parent)
        self.addWidget(parent.password_textbox)

class UsernameTextBox(QTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.textChanged.connect(parent.update_username)

class PasswordTextBox(QTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.textChanged.connect(parent.update_password)

class UsernameLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Username")

class PasswordLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Password")

class LoginButton(QPushButton):
    def __init__(self, callback):
        super().__init__()
        self.setText("Login")
        self.clicked.connect(callback)
        
class LoginMessage(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setText("Login Unsuccessful")
        self.hide()
        