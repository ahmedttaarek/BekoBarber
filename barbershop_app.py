import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from datetime import datetime

DATA_FILE = "barbershop_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            if "packages" not in data:
                data["packages"] = []
            if "inventory" not in data:
                data["inventory"] = []
            if "earnings" not in data:
                data["earnings"] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"packages": [], "inventory": [], "earnings": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

class BarbershopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Barbershop Management System")
        self.setGeometry(100, 100, 800, 600)
        
        self.data = load_data()
        
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        self.earnings_tab = EarningsTab(self.data)
        self.packages_tab = PackagesTab(self.data, self.earnings_tab)
        self.inventory_tab = InventoryTab(self.data)

        self.central_widget.addTab(self.packages_tab, "Packages")
        self.central_widget.addTab(self.inventory_tab, "Inventory")
        self.central_widget.addTab(self.earnings_tab, "Earnings")

    def closeEvent(self, event):
        save_data(self.data)
        event.accept()

class PackagesTab(QWidget):
    def __init__(self, data, earnings_tab):
        super().__init__()
        self.data = data
        self.earnings_tab = earnings_tab
        self.layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.description_input = QLineEdit()
        self.price_input = QLineEdit()
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Price:", self.price_input)
        
        self.add_package_button = QPushButton("Add Package")
        self.add_package_button.clicked.connect(self.add_package)
        
        self.checkout_button = QPushButton("Checkout Selected Package")
        self.checkout_button.clicked.connect(self.checkout)

        self.delete_package_button = QPushButton("Delete Selected Package")
        self.delete_package_button.clicked.connect(self.delete_package)

        self.packages_table = QTableWidget()
        self.packages_table.setColumnCount(2)
        self.packages_table.setHorizontalHeaderLabels(["Description", "Price"])
        self.layout.addWidget(self.packages_table)

        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.add_package_button)
        self.layout.addWidget(self.checkout_button)
        self.layout.addWidget(self.delete_package_button)
        
        self.setLayout(self.layout)

        self.load_packages_to_table()

    def load_packages_to_table(self):
        for package in self.data.get("packages", []):
            row_position = self.packages_table.rowCount()
            self.packages_table.insertRow(row_position)
            self.packages_table.setItem(row_position, 0, QTableWidgetItem(package["description"]))
            self.packages_table.setItem(row_position, 1, QTableWidgetItem(str(package["price"])))

    def add_package(self):
        description = self.description_input.text()
        price = self.price_input.text()
        
        if not description or not price:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields.")
            return
        
        package_data = {"description": description, "price": float(price)}
        self.data["packages"].append(package_data)
        
        row_position = self.packages_table.rowCount()
        self.packages_table.insertRow(row_position)
        self.packages_table.setItem(row_position, 0, QTableWidgetItem(description))
        self.packages_table.setItem(row_position, 1, QTableWidgetItem(price))
        
        QMessageBox.information(self, "Package Added", f"Package Added:\nDescription: {description}\nPrice: {price}")
        
        self.description_input.clear()
        self.price_input.clear()

    def checkout(self):
        current_row = self.packages_table.currentRow()
        if current_row != -1:
            description = self.packages_table.item(current_row, 0).text()
            price = self.packages_table.item(current_row, 1).text()
            QMessageBox.information(self, "Receipt", f"Receipt Printed:\nDescription: {description}\nPrice: {price}")
            self.earnings_tab.add_earning(price)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a package to checkout.")

    def delete_package(self):
        current_row = self.packages_table.currentRow()
        if current_row != -1:
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
        
        self.layout = QVBoxLayout()

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(3)
        self.inventory_table.setHorizontalHeaderLabels(["Component", "Quantity", "Actions"])
        self.layout.addWidget(self.inventory_table)
        
        self.load_inventory_to_table()

        self.component_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.add_component_button = QPushButton("Add Component")
        self.add_component_button.clicked.connect(self.add_component)
        self.remove_component_button = QPushButton("Remove Component")
        self.remove_component_button.clicked.connect(self.remove_component)
        
        self.layout.addWidget(QLabel("Component Name:"))
        self.layout.addWidget(self.component_input)
        self.layout.addWidget(QLabel("Quantity:"))
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(self.add_component_button)
        self.layout.addWidget(self.remove_component_button)

        self.setLayout(self.layout)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

    def load_inventory_to_table(self):
        for item in self.data.get("inventory", []):
            self.add_table_row(item["component"], item["quantity"])

    def add_table_row(self, component, quantity):
        row_position = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row_position)
        self.inventory_table.setItem(row_position, 0, QTableWidgetItem(component))
        self.inventory_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))

        # Create a widget to hold the buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        # Create the plus button
        plus_button = QPushButton("+")
        plus_button.clicked.connect(lambda: self.change_quantity(row_position, 1))
        button_layout.addWidget(plus_button)

        # Create the minus button
        minus_button = QPushButton("-")
        minus_button.clicked.connect(lambda: self.change_quantity(row_position, -1))
        button_layout.addWidget(minus_button)

        # Set the button widget in the third column
        self.inventory_table.setCellWidget(row_position, 2, button_widget)

    def add_component(self):
        component_name = self.component_input.text()
        quantity = self.quantity_input.text()
        
        if not component_name or not quantity.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid component name and quantity.")
            return
        
        self.add_table_row(component_name, quantity)
        self.data["inventory"].append({"component": component_name, "quantity": int(quantity)})
        
        self.component_input.clear()
        self.quantity_input.clear()

    def remove_component(self):
        current_row = self.inventory_table.currentRow()
        if current_row != -1:
            component_name = self.inventory_table.item(current_row, 0).text()
            self.data["inventory"] = [item for item in self.data["inventory"] if item["component"] != component_name]
            self.inventory_table.removeRow(current_row)
            QMessageBox.information(self, "Component Removed", f"Component Removed: {component_name}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to remove.")

    def change_quantity(self, row, change):
        current_item = self.inventory_table.item(row, 1)
        if current_item:
            current_quantity = int(current_item.text())
            new_quantity = current_quantity + change
            
            if new_quantity < 0:
                return
            
            self.inventory_table.item(row, 1).setText(str(new_quantity))
            component_name = self.inventory_table.item(row, 0).text()
            for item in self.data["inventory"]:
                if item["component"] == component_name:
                    item["quantity"] = new_quantity
                    break
    
    def save_data(self):
        with open('data.json', 'w') as json_file:
            json.dump(self.data, json_file, indent=4)
        QMessageBox.information(self, "Data Saved", "Inventory changes have been saved successfully.")



class EarningsTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        
        self.layout = QVBoxLayout()
        self.earnings_table = QTableWidget()
        self.earnings_table.setColumnCount(2)
        self.earnings_table.setHorizontalHeaderLabels(["Date", "Amount"])
        
        self.layout.addWidget(self.earnings_table)

        self.total_earnings_label = QLabel("Total Earnings: $0")
        self.layout.addWidget(self.total_earnings_label)

        self.setLayout(self.layout)

        self.load_earnings_to_table()
        self.update_total_earnings()

    def load_earnings_to_table(self):
        for earning in self.data.get("earnings", []):
            row_position = self.earnings_table.rowCount()
            self.earnings_table.insertRow(row_position)
            self.earnings_table.setItem(row_position, 0, QTableWidgetItem(earning["date"]))
            self.earnings_table.setItem(row_position, 1, QTableWidgetItem(str(earning["amount"])))

    def add_earning(self, amount):
        earning_data = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "amount": float(amount)}
        self.data["earnings"].append(earning_data)

        row_position = self.earnings_table.rowCount()
        self.earnings_table.insertRow(row_position)
        self.earnings_table.setItem(row_position, 0, QTableWidgetItem(earning_data["date"]))
        self.earnings_table.setItem(row_position, 1, QTableWidgetItem(str(earning_data["amount"])))

        self.update_total_earnings()

    def update_total_earnings(self):
        total = sum(earning["amount"] for earning in self.data["earnings"])
        self.total_earnings_label.setText(f"Total Earnings: ${total:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarbershopApp()
    window.show()
    sys.exit(app.exec_())
