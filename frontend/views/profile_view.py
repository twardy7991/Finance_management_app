from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QStackedLayout, QMessageBox
from .default_view import DefaultView
from view_models.profile_view_model import ProfileViewModel

class ProfileView(DefaultView):
    
    def __init__(self, parent, viewmodel : ProfileViewModel):
        
        super().__init__(parent)
        main_layout = self.layout()
        widget = UserInfoWidget(self, viewmodel=viewmodel)
        self.viewmodel = viewmodel

        main_layout.addWidget(widget)
    
class UserInfoWidget(QWidget):
    
    def __init__(self, parent, viewmodel : ProfileViewModel):
        super().__init__(parent)
        self.viewmodel = viewmodel
        layout = QVBoxLayout()
        self.labels = {}
        
        self.username_label = UsernameLabel(self, "username", self.viewmodel.username)
        self.name_label = NameLabel(self, "name" , self.viewmodel.name)
        self.surname_label = SurnameLabel(self, "surname" ,self.viewmodel.surname)
        self.phone_label = PhoneLabel(self, "telephone", self.viewmodel.telephone)
        self.email_label = EmailLabel(self, "email", self.viewmodel.email)
        self.address = AddressLabel(self, "address",self.viewmodel.address)
        
        self.save_button = SaveEditedDataButton(self)
        self.profile_updated = ProfileUpdated(self)
        
        layout.addWidget(self.username_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.address)
        layout.addWidget(self.profile_updated)
        self.setLayout(layout)
        
    def save_data(self):
        data = {}
        
        for key in self.labels.keys():
            data_point = self.labels[key]
            if data_point.updated:
                data[key] = data_point.line_edit.text()
        
        if data is {}:
            self.profile_updated.setText("None changes were made")
            self.profile_updated.show()
            return 
        
        self.viewmodel.update_user(data=data)
        
        if self.viewmodel.updated:
            self.profile_updated.setText("Profile Updated")
            self.profile_updated.show()
            self.viewmodel.set_updated()
            for label in self.labels:
                label.updated = False
            
        else:
            self.profile_updated.setText("There was an error while updating the profile")
            self.profile_updated.show()
            
class EditableLabel(QWidget):
    def __init__(self, parent, key, text="Error While Fetching"):
        
        super().__init__(parent)
        self.parent().labels[key] = self
        
        self.label = QLabel(text)
        self.line_edit = QLineEdit(text)
        self.stack = QStackedLayout(self)
        self.stack.addWidget(self.label)
        self.stack.addWidget(self.line_edit)
        self.stack.setCurrentWidget(self.label)
        self.updated = False
        
        self.line_edit.textChanged.connect(self.set_updated_true)
        self.line_edit.editingFinished.connect(self.finish_edit)
    
    def set_updated_true(self):
        self.updated = True
    
    def mouseDoubleClickEvent(self, event):
        self.stack.setCurrentWidget(self.line_edit)
        self.line_edit.setFocus()

    def finish_edit(self):
        self.label.setText(self.line_edit.text())
        self.line_edit.hide()
        self.stack.setCurrentWidget(self.label)
        

class UsernameLabel(EditableLabel):
    def __init__(self, parent, key, text):
        super().__init__(parent, key, text)
        self.hide()

class NameLabel(EditableLabel):
    def __init__(self, parent, key, text):
        super().__init__(parent, key, text)

class SurnameLabel(EditableLabel):
    def __init__(self, parent, key, text):
        super().__init__(parent, key, text)    

class PhoneLabel(EditableLabel):
    def __init__(self, parent, key, text):
        super().__init__(parent, key, text)
    
class EmailLabel(EditableLabel):
    def __init__(self, parent, key, text):
        super().__init__(parent, key, text)
        
class AddressLabel(EditableLabel):
    def __init__(self, parent, key, text):
        super().__init__(parent, key, text)
        
class SaveEditedDataButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.clicked.connect(parent.save_data)
        
class ProfileUpdated(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.hide()
        