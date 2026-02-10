import sys
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QTabWidget, 
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

API_URL = "http://127.0.0.1:8000"

# Global Stylesheet
STYLESHEET = """
    QWidget {
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        background-color: #f3f4f6;
        color: #111827;
    }
    
    QLabel {
        color: #111827;
    }
    
    QLineEdit {
        border: 1px solid #e2e8f0;
        padding: 8px;
        background-color: #ffffff;
        border-radius: 0px; 
    }
    
    QPushButton {
        background-color: #4f46e5;
        color: white;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
        border-radius: 0px;
    }
    
    QPushButton:hover {
        background-color: #4338ca;
    }
    
    QTabWidget::pane {
        border: 1px solid #e2e8f0;
        background: #ffffff;
        border-radius: 0px;
    }
    
    QTabBar::tab {
        background: #e2e8f0;
        padding: 10px 20px;
        margin-right: 2px;
        border-radius: 0px;
    }
    
    QTabBar::tab:selected {
        background: #ffffff;
        border-bottom: 2px solid #4f46e5;
    }
    
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        gridline-color: #e2e8f0;
        border-radius: 0px;
    }
    
    QHeaderView::section {
        background-color: #f9fafb;
        padding: 8px;
        border: none;
        border-bottom: 1px solid #e2e8f0;
        font-weight: bold;
        color: #6b7280;
    }

    QFrame.Card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0px;
    }
"""

class StatCard(QFrame):
    def __init__(self, title, value, unit="", color="#111827"):
        super().__init__()
        self.setProperty("class", "Card")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #6b7280; font-size: 12px; font-weight: 500;")
        layout.addWidget(self.title_label)
        
        value_layout = QHBoxLayout()
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
        value_layout.addWidget(self.value_label)
        
        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet("color: #6b7280; font-size: 12px; margin-top: 8px;")
            value_layout.addWidget(unit_label)
            value_layout.addStretch()
            
        layout.addLayout(value_layout)
        self.setLayout(layout)

    def update_value(self, value):
        self.value_label.setText(str(value))

class LoginWindow(QWidget):
    def __init__(self, switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main
        self.setWindowTitle("Login - Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet(STYLESHEET)
        
        # Center layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        card = QFrame()
        card.setProperty("class", "Card")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        title = QLabel("Chemical Equipment Parameter Visualizer Login")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4f46e5; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        card_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        card.setLayout(card_layout)
        main_layout.addWidget(card)
        
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        try:
            response = requests.post(f"{API_URL}/api-token-auth/", data={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                token = response.json()["token"]
                self.switch_to_main(token)
            else:
                QMessageBox.critical(self, "Login Failed", "Invalid credentials")
        except requests.exceptions.ConnectionError:
             QMessageBox.critical(self, "Connection Error", "Could not connect to backend")


class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1000, 700)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.dashboard_tab = QWidget()
        self.history_tab = QWidget()
        
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.history_tab, "History")
        
        self.setup_dashboard()
        self.setup_history()

    def setup_dashboard(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Stat Cards Grid
        stats_layout = QGridLayout()
        self.card_total = StatCard("Total Equipment", "0", "", "#4f46e5")
        self.card_flow = StatCard("Avg Flowrate", "0.00", "m³/h")
        self.card_press = StatCard("Avg Pressure", "0.00", "bar")
        self.card_temp = StatCard("Avg Temperature", "0.00", "°C")
        
        stats_layout.addWidget(self.card_total, 0, 0)
        stats_layout.addWidget(self.card_flow, 0, 1)
        stats_layout.addWidget(self.card_press, 0, 2)
        stats_layout.addWidget(self.card_temp, 0, 3)
        layout.addLayout(stats_layout)
        
        # Upload Section (Card style)
        upload_frame = QFrame()
        upload_frame.setProperty("class", "Card")
        upload_layout = QHBoxLayout()
        upload_layout.setContentsMargins(20, 20, 20, 20)
        
        self.file_label = QLabel("No file selected")
        upload_layout.addWidget(self.file_label)
        
        btn_select = QPushButton("Select CSV")
        btn_select.setCursor(Qt.PointingHandCursor)
        btn_select.setStyleSheet("background-color: #64748b;")
        btn_select.clicked.connect(self.select_file)
        upload_layout.addWidget(btn_select)
        
        btn_upload = QPushButton("Upload & Analyze")
        btn_upload.setCursor(Qt.PointingHandCursor)
        btn_upload.clicked.connect(self.upload_file)
        upload_layout.addWidget(btn_upload)
        
        upload_frame.setLayout(upload_layout)
        layout.addWidget(upload_frame)
        
        # Chart Section
        chart_frame = QFrame()
        chart_frame.setProperty("class", "Card")
        chart_layout = QVBoxLayout()
        
        title = QLabel("Equipment Type Distribution")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        chart_layout.addWidget(title)
        
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        
        chart_frame.setLayout(chart_layout)
        layout.addWidget(chart_frame, stretch=1)
        
        self.dashboard_tab.setLayout(layout)

    def setup_history(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        top_bar = QHBoxLayout()
        title = QLabel("Recent Upload History")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar.addWidget(title)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.load_history)
        top_bar.addWidget(self.refresh_btn)
        layout.addLayout(top_bar)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "ID", "Date", "Total Eq.", "Avg Flow", "Avg Press", "Action"
        ])
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setFixedHeight(40)
        
        self.history_table.verticalHeader().setDefaultSectionSize(50)
        
        layout.addWidget(self.history_table)
        
        self.history_tab.setLayout(layout)
        self.load_history()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path.split("/")[-1])

    def upload_file(self):
        if not hasattr(self, 'file_path'):
            QMessageBox.warning(self, "Warning", "Please select a file first")
            return

        files = {'file': open(self.file_path, 'rb')}
        headers = {'Authorization': f'Token {self.token}'}
        
        try:
            response = requests.post(f"{API_URL}/api/upload/", files=files, headers=headers)
            if response.status_code == 200:
                self.display_summary(response.json())
                self.load_history() # Refresh history
            else:
                 QMessageBox.critical(self, "Error", f"Upload failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_summary(self, data):
        self.card_total.update_value(data['total_equipment'])
        self.card_flow.update_value(f"{data['average_flowrate']:.2f}")
        self.card_press.update_value(f"{data['average_pressure']:.2f}")
        self.card_temp.update_value(f"{data['average_temperature']:.2f}")
        
        # Update Chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        types = list(data['type_distribution'].keys())
        counts = list(data['type_distribution'].values())
        
        ax.bar(types, counts, color="#4f46e5", alpha=0.7)
        ax.set_ylabel("Count")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        self.canvas.draw()

    def load_history(self):
        headers = {'Authorization': f'Token {self.token}'}
        try:
            response = requests.get(f"{API_URL}/api/history/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.history_table.setRowCount(len(data))
                for i, row in enumerate(data):
                    self.history_table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                    self.history_table.setItem(i, 1, QTableWidgetItem(row['created_at'].split('T')[0]))
                    self.history_table.setItem(i, 2, QTableWidgetItem(str(row['total_equipment'])))
                    self.history_table.setItem(i, 3, QTableWidgetItem(f"{row['average_flowrate']:.2f}"))
                    self.history_table.setItem(i, 4, QTableWidgetItem(f"{row['average_pressure']:.2f}"))
                    
                    btn = QPushButton("PDF Report")
                    btn.setStyleSheet("background-color: #10b981; padding: 5px;")
                    btn.setCursor(Qt.PointingHandCursor)
                    btn.clicked.connect(lambda checked, r=row: self.download_pdf(r['id']))
                    
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.addWidget(btn)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.history_table.setCellWidget(i, 5, widget)
        except Exception as e:
            print("Error loading history:", e)

    def download_pdf(self, upload_id):
        headers = {'Authorization': f'Token {self.token}'}
        try:
            response = requests.get(f"{API_URL}/api/report/{upload_id}/", headers=headers)
            if response.status_code == 200:
                save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"report_{upload_id}.pdf", "PDF Files (*.pdf)")
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, "Success", "PDF Saved Successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to download PDF")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET) # Apply global styles
    
    def start_main(token):
        window.close()
        main_win = MainWindow(token)
        main_win.show()
        # Keep reference to avoid garbage collection
        app.main_win = main_win 

    window = LoginWindow(start_main)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
