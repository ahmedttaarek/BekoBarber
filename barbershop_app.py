import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout

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
        
        # Layout for the tab
        self.layout = QVBoxLayout()

        # Inventory table setup
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setHorizontalHeaderLabels(["Component", "Quantity"])
        self.layout.addWidget(self.inventory_table)

        # Input fields for adding and updating items
        self.component_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.component_input.setPlaceholderText("Enter component name")
        self.quantity_input.setPlaceholderText("Enter quantity")

        # Buttons
        self.add_button = QPushButton("Add Component")
        self.remove_button = QPushButton("Remove Component")
        self.update_button = QPushButton("Update Quantity")

        # Connect buttons to their functions
        self.add_button.clicked.connect(self.add_component)
        self.remove_button.clicked.connect(self.remove_component)
        self.update_button.clicked.connect(self.update_quantity)

        # Arrange input fields and buttons in a horizontal layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.component_input)
        input_layout.addWidget(self.quantity_input)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.remove_button)
        input_layout.addWidget(self.update_button)

        # Add widgets and layouts to the main layout
        self.layout.addLayout(input_layout)
        self.setLayout(self.layout)

    def add_component(self):
        # Retrieve data from input fields
        component_name = self.component_input.text()
        quantity = self.quantity_input.text()
        
        # Validation
        if not component_name or not quantity.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid component name and quantity.")
            return
        
        # Add to table
        row_position = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row_position)
        self.inventory_table.setItem(row_position, 0, QTableWidgetItem(component_name))
        self.inventory_table.setItem(row_position, 1, QTableWidgetItem(quantity))
        
        # Clear input fields
        self.component_input.clear()
        self.quantity_input.clear()

    def remove_component(self):
        # Get selected row to remove
        current_row = self.inventory_table.currentRow()
        if current_row != -1:
            self.inventory_table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to remove.")

    def update_quantity(self):
        # Get selected row to update
        current_row = self.inventory_table.currentRow()
        if current_row != -1:
            new_quantity = self.quantity_input.text()
            if new_quantity.isdigit():
                self.inventory_table.setItem(current_row, 1, QTableWidgetItem(new_quantity))
                self.quantity_input.clear()
            else:
                QMessageBox.warning(self, "Input Error", "Please enter a valid quantity.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to update.")

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
