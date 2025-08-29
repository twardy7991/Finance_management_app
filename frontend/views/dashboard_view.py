from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget
from .default_view import DefaultView

class DashboardView(DefaultView):
    
    def __init__(self, parent):
        super().__init__(parent)
        main_layout = self.layout()
        sub_layout = QHBoxLayout()
        
        main_layout.addLayout(sub_layout)

class OperationsList(QListWidget):
    
    def __init__(self):
        super().__init__()
        