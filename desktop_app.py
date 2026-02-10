import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f4f6f8;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        # ---------- Header ----------
        self.title = QLabel("Chemical Equipment Data Analyzer")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # ---------- Upload Section ----------
        upload_card = QFrame()
        upload_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
            """
        )
        upload_layout = QVBoxLayout(upload_card)

        self.info_label = QLabel("Upload a CSV file to analyze equipment parameters")
        self.info_label.setFont(QFont("Arial", 11))
        self.info_label.setAlignment(Qt.AlignCenter)
        upload_layout.addWidget(self.info_label)

        self.upload_btn = QPushButton("📂 Choose CSV File")
        self.upload_btn.setFont(QFont("Arial", 11))
        self.upload_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        self.upload_btn.clicked.connect(self.choose_file)
        upload_layout.addWidget(self.upload_btn)

        self.layout.addWidget(upload_card)

        # ---------- Plot Area ----------
        plot_card = QFrame()
        plot_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
            """
        )
        plot_layout = QVBoxLayout(plot_card)

        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.ax = self.canvas.figure.add_subplot(111)
        plot_layout.addWidget(self.canvas)

        self.layout.addWidget(plot_card)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.upload_csv(file_path)

    def upload_csv(self, file_path):
        url = "http://127.0.0.1:8000/api/upload/"
        files = {'file': open(file_path, 'rb')}

        try:
            response = requests.post(url, files=files)
            data = response.json()['summary']

            # Show stats
            stats_text = (
                f"<b>Total Equipment:</b> {data['total_count']}<br>"
                f"<b>Average Flowrate:</b> {data['avg_flowrate']}<br>"
                f"<b>Average Pressure:</b> {data['avg_pressure']}<br>"
                f"<b>Average Temperature:</b> {data['avg_temperature']}"
            )
            self.info_label.setText(stats_text)

            # Plot
            self.ax.clear()
            types = list(data['type_distribution'].keys())
            counts = list(data['type_distribution'].values())

            self.ax.bar(types, counts)
            self.ax.set_title("Equipment Type Distribution")
            self.ax.set_ylabel("Count")

            self.canvas.draw()

        except Exception as e:
            self.info_label.setText(f"❌ Upload failed: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
