import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from views.login_view import LoginView
from view_models.login_view_model import LoginViewModel
from models.login_model import LoginModel

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self, app_state):
        super().__init__()
        
        self.setWindowTitle("My App")
        self.app_state = app_state
        self.setWidget(LoginView(self, LoginViewModel(LoginModel(), self.app_state)))
        
        self.setMinimumSize(800, 600)
          
    def setWidget(self, widget):
        self.setCentralWidget(widget)
        self.show()