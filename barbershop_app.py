import sys
import json
import os
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
    QSizePolicy,
    QComboBox
)
from PyQt5.QtGui import QFont, QPainter, QPixmap, QIcon  
from PyQt5.QtCore import Qt, QSize, QSizeF, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog  
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
            if "customers" not in data:
                data["customers"] = []
            if "monthly_earnings" not in data:  
                data["monthly_earnings"] = []  
            if "expenses" not in data:  # Add this line for expenses
                data["expenses"] = []  # Initialize expenses if not present
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "packages": [], "inventory": [], "earnings": [], 
            "customers": [], "monthly_earnings": [], "expenses": []  # Include expenses
        }

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

class BarbershopApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Beko Barber")
        self.setGeometry(100, 100, 1000, 800)

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
        self.logo_pixmap = QPixmap(self.resource_path("beko.jpg")).scaled(300, 100, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)  # Don't forget to add logo_label to layout

        # Set application icon
        self.setWindowIcon(QIcon(self.resource_path("beko.ico")))  # Ensure you reference the ICO file

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget) 

        # Add tabs
        self.earnings_tab = EarningsTab(self.data)
        self.packages_tab = PackagesTab(self.data, self.earnings_tab)
        self.inventory_tab = InventoryTab(self.data)
        self.customer_tab = CustomersTab(self.data)
        self.monthly_earnings_tab = MonthlyEarningsTab(self.data)
        self.expenses_tab = ExpensesTab(self.data)  # Add the ExpensesTab

        self.tab_widget.addTab(self.packages_tab, "الباقات")
        self.tab_widget.addTab(self.inventory_tab, "المخزون")
        self.tab_widget.addTab(self.earnings_tab, "الأرباح")
        self.tab_widget.addTab(self.customer_tab, "العملاء")
        self.tab_widget.addTab(self.monthly_earnings_tab, "الأرباح الشهرية")
        self.tab_widget.addTab(self.expenses_tab, "المصروفات")  # Add the tab for المصروفات
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

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

                # Create the receipt message with line breaks for organization
                receipt_message = (
                    f"السعر: {price}\n\n"  # Price in Arabic
                    f"الباقة: {description}\n\n"  # Package in Arabic
                    "صالون بيكو تشرف بوجود حضراتكم"  # Footer in Arabic
                )

                # Preview the receipt before printing
                self.preview_receipt(receipt_message)
                # Add the earnings after printing is confirmed
                self.earnings_tab.add_earning(price)
            else:
                QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار باقة للدفع.")

    def preview_receipt(self, message):
        # Create a printer object for previewing
        printer = QPrinter(QPrinter.HighResolution)
        
        # Set the paper size to 80 mm width and a custom height for roll printing
        custom_size = QSizeF(80, 300)  # 80 mm width, 300 mm height (or as needed)
        printer.setPaperSize(custom_size, QPrinter.Millimeter)  # Set the custom size in millimeters

        # Set up the print preview dialog
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(lambda p: self.render_receipt(p, message))
        preview_dialog.exec_()
        

    def render_receipt(self, printer, message):
        painter = QPainter(printer)

        # Draw the logo at a higher position with a larger size
        logo = QIcon("beko.ico").pixmap(100, 100)  # Increased size for visibility on 80mm paper
        logo_x = (printer.pageRect().width() - logo.width()) // 2
        painter.drawPixmap(logo_x, 10, logo)  # Positioned near the top

        # Draw the title below the logo with more space
        font = QFont("Arial", 18, QFont.Bold)
        painter.setFont(font)
        title = "Beko Barber"
        title_x = (printer.pageRect().width() - painter.fontMetrics().width(title)) // 2
        painter.drawText(title_x, 130, title)  # Adjusted y-position to avoid overlapping

        # Set a smaller font size for the Arabic content
        content_font = QFont("Arial", 10)
        painter.setFont(content_font)

        # Start drawing Arabic text with adjusted line height and padding to prevent cutting
        y = 170  # Start position for the Arabic content after title

        # Loop to draw each line with sufficient padding
        for line in message.split('\n'):
            rect = QRect(10, y, printer.pageRect().width() - 20, 30)  # 30px height per line for better fit
            painter.drawText(rect, Qt.AlignRight | Qt.AlignVCenter, line)
            y += 35  # Add extra padding between lines

        painter.end()



    def print_receipt(self, message):
        # Create a printer object for actual printing
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QSizeF(58, 200), QPrinter.Millimeter)  # Set size to match receipt printer width

        # Show the print dialog for printer selection and preview
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)

            # Render receipt in the same way as preview
            self.render_receipt(printer, message)
            
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
        self.inventory_table.setColumnCount(4)  # Updated to 4 columns
        self.inventory_table.setHorizontalHeaderLabels(["المكون", "الكمية", "السعر", "الاجرائات"])
        self.inventory_table.setMinimumSize(800, 400)
        self.inventory_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set equal column widths
        self.inventory_table.setColumnWidth(0, 200)
        self.inventory_table.setColumnWidth(1, 200)
        self.inventory_table.setColumnWidth(2, 200)  # New column for السعر
        self.inventory_table.setColumnWidth(3, 200)

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

        # Input fields for adding components
        self.component_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()  # New input for price

        # Customize button styles in InventoryTab
        self.add_component_button = QPushButton("أضف مكون")
        self.add_component_button.setFixedSize(QSize(220, 50))  # Increased size for better readability
        self.add_component_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.add_component_button.clicked.connect(self.add_component)

        self.remove_component_button = QPushButton("احذف مكون")
        self.remove_component_button.setFixedSize(QSize(220, 50))  # Increased size for better readability
        self.remove_component_button.setStyleSheet("background-color: #f44336; color: white; border: none; border-radius: 5px;")
        self.remove_component_button.clicked.connect(self.remove_component)

        # Adding the input fields and labels to the layout
        self.layout.addWidget(QLabel("اسم المكون:"))
        self.layout.addWidget(self.component_input)
        self.layout.addWidget(QLabel("الكمية:"))
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(QLabel("السعر:"))  # New label for price
        self.layout.addWidget(self.price_input)  # New input field for price

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
            self.add_table_row(item["component"], item["quantity"], item.get("price", "0"))

    def add_table_row(self, component, quantity, price="0"):
        row_position = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row_position)

        component_item = QTableWidgetItem(component)
        component_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center align the text
        self.inventory_table.setItem(row_position, 0, component_item)

        quantity_item = QTableWidgetItem(str(quantity))
        quantity_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center align the text
        self.inventory_table.setItem(row_position, 1, quantity_item)

        price_item = QTableWidgetItem(str(price))  # New price item
        price_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center align the text
        self.inventory_table.setItem(row_position, 2, price_item)

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
        self.inventory_table.setCellWidget(row_position, 3, button_widget)  # Updated index for actions column

    def add_component(self):
        component_name = self.component_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()  # Retrieve the price input
        
        if not component_name or not quantity.isdigit() or not price.isdigit():
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى إدخال اسم مكون صحيح وكمية وسعر.")
            return

        self.add_table_row(component_name, quantity, price)
        self.data["inventory"].append({"component": component_name, "quantity": int(quantity), "price": int(price)})
        
        self.component_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()  # Clear the price input after adding

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
            
            
            
class CustomersTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data

        # Set layout direction to right-to-left
        self.setLayoutDirection(Qt.RightToLeft)

        self.layout = QVBoxLayout()

        # Customers table with enhanced style and layout
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(4)
        self.customers_table.setHorizontalHeaderLabels(["الاسم", "رقم الموبايل", "عدد الزيارات", "الاجرائات"])
        self.customers_table.setMinimumSize(800, 400)
        self.customers_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set equal column widths
        for i in range(4):
            self.customers_table.setColumnWidth(i, 200)  # Adjust width as needed

        # Style the header
        header = self.customers_table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #333; color: white; font-weight: bold; padding: 12px; }")
        header.setStretchLastSection(True)

        # Row height and alternating colors with hover effect
        self.customers_table.verticalHeader().setDefaultSectionSize(50)  # Set row height
        self.customers_table.setAlternatingRowColors(True)
        self.customers_table.setStyleSheet("""
            QTableWidget {
                font-size: 18px;
                border: 1px solid #ddd;
                gridline-color: #ddd;
                font-weight: bold;
            }
            QHeaderView::section {
                font-size: 18px;
                background-color: #333;
                color: white;
                font-weight: bold;
                padding: 15px;
            }
            QTableWidget::item {
                padding: 10px;
                min-width: 100px;
                min-height: 50px;
                font-weight: bold;
                text-align: center;
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

        self.layout.addWidget(self.customers_table)
        self.load_customers_to_table()

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن عميل")
        self.search_input.setStyleSheet("font-size: 20px; padding: 8px;")  # Make the text more readable
        self.search_input.textChanged.connect(self.search_customer)
        self.layout.addWidget(self.search_input, alignment=Qt.AlignTop | Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.mobile_input = QLineEdit()

        # Add and remove buttons for customers
        self.add_customer_button = QPushButton("أضف عميل")
        self.add_customer_button.setFixedSize(QSize(220, 50))
        self.add_customer_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px; font-weight: bold; font-size: 16px;")
        self.add_customer_button.clicked.connect(self.add_customer)

        self.remove_customer_button = QPushButton("احذف عميل")
        self.remove_customer_button.setFixedSize(QSize(220, 50))
        self.remove_customer_button.setStyleSheet("background-color: #f44336; color: white; border: none; border-radius: 5px; font-weight: bold; font-size: 16px;")
        self.remove_customer_button.clicked.connect(self.remove_customer)

        self.save_changes_button = QPushButton("احفظ التغييرات")
        self.save_changes_button.setFixedSize(QSize(220, 50))
        self.save_changes_button.setStyleSheet("background-color: #2196F3; color: white; border: none; border-radius: 5px; font-weight: bold; font-size: 16px;")
        self.save_changes_button.clicked.connect(self.save_changes)

        self.layout.addWidget(QLabel("الاسم:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("رقم الموبايل:"))
        self.layout.addWidget(self.mobile_input)

        # Adjust button layout to position the save button in the bottom-left corner
        button_layout = QVBoxLayout()

        # Centering the "أضف عميل" and "احذف عميل" buttons side by side
        center_buttons_layout = QHBoxLayout()
        center_buttons_layout.addWidget(self.add_customer_button)
        center_buttons_layout.addWidget(self.remove_customer_button)
        center_buttons_layout.setAlignment(Qt.AlignCenter)

        # Add the save button to the bottom left
        button_layout.addLayout(center_buttons_layout)
        button_layout.addWidget(self.save_changes_button, alignment=Qt.AlignLeft)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def search_customer(self):
        search_text = self.search_input.text().lower()
        for row in range(self.customers_table.rowCount()):
            item = self.customers_table.item(row, 0)  # Assuming name is in the first column
            self.customers_table.setRowHidden(row, search_text not in item.text().lower())

    def load_customers_to_table(self):
        for customer in self.data.get("customers", []):
            name = customer["name"]
            mobile = customer["mobile"]
            visits = customer.get("visits", 0)  # Default to 0 if not in data
            self.add_table_row(name, mobile, visits)

    def add_table_row(self, name, mobile, visits=0):
        row_position = self.customers_table.rowCount()
        self.customers_table.insertRow(row_position)

        name_item = QTableWidgetItem(name)
        name_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.customers_table.setItem(row_position, 0, name_item)

        mobile_item = QTableWidgetItem(mobile)
        mobile_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.customers_table.setItem(row_position, 1, mobile_item)

        visits_item = QTableWidgetItem(str(visits))
        visits_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.customers_table.setItem(row_position, 2, visits_item)

        # Create action buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        plus_button = QPushButton("+")
        plus_button.setFixedSize(40, 40)
        plus_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; font-weight: bold;")
        plus_button.clicked.connect(lambda _, row=row_position: self.increment_visits(row))

        minus_button = QPushButton("-")
        minus_button.setFixedSize(40, 40)
        minus_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; font-weight: bold;")
        minus_button.clicked.connect(lambda _, row=row_position: self.decrement_visits(row))

        button_layout.addWidget(plus_button)
        button_layout.addWidget(minus_button)
        button_layout.setAlignment(Qt.AlignCenter)
        self.customers_table.setCellWidget(row_position, 3, button_widget)

    def increment_visits(self, row):
        visits_item = self.customers_table.item(row, 2)
        current_visits = int(visits_item.text())
        visits_item.setText(str(current_visits + 1))

    def decrement_visits(self, row):
        visits_item = self.customers_table.item(row, 2)
        current_visits = int(visits_item.text())
        visits_item.setText(str(max(current_visits - 1, 0)))  # Prevent negative values

    def add_customer(self):
        name = self.name_input.text()
        mobile = self.mobile_input.text()

        if not name or not mobile:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى إدخال اسم ورقم موبايل صحيح.")
            return

        self.add_table_row(name, mobile)
        self.data["customers"].append({"name": name, "mobile": mobile, "visits": 0})

        self.name_input.clear()
        self.mobile_input.clear()

    def remove_customer(self):
        current_row = self.customers_table.currentRow()
        if current_row != -1:
            name = self.customers_table.item(current_row, 0).text()
            self.data["customers"] = [customer for customer in self.data["customers"] if customer["name"] != name]
            self.customers_table.removeRow(current_row)
            QMessageBox.information(self, "تم حذف العميل", f"تم حذف العميل: {name}")
        else:
            QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار عميل للحذف.")

    def save_changes(self):
        # Update visits in the data dictionary
        for row in range(self.customers_table.rowCount()):
            name = self.customers_table.item(row, 0).text()
            visits = int(self.customers_table.item(row, 2).text())
            for customer in self.data["customers"]:
                if customer["name"] == name:
                    customer["visits"] = visits

        QMessageBox.information(self, "حفظ التغييرات", "تم حفظ التغييرات بنجاح.")
        
        
class MonthlyEarningsTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data

        # Ensure 'monthly_earnings' key exists in data
        if "monthly_earnings" not in self.data:
            self.data["monthly_earnings"] = []

        # Set layout direction to right-to-left for Arabic language support
        self.setLayoutDirection(Qt.RightToLeft)

        self.layout = QVBoxLayout()

        # Table for displaying monthly earnings (remove the "إجراء" column)
        self.earnings_table = QTableWidget()
        self.earnings_table.setColumnCount(2)  # Remove the "إجراء" column
        self.earnings_table.setHorizontalHeaderLabels(["الشهر", "الربح"])
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
            QTableWidget::item { padding: 8px; text-align: center; }
            QTableWidget::item:alternate { background-color: #f9f9f9; }
            QTableWidget::item:selected { background-color: #d9edf7; }
            QTableWidget::item:hover { background-color: #f5f5f5; }
        """)

        self.layout.addWidget(self.earnings_table)

        # Load existing earnings data into the table
        self.load_earnings_table()

        # Text fields and buttons moved to bottom
        self.monthly_earnings_label = QLabel("أرباح الشهر:")
        self.monthly_earnings_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")

        self.earnings_input = QLineEdit()
        self.earnings_input.setPlaceholderText("أدخل أرباح الشهر")
        self.earnings_input.setStyleSheet("padding: 8px; font-size: 14px;")

        self.month_dropdown = QComboBox()
        months_arabic = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
        self.month_dropdown.addItems(months_arabic)
        self.month_dropdown.setStyleSheet("padding: 8px; font-size: 18px;")

        self.add_earnings_button = QPushButton("إضافة الربح")
        self.add_earnings_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px 24px; font-weight: bold; border-radius: 5px; text-align: center;")
        self.add_earnings_button.clicked.connect(self.add_monthly_earning)

        self.remove_earnings_button = QPushButton("ازاله الربح")
        self.remove_earnings_button.setStyleSheet("background-color: #FF5733; color: white; padding: 12px 24px; font-weight: bold; border-radius: 5px; text-align: center;")
        self.remove_earnings_button.clicked.connect(self.remove_selected_earning)

        # Layout for text fields and buttons (center the buttons)
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.monthly_earnings_label)
        bottom_layout.addWidget(self.earnings_input)
        bottom_layout.addWidget(self.month_dropdown)

        # Center buttons and set them with bold text
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add space to left
        button_layout.addWidget(self.add_earnings_button)
        button_layout.addWidget(self.remove_earnings_button)
        button_layout.addStretch()  # Add space to right

        bottom_layout.addLayout(button_layout)

        # Add bottom layout to main layout
        self.layout.addLayout(bottom_layout)
        self.setLayout(self.layout)

    def add_monthly_earning(self):
        """ Add monthly earnings to the data and table """
        earnings_value = self.earnings_input.text().strip()
        selected_month = self.month_dropdown.currentText()
        if earnings_value:
            try:
                earnings_amount = float(earnings_value)
                entry = {"month": selected_month, "amount": earnings_amount}
                self.data["monthly_earnings"].append(entry)  # Add to data
                self.earnings_input.clear()  # Clear the input field after adding
                QMessageBox.information(self, "نجاح", f"تمت إضافة أرباح {earnings_amount} لشهر {selected_month} بنجاح.")
                self.add_earning_to_table(selected_month, earnings_amount)  # Add entry to table
            except ValueError:
                QMessageBox.warning(self, "خطأ في المدخلات", "يرجى إدخال قيمة عددية صحيحة للأرباح.")
        else:
            QMessageBox.warning(self, "خطأ في المدخلات", "يرجى ملء حقل الأرباح قبل إضافة الربح.")

    def load_earnings_table(self):
        """ Load earnings data into the table """
        for entry in self.data["monthly_earnings"]:
            self.add_earning_to_table(entry["month"], entry["amount"])

    def add_earning_to_table(self, month, amount):
        """ Add an earning entry to the table """
        row_position = self.earnings_table.rowCount()
        self.earnings_table.insertRow(row_position)

        month_item = QTableWidgetItem(month)
        month_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        month_item.setFont(QFont("Arial", 12, QFont.Bold))
        self.earnings_table.setItem(row_position, 0, month_item)

        amount_item = QTableWidgetItem(str(amount))
        amount_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        amount_item.setFont(QFont("Arial", 12, QFont.Bold))
        self.earnings_table.setItem(row_position, 1, amount_item)

    def remove_selected_earning(self):
        """ Remove the selected earning from the table and data """
        selected_row = self.earnings_table.currentRow()  # Get the selected row
        if selected_row >= 0:
            # Get the month and amount of the selected row
            month = self.earnings_table.item(selected_row, 0).text() if self.earnings_table.item(selected_row, 0) else None
            amount = self.earnings_table.item(selected_row, 1).text() if self.earnings_table.item(selected_row, 1) else None
            
            if month and amount:
                # Remove from data
                self.data["monthly_earnings"] = [
                    entry for entry in self.data["monthly_earnings"] if entry["month"] != month or str(entry["amount"]) != amount
                ]
                # Remove from table
                self.earnings_table.removeRow(selected_row)
                QMessageBox.information(self, "تم الحذف", f"تمت إزالة أرباح {amount} لشهر {month} بنجاح.")
            else:
                QMessageBox.warning(self, "خطأ", "لم يتم العثور على العناصر للحذف.")
        else:
            QMessageBox.warning(self, "خطأ", "يرجى اختيار صف للحذف.")



class ExpensesTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
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
        form_layout.addRow("المبلغ:", self.price_input)
        form_layout.setAlignment(Qt.AlignRight)

        # Button styles, sizes, and font
        button_font = QFont("Arial", 14)

        # Add Expense Button
        self.add_expense_button = QPushButton("إضافة")
        self.add_expense_button.setFont(button_font)
        self.add_expense_button.setFixedSize(QSize(150, 40))
        self.add_expense_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        self.add_expense_button.clicked.connect(self.add_expense)

        # Remove Selected Button
        self.remove_selected_button = QPushButton("إزالة المحدد")
        self.remove_selected_button.setFont(button_font)
        self.remove_selected_button.setFixedSize(QSize(200, 40))
        self.remove_selected_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        self.remove_selected_button.clicked.connect(self.remove_selected)

        # Expenses Table
        self.expenses_table = QTableWidget()
        self.expenses_table.setColumnCount(2)
        self.expenses_table.setHorizontalHeaderLabels(["الوصف", "المبلغ"])
        self.expenses_table.setLayoutDirection(Qt.RightToLeft)

        # Table styling
        self.expenses_table.setFont(QFont("Arial", 16, QFont.Bold))
        self.expenses_table.setMinimumSize(700, 400)
        self.expenses_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        column_width = 350
        self.expenses_table.setColumnWidth(0, column_width)
        self.expenses_table.setColumnWidth(1, column_width)

        header = self.expenses_table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #333; color: white; font-weight: bold; padding: 10px; }")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStretchLastSection(True)

        self.expenses_table.verticalHeader().setDefaultSectionSize(50)
        self.expenses_table.setAlternatingRowColors(True)
        self.expenses_table.setStyleSheet("""
            QTableWidget {
                font-size: 16px;
                border: 1px solid #ddd;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                text-align: center;
                font-weight: bold;
            }
        """)

        self.layout.addWidget(self.expenses_table)
        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_expense_button)
        button_layout.addWidget(self.remove_selected_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)
        self.load_expenses_to_table()
        

    def load_expenses_to_table(self):
        for expense in self.data.get("expenses", []):
            row_position = self.expenses_table.rowCount()
            self.expenses_table.insertRow(row_position)
            description_item = QTableWidgetItem(expense["description"])
            description_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.expenses_table.setItem(row_position, 0, description_item)
            amount_item = QTableWidgetItem(str(expense["amount"]))
            amount_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.expenses_table.setItem(row_position, 1, amount_item)

    def add_expense(self):
        description = self.description_input.text()
        amount = self.price_input.text()

        if not description or not amount:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى ملء جميع الحقول.")
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى إدخال مبلغ صحيح.")
            return

        expense_data = {"description": description, "amount": amount}
        self.data["expenses"].append(expense_data)

        row_position = self.expenses_table.rowCount()
        self.expenses_table.insertRow(row_position)
        description_item = QTableWidgetItem(description)
        description_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.expenses_table.setItem(row_position, 0, description_item)
        amount_item = QTableWidgetItem(str(amount))
        amount_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.expenses_table.setItem(row_position, 1, amount_item)

        QMessageBox.information(self, "تمت الإضافة", f"تمت إضافة المصروف:\nالوصف: {description}\nالمبلغ: {amount}")
        self.description_input.clear()
        self.price_input.clear()

    def remove_selected(self):
        selected_indexes = self.expenses_table.selectedIndexes()

        if selected_indexes:
            rows_to_remove = set(index.row() for index in selected_indexes if index.column() == 0)

            if rows_to_remove:
                for row in sorted(rows_to_remove, reverse=True):
                    # Remove data from the data source
                    description = self.expenses_table.item(row, 0).text()
                    amount = self.expenses_table.item(row, 1).text()

                    self.data["expenses"] = [
                        expense for expense in self.data["expenses"]
                        if not (expense["description"] == description and str(expense["amount"]) == amount)
                    ]

                    # Remove row from the table
                    self.expenses_table.removeRow(row)

                QMessageBox.information(self, "تم الحذف", "تمت إزالة المصروفات المحددة.")
            else:
                QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار المصروفات من عمود الوصف.")
        else:
            QMessageBox.warning(self, "خطأ في الاختيار", "يرجى اختيار المصروفات المراد إزالتها.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarbershopApp()
    window.show()
    sys.exit(app.exec_())
