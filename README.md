# Python Final Project MFT

# 🌱 Saba Data Entry Application

<p align="center">
  <img src="" alt="" width="850">
</p>

<p align="center">
  <b>A clean desktop data entry app built with Python, Tkinter, and MVC architecture</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Tkinter-GUI-orange">
  <img src="https://img.shields.io/badge/Architecture-MVC-success">
  <img src="https://img.shields.io/badge/Storage-CSV-lightgrey">
  <img src="https://img.shields.io/badge/Status-In%20Progress-yellow">
</p>

---

## 🚧 Project Status

# 🔥 THIS PROJECT IS STILL UNDER DEVELOPMENT 🔥

The application is working, but the project is **not finished yet**.

More improvements are still coming, including:

- better authentication
- cleaner UI
- stronger validation
- improved data handling
- more user-friendly behavior
- future packaging and deployment

---

## ✨ About the Project

**Saba Data Entry Application** is a desktop app made for structured data collection.

It helps users enter records in a neat and organized form instead of dealing directly with raw CSV files.

The app includes:

- a login dialog
- a main data-entry window
- automatic validation
- red error messages
- settings persistence
- CSV export
- menu actions
- clean MVC-based structure

This project was built as a final Python project using:

- **Python**
- **Tkinter**
- **Object-Oriented Programming**
- **MVC design**
- **CSV files**
- **JSON settings**
- **custom widget validation**

---

## 🖼️ Application Screenshots

### 🔐 Login Window
The app starts with a simple login screen.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f86c69d2-1fe2-4554-9028-06b8f390c16b" alt="Login Window" width="300"/>

</p>

---

### 📝 Main Form
The main form is divided into sections:

- Record Information
- Environment Data
- Plant Data
- Notes

<p align="center">
  <img src="https://github.com/user-attachments/assets/8c88d3ad-72b2-4004-862e-b4e51e83ac6f" alt="Main Form" width="600"/>

</p>

---

### ❌ Validation Errors
Invalid or empty fields are shown in **red**.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4082f838-12b9-4f98-8d69-1164ef1491a6" alt="Validation Errors" width="600"/>

</p>

---

### 📁 File Menu
The File menu lets you choose the output CSV file or quit the app.

<p align="center">
 
</p>

---

### ⚙️ Options Menu
The Options menu includes settings such as autofill date and autofill sheet data.

<p align="center">

</p>

---

### 💾 Save Record
After validation passes, the record is saved to CSV.

<p align="center">
  <img  src="https://github.com/user-attachments/assets/e78935a2-169f-4012-abcf-ceeeca764531" alt="Save Record" width="800"/>

</p>

---

### 🛠️ Project Progress
This screenshot shows the development progress of the project.

<p align="center">
  <img src="docs/screenshots/07-project-progress.png" alt="Project Progress" width="800">
</p>

---

## 🧩 Features

### ✅ User Login
A login dialog appears before the main app opens.

### ✅ Form-Based Data Entry
The UI is split into logical sections for easier data input.

### ✅ Validation System
The app checks:

- required fields
- valid dates
- numeric ranges
- combobox values
- field relationships

### ✅ Red Error Messages
Validation errors appear below fields in red.

### ✅ Autofill Date
The current date can be inserted automatically.

### ✅ Autofill Sheet Data
Repeated sheet values can be preserved for faster entry.

### ✅ Save to CSV
Validated records are written into a CSV file.

### ✅ Persistent Settings
Settings are stored and loaded through a JSON file.

---

## 🏗️ MVC Structure

This project follows an MVC-style structure:
```text
User
  ↓
View
  ↓
Application Controller
  ↓
Model

