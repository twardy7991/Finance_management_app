from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMainWindow, QApplication, QVBoxLayout
from view_models.profile_view_model import ProfileViewModel
from models.user_model import UserModel
from models.operation_model import OperationModel
from view_models.operation_view_model import OperationViewModel

class DefaultView(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        layout.addLayout(NavigationBar(parent))
        self.setLayout(layout)
    
class NavigationBar(QHBoxLayout):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.window = self.parent()
        self.addWidget(HomeButton(parent))
        self.addWidget(OperationsButton(parent))
        self.addWidget(DashboardButton(parent))
        self.addWidget(ProfileButton(parent))    
        self.addWidget(LogoutButton(parent))
    
class HomeButton(QPushButton):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setText("Home")
        self.parent_window = parent 
        self.clicked.connect(self.go_home)

    def go_home(self):
        from .home_view import HomeView
        self.parent_window.setWidget(HomeView(self.parent_window))
        
class OperationsButton(QPushButton):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setText("Operations")
        self.parent_window = parent 
        self.clicked.connect(self.go_operations)

    def go_operations(self):
        from .operations_view import OperationsView
        self.parent_window.setWidget(OperationsView(self.parent_window, view_model=OperationViewModel(model=OperationModel())))
    
class ProfileButton(QPushButton):

    def __init__(self, parent):
        super().__init__(parent)
        self.setText("Profile")
        self.parent_window = parent 
        self.clicked.connect(self.go_profile)

    def go_profile(self):
        from .profile_view import ProfileView

        self.parent_window.setWidget(ProfileView(self.parent_window, viewmodel=ProfileViewModel(model=UserModel())))

class DashboardButton(QPushButton):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.setText("Dashboard")
        self.parent_window = parent 
        self.clicked.connect(self.go_dashboard)

    def go_dashboard(self):
        from .dashboard_view import DashboardView
        self.parent_window.setWidget(DashboardView(self.parent_window))
        
class LogoutButton(QPushButton):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Logout")
        
        self.clicked.connect(self.logout)
        
    def logout(self):
        from .login_view import LoginViewModel
        from models.login_model import LoginModel
        self.login_view_model = LoginViewModel(LoginModel(), self.parent().app_state)
        self.login_view_model.logout()
    
if __name__ == "__main__":
    from PyQt6.QtWidgets import QMainWindow, QApplication
    import sys
    
    sys.path.append("/home/twardy/projects/Finance_calc")
    class MainWindow(QMainWindow):

        def __init__(self):
            super().__init__()

            self.setWindowTitle("My App")

            self.setWidget(DefaultView(self))
        
        def setWidget(self, widget):
            self.setCentralWidget(widget) 
            self.show()   
        
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()