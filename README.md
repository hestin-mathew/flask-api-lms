# Library Management System

This project is a simple Library Management System built using Python. It includes a web-based interface for managing books, users, and transactions, backed by a SQLite database.

## Features
- Manage books and their details.
- Track library users.
- Handle book lending and return transactions.
- User-friendly web interface.

## Project Structure
library/ 
├── app.py # Main application script 
├── library.db # SQLite database file 
├── static/ # Static assets (CSS, JS, images) 
├── templates/ # HTML templates for the UI 
├── tests.py # Unit tests for the application 
├── venv/ # Python virtual environment 
└── pycache/ # Compiled Python files


## Prerequisites
- Python 3.8 or higher
- Virtual environment (`venv`)

## Setup Instructions

1. **Clone the Repository**:
   git clone https://github.com/hestin-mathew/flask-api-lms

2. Set Up the Virtual Environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Run the Application:
pyhton app.py
