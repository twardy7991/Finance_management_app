from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QStackedLayout
from .default_view import DefaultView

class ProfileView(DefaultView):
    
    def __init__(self, parent, viewmodel):
        
        super().__init__(parent)
        main_layout = self.layout()
        sub_layout = UserInfoLayout(viewmodel=viewmodel)
        self.viewmodel = viewmodel

        main_layout.addLayout(sub_layout)
    
class UserInfoLayout(QVBoxLayout):
    
    def __init__(self, viewmodel, parent=None):
        super().__init__()
        self.viewmmodel = viewmodel
        
        self.addWidget(UsernameLabel(viewmodel.username))
        self.addWidget(NameLabel(viewmodel.name))
        self.addWidget(SurnameLabel(viewmodel.surname))
        self.addWidget(PhoneLabel(viewmodel.telephone))
        self.addWidget(EmailLabel(viewmodel.email))
        self.addWidget(AddressLabel(viewmodel.address))
        
class EditableLabel(QWidget):
    def __init__(self, text="Error While Fetching", parent=None):
        
        super().__init__(parent)

        self.label = QLabel(text)
        self.line_edit = QLineEdit(text)
        self.stack = QStackedLayout(self)
        self.stack.addWidget(self.label)
        self.stack.addWidget(self.line_edit)
        self.stack.setCurrentWidget(self.label)
        
        self.line_edit.editingFinished.connect(self.finish_edit)
    
    def mouseDoubleClickEvent(self, event):
        self.stack.setCurrentWidget(self.line_edit)
        self.line_edit.setFocus()

    def finish_edit(self):
        self.label.setText(self.line_edit.text())
        self.line_edit.hide()
        self.stack.setCurrentWidget(self.label)

class UsernameLabel(EditableLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

class NameLabel(EditableLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

class SurnameLabel(EditableLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)    

class PhoneLabel(EditableLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
    
class EmailLabel(EditableLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
class AddressLabel(EditableLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)    