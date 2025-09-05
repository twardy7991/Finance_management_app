import sys

from PyQt6.QtWidgets import QApplication

from views.login_view import LoginView
from main_window import MainWindow
from app_state import AppState

def create_app():
    
    app = QApplication(sys.argv)
    window = MainWindow(AppState())
    window.show()
    app.exec()
    
if __name__ == "__main__":
    app = create_app()