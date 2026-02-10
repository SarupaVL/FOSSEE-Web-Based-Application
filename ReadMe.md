# Chemical Equipment Parameter Visualizer

This is a hybrid web and desktop application developed for the FOSSEE IIT Bombay Intern Screening Task. It allows users to upload, analyze, and visualize chemical equipment data from CSV files.

The project consists of three main components:
1.  **Backend (Django)** - Handles API requests, data processing, and authentication.
2.  **Web Frontend (React.js)** - A responsive dashboard for data visualization.
3.  **Desktop App (PyQt5)** - A native desktop client with the same functionality.

## Features Implemented

-   **Data Processing**: Uploads CSV files to calculate total equipment count, average parameters (Flowrate, Pressure, Temperature), and type distribution.
-   **Visualization**:
    -   Web: Interactive Bar Charts using Chart.js.
    -   Desktop: Embedded Matplotlib charts.
-   **History**: Tracks the last 5 uploads for quick access.
-   **Reporting**: Generates a PDF report for any analysis result.
-   **Authentication**: Token-based login system for secure access.
-   **UI Consistency**: Both platforms share a consistent "Scientific Flat" design with a focus on usability.

## Tech Stack

-   **Backend**: Python, Django, Django REST Framework
-   **Web**: React, Vite, Chart.js
-   **Desktop**: Python, PyQt5, Matplotlib
-   **Database**: SQLite

---

## Setup Instructions

### 1. Backend Setup (Django)

First, set up the backend server which powers both applications.

```bash
cd backend

# Create and activate virtual environment (Recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000`.

### 2. Web Application Setup (React)

Open a new terminal for the web frontend.

```bash
cd web-frontend

# Install node dependencies
npm install

# Start development server
npm run dev
```
Open `http://localhost:5173` in your browser.

### 3. Desktop Application Setup (PyQt5)

Open a new terminal for the desktop app.

```bash
cd desktop-app

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## Deployment Note

-   **Web App**: The frontend is configured to use `VITE_API_URL` from the `.env` file. For production (e.g., Vercel), set this variable to your live backend URL.
-   **Backend**: `settings.py` includes configuration for WhiteNoise to serve static files in production. Ensure `DEBUG = False` and `ALLOWED_HOSTS` are updated when deploying.
