from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from .default_view import DefaultView

class HomeView(DefaultView):
    
    def __init__(self, parent):
        super().__init__(parent)
        main_layout = self.layout()
        sub_layout = QHBoxLayout()
        sub_layout.addWidget(QPushButton("Button h  1"))
        sub_layout.addWidget(QPushButton("Buttonh  2"))

        main_layout.addLayout(sub_layout)