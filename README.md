# Apk-Automation

Apk-Automation is a Django-based web application designed for run APK files and automating mobile application testing. It offers user registration, app management, and detailed UI hierarchy views.

## Features

- **User Registration and Login:** Secure user registration and authentication.
- **View and Update User Information:** Access and modify user Info.
- **Add New Apps:** Upload and manage new APK files.
- **View UI Hierarchy:** Analyze and view the UI hierarchy of added apps.
- **Update App Details:** Edit app details and information.
- **Delete Apps:** Remove apps from the system.
- **Database:** Added instructions for configuring MySQL as the database with name apk_manager

## Getting Started
Make sure that you 
### Installation

1. **Create VENV:**
   ```bash
   python -m venv apk_manager_venv
   for linux: source venv/bin/activate 
   for windows: .\apk_manager_venv\Scripts\activate
   cd apk_manager_venv

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/BeshoiBotros/Apk-Automation.git
   cd Apk-Automation


3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Apply Migrations:**
   ```bash
   python manage.py migrate

5. **Collecting Static Files:**
   ```bash
   python manage.py collectstatic

6. **Run the Server:**
   ```bash
   python manage.py runserver

