import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from datetime import datetime

DATA_FILE = "barbershop_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            # Ensure all necessary keys exist
            if "packages" not in data:
                data["packages"] = []
            if "inventory" not in data:
                data["inventory"] = []
            if "earnings" not in data:
                data["earnings"] = []  # Ensure earnings key exists
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Ensure the default structure contains all necessary keys
        return {"packages": [], "inventory": [], "earnings": []}

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
        self.data = load_data()  # This will ensure "earnings" exists
        
        # Create a central widget and tab layout
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        # Initialize tabs
        self.earnings_tab = EarningsTab(self.data)
        self.packages_tab = PackagesTab(self.data, self.earnings_tab)
        self.inventory_tab = InventoryTab(self.data)

        # Add tabs
        self.central_widget.addTab(self.packages_tab, "Packages")
        self.central_widget.addTab(self.inventory_tab, "Inventory")
        self.central_widget.addTab(self.earnings_tab, "Earnings")

    def closeEvent(self, event):
        # Save data when the app is closed
        save_data(self.data)
        event.accept()

class PackagesTab(QWidget):
    def __init__(self, data, earnings_tab):
        super().__init__()
        self.data = data
        self.earnings_tab = earnings_tab  # Store the reference to EarningsTab
        self.layout = QVBoxLayout()
        
        # Add form for entering package details
        form_layout = QFormLayout()
        
        # Input fields for Description and Price
        self.description_input = QLineEdit()
        self.price_input = QLineEdit()
        
        # Add input fields to the form
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Price:", self.price_input)
        
        # Add buttons for adding package, checking out, and deleting package
        self.add_package_button = QPushButton("Add Package")
        self.add_package_button.clicked.connect(self.add_package)
        
        self.checkout_button = QPushButton("Checkout Selected Package")
        self.checkout_button.clicked.connect(self.checkout)

        self.delete_package_button = QPushButton("Delete Selected Package")
        self.delete_package_button.clicked.connect(self.delete_package)

        # Packages table setup
        self.packages_table = QTableWidget()
        self.packages_table.setColumnCount(2)
        self.packages_table.setHorizontalHeaderLabels(["Description", "Price"])
        self.layout.addWidget(self.packages_table)

        # Add form and buttons to the layout
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.add_package_button)
        self.layout.addWidget(self.checkout_button)
        self.layout.addWidget(self.delete_package_button)
        
        # Set the layout for the tab
        self.setLayout(self.layout)

        # Populate table with existing packages
        self.load_packages_to_table()

    def load_packages_to_table(self):
        # Populate the table with packages stored in the data
        for package in self.data.get("packages", []):
            row_position = self.packages_table.rowCount()
            self.packages_table.insertRow(row_position)
            self.packages_table.setItem(row_position, 0, QTableWidgetItem(package["description"]))
            self.packages_table.setItem(row_position, 1, QTableWidgetItem(str(package["price"])))

    def add_package(self):
        # Get input values
        description = self.description_input.text()
        price = self.price_input.text()
        
        # Simple validation
        if not description or not price:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields.")
            return
        
        # Save the package data
        package_data = {"description": description, "price": float(price)}
        self.data["packages"].append(package_data)
        
        # Add package to the table for display
        row_position = self.packages_table.rowCount()
        self.packages_table.insertRow(row_position)
        self.packages_table.setItem(row_position, 0, QTableWidgetItem(description))
        self.packages_table.setItem(row_position, 1, QTableWidgetItem(price))
        
        # Confirm package addition
        QMessageBox.information(self, "Package Added", f"Package Added:\nDescription: {description}\nPrice: {price}")
        
        # Reset fields after adding
        self.description_input.clear()
        self.price_input.clear()

    def checkout(self):
        # Get selected row to checkout
        current_row = self.packages_table.currentRow()
        if current_row != -1:
            description = self.packages_table.item(current_row, 0).text()
            price = self.packages_table.item(current_row, 1).text()
            # Print receipt logic placeholder
            QMessageBox.information(self, "Receipt", f"Receipt Printed:\nDescription: {description}\nPrice: {price}")
            
            # Log earning to the EarningsTab
            self.earnings_tab.add_earning(price)  # Access earnings_tab directly

        else:
            QMessageBox.warning(self, "Selection Error", "Please select a package to checkout.")

    def delete_package(self):
        # Get selected row to delete
        current_row = self.packages_table.currentRow()
        if current_row != -1:
            # Remove from data
            package_description = self.packages_table.item(current_row, 0).text()
            self.data["packages"] = [pkg for pkg in self.data["packages"] if pkg["description"] != package_description]
            self.packages_table.removeRow(current_row)
            QMessageBox.information(self, "Package Deleted", f"Package Deleted: {package_description}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a package to delete.")

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
            self.data["inventory"] = [item for item in self.data["inventory"] if item["component"] != component_name]
            self.inventory_table.removeRow(current_row)
            QMessageBox.information(self, "Component Removed", f"Component Removed: {component_name}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to remove.")

    def update_quantity(self):
        # Get selected row to update
        current_row = self.inventory_table.currentRow()
        if current_row != -1:
            component_name = self.inventory_table.item(current_row, 0).text()
            new_quantity = self.quantity_input.text()
            
            # Validation
            if not new_quantity.isdigit():
                QMessageBox.warning(self, "Input Error", "Please enter a valid quantity.")
                return
            
            # Update the quantity in the table and data
            self.inventory_table.item(current_row, 1).setText(new_quantity)
            for item in self.data["inventory"]:
                if item["component"] == component_name:
                    item["quantity"] = int(new_quantity)
                    break
            
            QMessageBox.information(self, "Quantity Updated", f"Quantity updated for: {component_name}")
            self.quantity_input.clear()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to update.")

class EarningsTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        
        # Layout for the tab
        self.layout = QVBoxLayout()

        # Earnings table setup
        self.earnings_table = QTableWidget()
        self.earnings_table.setColumnCount(2)
        self.earnings_table.setHorizontalHeaderLabels(["Date", "Earnings"])
        self.layout.addWidget(self.earnings_table)
        
        # Populate earnings table from loaded data
        for earning in self.data.get("earnings", []):
            self.add_table_row(earning["date"], earning["amount"])

        # Total earnings label
        self.total_earnings_label = QLabel("Total Earnings: $0")
        self.layout.addWidget(self.total_earnings_label)

        # Set the layout for the tab
        self.setLayout(self.layout)

    def add_table_row(self, date, amount):
        row_position = self.earnings_table.rowCount()
        self.earnings_table.insertRow(row_position)
        self.earnings_table.setItem(row_position, 0, QTableWidgetItem(date))
        self.earnings_table.setItem(row_position, 1, QTableWidgetItem(str(amount)))

    def add_earning(self, amount):
        # Get the current date for the earning entry
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_table_row(date, amount)

        # Update the total earnings
        total = sum(float(self.earnings_table.item(row, 1).text()) for row in range(self.earnings_table.rowCount()))
        self.total_earnings_label.setText(f"Total Earnings: ${total:.2f}")

        # Store the earning data in the earnings list
        self.data["earnings"].append({"date": date, "amount": float(amount)})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarbershopApp()
    window.show()
    sys.exit(app.exec_())
