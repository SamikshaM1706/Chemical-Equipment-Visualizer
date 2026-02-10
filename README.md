# Chemical Equipment Visualizer

A hybrid Web + Desktop application for analyzing and visualizing chemical equipment data using CSV files.

---

## Project Overview
This project allows users to upload chemical equipment data and view:
- Summary statistics
- Equipment type distribution
- Visual graphs

It is implemented using:
- Django (backend API)
- React (web frontend)
- PyQt5 (desktop application)

---

## Folder Structure
ChemicalVisualizer/
│
├── backend/ # Django backend
├── web-frontend/ # React frontend
├── desktop_app.py # PyQt desktop application
├── sample_equipment_data.csv
└── README.md

---

## How to Run the Project

### 1. Backend (Django)
```bash
cd backend
python manage.py runserver
Backend will run at: http://127.0.0.1:8000

### 2. Frontend(React)
cd web-frontend
npm install
npm start

3. Desktop Application (PyQt)
python desktop_app.py

Technologies Used:
Python
Django
PyQt5
React
JavaScript
HTML / CSS
Matplotlib

Author:
Samiksha Mate

