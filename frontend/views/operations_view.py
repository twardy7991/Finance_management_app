from PyQt6.QtWidgets import QWidget 
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidgetItem, QListWidget, QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSlot
from .default_view import DefaultView

from dataclasses import dataclass
from datetime import datetime
from view_models.operation_view_model import OperationViewModel

class OperationsView(DefaultView):
    
    def __init__(self, parent, view_model):
        super().__init__(parent)
        
        main_layout = self.layout()
        
        sub_layout = QHBoxLayout()
        table_view = QTableView()
        self.model = view_model
        
        
        table_view.setModel(self.model)
        sub_layout.addWidget(table_view)
        
        main_layout.addLayout(sub_layout)
        
