from PyQt6.QtCore import QAbstractTableModel, QModelIndex, pyqtSlot

from dataclasses import dataclass
from datetime import datetime
from models.operation_model import OperationModel

class OperationViewModel(QAbstractTableModel):
    fields = ["description", "category", "date", "value", "currency", "month"]
    
    def __init__(self, parent = None, model : OperationModel = None):
        self.model = model
        
        super().__init__(parent)
        
        self.operations_list = []
        operations = self.model.get_operations()
        
        for operation in operations:
            self.add(self.Operation(description=operation["description"],
                                    category=operation["category"],
                                    date=operation["operation_date"],
                                    value=operation["value"],
                                    currency=operation["currency"]))
        
    # class OperationRole(IntEnum):
    #     ItemDescriptionRole = Qt.ItemDataRole.DisplayRole
    #     ItemCategoryRole = Qt.ItemDataRole.UserRole
    #     ItemDateRole = Qt.ItemDataRole.UserRole + 1
    #     ItemValueRole = Qt.ItemDataRole.UserRole + 2
    #     ItemCurrencyRole = Qt.ItemDataRole.UserRole + 3
    #     ItemMonthRole = Qt.ItemDataRole.UserRole + 4
    
    @dataclass
    class Operation:
        description : str
        category : str
        date : str
        value : int
        currency : str
        
        @property
        def month(self):
            return datetime.strptime(self.date, "%Y-%m-%d").strftime("%B %Y")
        
    def rowCount(self, parent = QModelIndex()):
        return len(self.operations_list)
    
    def columnCount(self, parent = None):
        return len(self.fields)
    
    def data(self, index, role) -> None:
        row = index.row()
        if row < self.rowCount():
            operation = self.operations_list[row]
            match index.column():
                case 0:
                    return operation.description
                case 1:
                    return operation.category
                case 2:
                    return operation.date
                case 3:
                    return operation.value
                case 4:
                    return operation.currency
                case 5:
                    return operation.month
                case _:
                    return None
    
    # def data(self, index, role) -> None:
    #     row = index.row()
    #     if row < self.rowCount():
    #         operation = self.operations_list[row]
    #         match role:
    #             case OperationsModel.OperationRole.ItemDescriptionRole: 
    #                 return operation.description
    #             case OperationsModel.OperationRole.ItemCategoryRole:
    #                 return operation.category
    #             case OperationsModel.OperationRole.ItemDateRole:
    #                 return operation.date
    #             case OperationsModel.OperationRole.ItemValueRole:
    #                 return operation.value
    #             case OperationsModel.OperationRole.ItemCurrencyRole:
    #                 return operation.currency
    #             case OperationsModel.OperationRole.ItemMonthRole:
    #                 return operation.month
    #             case _:
    #                 return None
    
    @pyqtSlot()
    def add(self, operation):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.operations_list.insert(0, operation)
        self.endInsertRows()