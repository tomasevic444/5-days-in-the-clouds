# **Levi9 Competition: 5 Days in the Cloud - Hackaton entry project*

This project is designed for the **Levi9 Competition** in the **5 Days in the Cloud** event. The application is built using **Python**, **FastAPI**, and **TinyDB** as an in-memory database for simulating a team and player management system. It allows you to manage players, teams, and match results with **ELO** ranking calculations and more.

## **Technologies Used**

- **Python**: The core programming language used to build the application.
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **TinyDB**: A lightweight, document-oriented database that is used in this project as an in-memory storage solution for teams, players, and matches.

## **Project Setup**

Follow these steps to get started with the project.

### **1. Clone the repository**

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### **2. Install Dependencies**


Install all the required dependencies using pip and the requirements.txt file:

```bash
pip install -r requirements.txt
```
This will install FastAPI, TinyDB, Uvicorn, and other necessary packages for running the project.

### **3. Run the Application**
To start the FastAPI application, run the following command:

```bash
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```
Once the application is running, you can interact with the API in the following way:
- **Postman**: Use Postman to test endpoints manually. Add requests with the base URL http://127.0.0.1:8080 and the desired endpoint paths.

### **4. Unit Tests**
The project includes unit tests to verify the functionality of your endpoints and logic.

To run the tests, use pytest:

```bash
pytest
```
This will run all the unit tests and show the results in your terminal. You can add -v for a more detailed output:



### **Project Structure**
Here’s an overview of the project structure:

```bash
.
├── app/
│   ├── controllers/      # API routers for handling requests
│   │   ├── __init__.py
│   │   ├── match_controller.py
│   │   ├── players_controller.py
│   │   └── teams_controller.py
│   ├── models/           # Models
│   │   ├── __init__.py
│   │   ├── match.py
│   │   ├── player.py
│   │   └── team.py
│   ├── services/         #  Logic for handling data
│   │   ├── __init__.py
│   │   ├── match_service.py
│   │   ├── player_service.py
│   │   └── team_service.py
│   └── __init__.py
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_match_service.py
│   ├── test_players_service.py
│   └── test_team_service.py
├── .gitignore            # Ignored files for Git
├── main.py               # Entry point for the FastAPI application
├── README.md             # Project documentation
└── requirements.txt 
```
