import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout

DATA_FILE = "barbershop_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"packages": [], "inventory": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

class BarbershopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.setWindowTitle("Barbershop Management System")
        self.setGeometry(100, 100, 800, 600)
        
        # Load data from file
        self.data = load_data()
        
        # Create a central widget and tab layout
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        # Add tabs
        self.initUI()
    
    def initUI(self):
        # Add tabs to the main window, passing loaded data
        self.packages_tab = PackagesTab(self.data)
        self.inventory_tab = InventoryTab(self.data)
        self.earnings_tab = EarningsTab()

        self.central_widget.addTab(self.packages_tab, "Packages")
        self.central_widget.addTab(self.inventory_tab, "Inventory")
        self.central_widget.addTab(self.earnings_tab, "Earnings")
    
    def closeEvent(self, event):
        # Save data when the app is closed
        save_data(self.data)
        event.accept()

class PackagesTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
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
        
        # Save the package data
        self.data["packages"].append({"description": description, "price": price})
        
        # Print receipt logic placeholder
        QMessageBox.information(self, "Receipt", f"Receipt Printed:\nDescription: {description}\nPrice: {price}")
        # Reset fields after checkout
        self.description_input.clear()
        self.price_input.clear()

class InventoryTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        
        # Layout for the tab
        self.layout = QVBoxLayout()

        # Inventory table setup
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setHorizontalHeaderLabels(["Component", "Quantity"])
        self.layout.addWidget(self.inventory_table)
        
        # Populate inventory table from loaded data
        for item in self.data.get("inventory", []):
            self.add_table_row(item["component"], item["quantity"])

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

    def add_table_row(self, component, quantity):
        row_position = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row_position)
        self.inventory_table.setItem(row_position, 0, QTableWidgetItem(component))
        self.inventory_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))

    def add_component(self):
        # Retrieve data from input fields
        component_name = self.component_input.text()
        quantity = self.quantity_input.text()
        
        # Validation
        if not component_name or not quantity.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid component name and quantity.")
            return
        
        # Add to table and save to data
        self.add_table_row(component_name, quantity)
        self.data["inventory"].append({"component": component_name, "quantity": int(quantity)})
        
        # Clear input fields
        self.component_input.clear()
        self.quantity_input.clear()

    def remove_component(self):
        # Get selected row to remove
        current_row = self.inventory_table.currentRow()
        if current_row != -1:
            component_name = self.inventory_table.item(current_row, 0).text()
            # Remove from data
            self.data["inventory"] = [item for item in self.data["inventory"] if item["component"] != component_name]
            self.inventory_table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to remove.")

    def update_quantity(self):
        # Get selected row to update
        current_row = self.inventory_table.currentRow()
        if current_row != -1:
            new_quantity = self.quantity_input.text()
            if new_quantity.isdigit():
                component_name = self.inventory_table.item(current_row, 0).text()
                # Update data
                for item in self.data["inventory"]:
                    if item["component"] == component_name:
                        item["quantity"] = int(new_quantity)
                        break
                self.inventory_table.setItem(current_row, 1, QTableWidgetItem(new_quantity))
                self.quantity_input.clear()
            else:
                QMessageBox.warning(self, "Input Error", "Please enter a valid quantity.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to update.")

class EarningsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout for the earnings tab
        self.layout = QVBoxLayout()

        # Table to display earnings with columns for Date, Service/Description, and Amount
        self.earnings_table = QTableWidget()
        self.earnings_table.setColumnCount(3)
        self.earnings_table.setHorizontalHeaderLabels(["Date", "Service/Description", "Amount"])
        self.layout.addWidget(self.earnings_table)

        # Inputs for adding new earnings entry
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Enter date (e.g., 2024-10-31)")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter service/description")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")

        # Buttons for adding and clearing earnings
        self.add_earning_button = QPushButton("Add Earning")
        self.clear_earnings_button = QPushButton("Clear All Earnings")

        # Display for total earnings
        self.total_earnings_label = QLabel("Total Earnings: $0")

        # Connect buttons to methods
        self.add_earning_button.clicked.connect(self.add_earning)
        self.clear_earnings_button.clicked.connect(self.clear_earnings)

        # Layout for input fields and buttons
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.add_earning_button)
        input_layout.addWidget(self.clear_earnings_button)

        # Add all elements to the main layout
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.total_earnings_label)
        self.setLayout(self.layout)

        # List to store earnings data
        self.earnings_data = []

    def add_earning(self):
        # Retrieve input values
        date = self.date_input.text()
        description = self.description_input.text()
        amount = self.amount_input.text()

        # Validation for non-empty fields and numeric amount
        if not date or not description or not amount.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter valid date, description, and numeric amount.")
            return

        # Add data to table
        row_position = self.earnings_table.rowCount()
        self.earnings_table.insertRow(row_position)
        self.earnings_table.setItem(row_position, 0, QTableWidgetItem(date))
        self.earnings_table.setItem(row_position, 1, QTableWidgetItem(description))
        self.earnings_table.setItem(row_position, 2, QTableWidgetItem(f"${amount}"))

        # Append earnings data to list for total calculation
        self.earnings_data.append(int(amount))

        # Update total earnings
        self.update_total_earnings()

        # Clear input fields after adding
        self.date_input.clear()
        self.description_input.clear()
        self.amount_input.clear()

    def update_total_earnings(self):
        # Calculate total earnings and update label
        total = sum(self.earnings_data)
        self.total_earnings_label.setText(f"Total Earnings: ${total}")

    def clear_earnings(self):
        # Confirm before clearing
        reply = QMessageBox.question(self, "Clear Earnings", "Are you sure you want to clear all earnings?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Clear earnings table and data
            self.earnings_table.setRowCount(0)
            self.earnings_data.clear()
            self.update_total_earnings()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = BarbershopApp()
    mainWin.show()
    sys.exit(app.exec_())
