import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QMainWindow,
    QTabWidget,
    QFormLayout,
    QLineEdit,
    QHeaderView,
    QSizePolicy
)
from PyQt5.QtGui import QFont, QPainter, QPixmap, QIcon  
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog  
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

        self.setWindowTitle("Beko Barber")
        self.setGeometry(100, 100, 1000, 800)  # Increased window size

        # Set default font
        font = QFont("Arial", 12)
        self.setFont(font)

        self.data = load_data()

        # Set layout direction to right-to-left
        self.setLayoutDirection(Qt.RightToLeft)

        # Create a central widget to hold the logo and tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout(self.central_widget)

        # Add logo
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("beko.jpg").scaled(300, 100, Qt.KeepAspectRatio)  
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)  

        # Set application icon
        self.setWindowIcon(QIcon("beko.jpg"))  

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget) 

        self.earnings_tab = EarningsTab(self.data)
        self.packages_tab = PackagesTab(self.data, self.earnings_tab)
        self.inventory_tab = InventoryTab(self.data)

        self.tab_widget.addTab(self.packages_tab, "الباقات")
        self.tab_widget.addTab(self.inventory_tab, "المخزون")
        self.tab_widget.addTab(self.earnings_tab, "الأرباح")

    def closeEvent(self, event):
        save_data(self.data)
        event.accept()


class PackagesTab(QWidget):
    def __init__(self, data, earnings_tab):
        super().__init__()
        self.data = data
        self.earnings_tab = earnings_tab
        self.layout = QVBoxLayout()

        # Set layout direction to right-to-left
        self.setLayoutDirection(Qt.RightToLeft)

        # Adjusted font for larger screens
        large_font = QFont("Arial", 16)

        form_layout = QFormLayout()
        self.description_input = QLineEdit()
        self.description_input.setFont(large_font)
        self.price_input = QLineEdit()
        self.price_input.setFont(large_font)
        
        form_layout.addRow("الوصف:", self.description_input)
        form_layout.addRow("السعر:", self.price_input)
        form_layout.setAlignment(Qt.AlignRight)

        # Customize button styles, sizes, and font
        button_font = QFont("Arial", 14)
        
        # Add Package Button
        self.add_package_button = QPushButton("أضف باقة")
        self.add_package_button.setFont(button_font)
        self.add_package_button.setFixedSize(QSize(200, 50))
        self.add_package_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;  /* Darker green on hover */
            }
        """)
        self.add_package_button.clicked.connect(self.add_package)

        # Checkout Button
        self.checkout_button = QPushButton("الدفع للباقة المختارة")
        self.checkout_button.setFont(button_font)
        self.checkout_button.setFixedSize(QSize(250, 50))
        self.checkout_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1E88E5;  /* Darker blue on hover */
            }
        """)
        self.checkout_button.clicked.connect(self.checkout)

        # Delete Package Button
        self.delete_package_button = QPushButton("احذف الباقة المختارة")
        self.delete_package_button.setFont(button_font)
        self.delete_package_button.setFixedSize(QSize(240, 50))
        self.delete_package_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e53935;  /* Darker red on hover */
            }
        """)
        self.delete_package_button.clicked.connect(self.delete_package)

        # Enhanced table style
        self.packages_table = QTableWidget()
        self.packages_table.setColumnCount(2)
        self.packages_table.setHorizontalHeaderLabels(["الوصف", "السعر"])

        # Set layout direction for the table
        self.packages_table.setLayoutDirection(Qt.RightToLeft)

        # Adjust table size, font, and readability for large screens
        self.packages_table.setFont(QFont("Arial", 18, QFont.Bold))  # Set larger and bold font
        self.packages_table.setMinimumSize(900, 500)
        self.packages_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set equal column widths
        column_width = 400  # Adjust this value as needed
        self.packages_table.setColumnWidth(0, column_width)
        self.packages_table.setColumnWidth(1, column_width)

        # Style the header
        header = self.packages_table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #333; color: white; font-weight: bold; padding: 16px; }")
        header.setFont(QFont("Arial", 18, QFont.Bold))  # Header font size and style
        header.setStretchLastSection(True)

        # Row height and alternating colors with hover effect
        self.packages_table.verticalHeader().setDefaultSectionSize(50)
        self.packages_table.setAlternatingRowColors(True)
        self.packages_table.setStyleSheet(""" 
                QTableWidget {
                    font-size: 18px;  /* Increased font size for table cells */
                    border: 1px solid #ddd;
                    gridline-color: #ddd;
                }
                QHeaderView::section {
                    font-size: 18px;  /* Header font size */
                    background-color: #333;
                    color: white;
                    font-weight: bold;
                    padding: 15px;
                }
                QTableWidget::item {
                    padding: 10px;
                    text-align: center;  /* Center text in all table cells */
                }
            """)
        self.packages_table.verticalHeader().setDefaultSectionSize(50)  # Adjust row height
        self.layout.addWidget(self.packages_table)
        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_package_button)
        button_layout.addWidget(self.checkout_button)
        button_layout.addWidget(self.delete_package_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

        self.load_packages_to_table()

    def load_packages_to_table(self):
        for package in self.data.get("packages", []):
            row_position = self.packages_table.rowCount()
            self.packages_table.insertRow(row_position)
            
            # Center-aligned items
            description_item = QTableWidgetItem(package["description"])
            description_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.packages_table.setItem(row_position, 0, description_item)
            
            price_item = QTableWidgetItem(str(package["price"]))
            price_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.packages_table.setItem(row_position, 1, price_item)

    def add_package(self):
        description = self.description_input.text()
        price = self.price_input.text()
        
        if not description or not price:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى ملء جميع الحقول.")
            return
        
        package_data = {"description": description, "price": float(price)}
        self.data["packages"].append(package_data)
        
        row_position = self.packages_table.rowCount()
        self.packages_table.insertRow(row_position)
        
        description_item = QTableWidgetItem(description)
        description_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.packages_table.setItem(row_position, 0, description_item)
        
        price_item = QTableWidgetItem(price)
        price_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.packages_table.setItem(row_position, 1, price_item)
        
        QMessageBox.information(self, "تم إضافة الباقة", f"تمت إضافة الباقة:\nالوصف: {description}\nالسعر: {price}")
        
        self.description_input.clear()
        self.price_input.clear()

    def checkout(self):
        current_row = self.packages_table.currentRow()
        if current_row != -1:
            description = self.packages_table.item(current_row, 0).text()
            price = self.packages_table.item(current_row, 1).text()

            # Create the receipt message
            receipt_message = (
                "عنوان: بيكو حلاق\n"
                f"السعر: {price}\n"
                f"الباقة: {description}\n"
                "رسالة: صالون بيكو تشرف بوجود حضراتكم"
            )

            # Ask the user to connect to the printer and print the receipt
            self.print_receipt(receipt_message)
            self.earnings_tab.add_earning(price)
        else:
            QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار باقة للدفع.")

    def print_receipt(self, message):
        # Create a printer object
        printer = QPrinter(QPrinter.HighResolution)

        # Show the print dialog
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)

            # Set the font for the printed text
            font = QFont("Arial", 16)
            painter.setFont(font)

            # Draw the message on the printer
            # You may want to adjust these coordinates to fit your layout
            painter.drawText(100, 100, message)  # Adjust x, y coordinates as needed

            # End the painting
            painter.end()

    def delete_package(self):
        current_row = self.packages_table.currentRow()
        if current_row != -1:
            package_description = self.packages_table.item(current_row, 0).text()
            self.data["packages"] = [pkg for pkg in self.data["packages"] if pkg["description"] != package_description]
            self.packages_table.removeRow(current_row)
            QMessageBox.information(self, "تم حذف الباقة", f"تم حذف الباقة: {package_description}")
        else:
            QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار باقة للحذف.")



class InventoryTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data

        # Set layout direction to right-to-left
        self.setLayoutDirection(Qt.RightToLeft)

        self.layout = QVBoxLayout()

        # Inventory table with enhanced style and layout
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(3)
        self.inventory_table.setHorizontalHeaderLabels(["المكون", "الكمية", "الإجراءات"])
        self.inventory_table.setMinimumSize(800, 400)
        self.inventory_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set equal column widths
        self.inventory_table.setColumnWidth(0, 266)  # Approximately 800 / 3
        self.inventory_table.setColumnWidth(1, 266)  # Approximately 800 / 3
        self.inventory_table.setColumnWidth(2, 266)  # Approximately 800 / 3

        # Style the header
        header = self.inventory_table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #333; color: white; font-weight: bold; padding: 12px; }")
        header.setStretchLastSection(True)

        # Row height and alternating colors with hover effect
        self.inventory_table.verticalHeader().setDefaultSectionSize(50)  # Set row height
        self.inventory_table.setAlternatingRowColors(True)
        self.setStyleSheet("""  
            QWidget {
                font-size: 16px;  /* General font size */
            }
            QLabel, QLineEdit {
                font-size: 18px;  /* Labels and input fields font size */
            }
            QPushButton {
                font-size: 18px;  /* Button font size */
                font-weight: bold; /* Make button text bold */
            }
        """)

        # Inventory table styling
        self.inventory_table.setStyleSheet("""
            QTableWidget {
                font-size: 18px;  /* Larger font size for table cells */
                border: 1px solid #ddd;
                gridline-color: #ddd;
                font-weight: bold; /* Bold font for table cells */
            }
            QHeaderView::section {
                font-size: 18px;  /* Header font size */
                background-color: #333;
                color: white;
                font-weight: bold;
                padding: 15px;
            }
            QTableWidget::item {
                padding: 10px;
                min-width: 100px;  /* Minimum width for cells */
                min-height: 50px;  /* Minimum height for cells */
                font-weight: bold;  /* Bold font for table items */
                text-align: center; /* Center align text */
            }
            QTableWidget::item:alternate {
                background-color: #f9f9f9;
            }
            QTableWidget::item:selected {
                background-color: #d9edf7;
            }
            QTableWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)

        self.layout.addWidget(self.inventory_table)
        self.load_inventory_to_table()

        self.component_input = QLineEdit()
        self.quantity_input = QLineEdit()

        # Customize button styles in InventoryTab
        self.add_component_button = QPushButton("أضف مكون")
        self.add_component_button.setFixedSize(QSize(220, 50))  # Increased size for better readability
        self.add_component_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.add_component_button.clicked.connect(self.add_component)

        self.remove_component_button = QPushButton("احذف مكون")
        self.remove_component_button.setFixedSize(QSize(220, 50))  # Increased size for better readability
        self.remove_component_button.setStyleSheet("background-color: #f44336; color: white; border: none; border-radius: 5px;")
        self.remove_component_button.clicked.connect(self.remove_component)

        self.layout.addWidget(QLabel("اسم المكون:"))
        self.layout.addWidget(self.component_input)
        self.layout.addWidget(QLabel("الكمية:"))
        self.layout.addWidget(self.quantity_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_component_button)
        button_layout.addWidget(self.remove_component_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

        self.save_button = QPushButton("احفظ التغييرات")
        self.save_button.setFixedSize(QSize(220, 50))  # Increased size for better readability
        self.save_button.setStyleSheet("background-color: #2196F3; color: white; border: none; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

    def load_inventory_to_table(self):
        for item in self.data.get("inventory", []):
            self.add_table_row(item["component"], item["quantity"])

    def add_table_row(self, component, quantity):
        row_position = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row_position)

        component_item = QTableWidgetItem(component)
        component_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center align the text
        self.inventory_table.setItem(row_position, 0, component_item)

        quantity_item = QTableWidgetItem(str(quantity))
        quantity_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center align the text
        self.inventory_table.setItem(row_position, 1, quantity_item)

        # Create the widget to hold the action buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)  # Add spacing between buttons

        # Create and style the plus and minus buttons
        plus_button = QPushButton("+")
        plus_button.setFixedSize(40, 40)  # Increased size for better readability
        plus_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; font-weight: bold;")
        plus_button.clicked.connect(lambda: self.change_quantity(row_position, 1))

        minus_button = QPushButton("-")
        minus_button.setFixedSize(40, 40)  # Increased size for better readability
        minus_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; font-weight: bold;")
        minus_button.clicked.connect(lambda: self.change_quantity(row_position, -1))

        # Add buttons to the layout
        button_layout.addWidget(plus_button)
        button_layout.addWidget(minus_button)

        # Center align the buttons in the widget
        button_layout.setAlignment(Qt.AlignCenter)
        self.inventory_table.setCellWidget(row_position, 2, button_widget)

    def add_component(self):
        component_name = self.component_input.text()
        quantity = self.quantity_input.text()
        
        if not component_name or not quantity.isdigit():
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى إدخال اسم مكون صحيح وكمية.")
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
            QMessageBox.information(self, "تم حذف المكون", f"تم حذف المكون: {component_name}")
        else:
            QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار مكون للحذف.")

    def change_quantity(self, row, change):
        current_item = self.inventory_table.item(row, 1)
        if current_item:
            current_quantity = int(current_item.text())
            new_quantity = current_quantity + change
            
            if new_quantity < 0:
                QMessageBox.warning(self, "خطأ", "لا يمكن أن تكون الكمية أقل من صفر.")
                return
            
            self.inventory_table.item(row, 1).setText(str(new_quantity))
            component_name = self.inventory_table.item(row, 0).text()

            for item in self.data["inventory"]:
                if item["component"] == component_name:
                    item["quantity"] = new_quantity

    def save_data(self):
        save_data(self.data)
        QMessageBox.information(self, "تم الحفظ", "تم حفظ بيانات المخزون بنجاح.")




class EarningsTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data

        # Set layout direction to right-to-left for Arabic language support
        self.setLayoutDirection(Qt.RightToLeft)

        self.layout = QVBoxLayout()

        # Total earnings label with enhanced style
        self.total_earnings_label = QLabel("إجمالي الأرباح: $0.00")
        self.total_earnings_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.total_earnings_label)

        # Earnings table with styled header and rows
        self.earnings_table = QTableWidget()
        self.earnings_table.setColumnCount(2)
        self.earnings_table.setHorizontalHeaderLabels(["التاريخ", "الأرباح"])
        self.earnings_table.setMinimumSize(800, 400)
        self.earnings_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set equal column widths
        self.earnings_table.setColumnWidth(0, 400)
        self.earnings_table.setColumnWidth(1, 400)

        # Style header
        header = self.earnings_table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #333; color: white; font-weight: bold; padding: 12px; }")
        header.setStretchLastSection(True)

        # Row height and alternating colors with hover effect
        self.earnings_table.verticalHeader().setDefaultSectionSize(40)
        self.earnings_table.setAlternatingRowColors(True)
        self.earnings_table.setStyleSheet("""
            QTableWidget { border: 1px solid #ddd; gridline-color: #ddd; font-size: 14px; }
            QTableWidget::item { padding: 8px; text-align: center; }  /* Center-align text in items */
            QTableWidget::item:alternate { background-color: #f9f9f9; }
            QTableWidget::item:selected { background-color: #d9edf7; }
            QTableWidget::item:hover { background-color: #f5f5f5; }
        """)

        self.layout.addWidget(self.earnings_table)
        self.load_earnings_to_table()

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Customize button styles in EarningsTab
        self.remove_earning_button = QPushButton("إزالة الربح المحدد")
        self.remove_earning_button.setFixedSize(QSize(220, 60))  # Increased size for better readability
        self.remove_earning_button.setStyleSheet("background-color: #f44336; color: white; border: none; border-radius: 5px; font-weight: bold;")  # Added font-weight
        self.remove_earning_button.clicked.connect(self.remove_earning)

        self.remove_all_button = QPushButton("إزالة جميع الأرباح")
        self.remove_all_button.setFixedSize(QSize(220, 60))  # Increased size for better readability
        self.remove_all_button.setStyleSheet("background-color: #f44336; color: white; border: none; border-radius: 5px; font-weight: bold;")  # Added font-weight
        self.remove_all_button.clicked.connect(self.remove_all_earnings)

        # Center-align the buttons in the horizontal layout
        button_layout.addStretch()
        button_layout.addWidget(self.remove_earning_button)
        button_layout.addWidget(self.remove_all_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def load_earnings_to_table(self):
        total_earnings = 0
        self.earnings_table.setRowCount(0)  # Clear the table before loading
        for earning in self.data.get("earnings", []):
            row_position = self.earnings_table.rowCount()
            self.earnings_table.insertRow(row_position)

            date_item = QTableWidgetItem(earning["date"])
            date_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # Center-align text
            date_item.setFont(QFont("Arial", 12, QFont.Bold))  # Set font to bold and size 12
            self.earnings_table.setItem(row_position, 0, date_item)

            amount_item = QTableWidgetItem(f"${earning['amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # Center-align text
            amount_item.setFont(QFont("Arial", 12, QFont.Bold))  # Set font to bold and size 12
            self.earnings_table.setItem(row_position, 1, amount_item)

            total_earnings += earning["amount"]

        self.update_total_earnings(total_earnings)

    def add_earning(self, amount):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        earning_data = {"date": date, "amount": float(amount)}
        self.data["earnings"].append(earning_data)

        row_position = self.earnings_table.rowCount()
        self.earnings_table.insertRow(row_position)

        date_item = QTableWidgetItem(date)
        date_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # Center-align text
        date_item.setFont(QFont("Arial", 12, QFont.Bold))  # Set font to bold and size 12
        self.earnings_table.setItem(row_position, 0, date_item)

        amount_item = QTableWidgetItem(f"${float(amount):.2f}")
        amount_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # Center-align text
        amount_item.setFont(QFont("Arial", 12, QFont.Bold))  # Set font to bold and size 12
        self.earnings_table.setItem(row_position, 1, amount_item)

        # Update total earnings
        total_earnings = sum(earning["amount"] for earning in self.data.get("earnings", []))
        self.update_total_earnings(total_earnings)

    def update_total_earnings(self, total):
        self.total_earnings_label.setText(f"إجمالي الأرباح: ${total:.2f}")

    def remove_earning(self):
        current_row = self.earnings_table.currentRow()
        if current_row != -1:
            amount = float(self.earnings_table.item(current_row, 1).text().replace("$", ""))
            self.data["earnings"].pop(current_row)
            self.earnings_table.removeRow(current_row)
            total_earnings = sum(earning["amount"] for earning in self.data.get("earnings", []))
            self.update_total_earnings(total_earnings)
            QMessageBox.information(self, "تمت الإزالة", f"تمت إزالة ربح قدره ${amount:.2f} بنجاح.")
        else:
            QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار ربح للإزالة.")

    def remove_all_earnings(self):
        confirm = QMessageBox.question(self, "تأكيد الإزالة", "هل أنت متأكد أنك تريد إزالة جميع الأرباح؟", 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.data["earnings"].clear()
            self.earnings_table.setRowCount(0)
            self.update_total_earnings(0)
            QMessageBox.information(self, "تمت الإزالة", "تمت إزالة جميع الأرباح.")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarbershopApp()
    window.show()
    sys.exit(app.exec_())
