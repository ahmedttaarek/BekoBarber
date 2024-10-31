import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox

class BarbershopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.setWindowTitle("Barbershop Management System")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a central widget and tab layout
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        # Add tabs
        self.initUI()
    
    def initUI(self):
        # Add tabs to the main window
        self.packages_tab = PackagesTab()
        self.inventory_tab = InventoryTab()
        self.earnings_tab = EarningsTab()

        self.central_widget.addTab(self.packages_tab, "Packages")
        self.central_widget.addTab(self.inventory_tab, "Inventory")
        self.central_widget.addTab(self.earnings_tab, "Earnings")

class PackagesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        # Add form for entering package details
        form_layout = QFormLayout()
        
        # Input fields for Description and Price
        self.description_input = QLineEdit()
        self.price_input = QLineEdit()
        
        # Add input fields to the form
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Price:", self.price_input)
        
        # Add a Checkout button
        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        
        # Add form and button to the layout
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.checkout_button)
        
        # Set the layout for the tab
        self.setLayout(self.layout)

    def checkout(self):
        # Get input values
        description = self.description_input.text()
        price = self.price_input.text()
        
        # Simple validation
        if not description or not price:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields.")
            return
        
        # Print receipt logic placeholder
        QMessageBox.information(self, "Receipt", f"Receipt Printed:\nDescription: {description}\nPrice: {price}")
        # Reset fields after checkout
        self.description_input.clear()
        self.price_input.clear()

class InventoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Inventory tab coming soon"))
        self.setLayout(layout)

class EarningsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Earnings tab coming soon"))
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = BarbershopApp()
    mainWin.show()
    sys.exit(app.exec_())
