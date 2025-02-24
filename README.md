# AlphaBot Project

## Introduction
AlphaBot is an autonomous robotic system designed for remote control via a web-based interface. The project involves user authentication, a database-driven account creation system, and command execution through an interactive UI. This README details the technologies used, the authentication process, and the robot control mechanism.

---

## Project Overview
This project consists of a web-based interface built using Flask, which allows users to:
1. **Create an Account**: User registration that populates a database.
2. **Log in**: Authentication using hashed passwords and session management.
3. **Control the AlphaBot**: Send commands through a web interface using buttons.

The project leverages various technologies and libraries to achieve security, authentication, and communication with the AlphaBot.

---

## AlphaBot Theory
AlphaBot is a mobile robotic platform that integrates sensors, motors, and a microcontroller for autonomous or remote operation. The robot typically consists of:
- **Chassis & Motors**: Provides movement and navigation capabilities.
- **Sensors**: Includes cameras, ultrasonic sensors, and gyroscopes for environmental awareness.
- **Microcontroller/Processor**: Manages logic and processes user commands.
- **Communication Module**: Facilitates remote control via Wi-Fi or Bluetooth.

---

## Technologies Used
### Flask (Python Web Framework)
[Flask](https://flask.palletsprojects.com/) is a lightweight WSGI web framework used to develop the AlphaBot's web interface. It provides:
- Routing for handling HTTP requests.
- Session management to maintain user authentication.
- Integration with databases (SQLite, MySQL, or PostgreSQL).

### hashlib (Python Library)
[hashlib](https://docs.python.org/3/library/hashlib.html) is used for password hashing to enhance security. Instead of storing plain-text passwords, Flask uses hashing functions like SHA-256 to store securely hashed versions of user credentials.

### Cookies
Cookies are small pieces of data stored on the client-side to maintain user sessions. When a user logs in, a session cookie is generated to keep the user authenticated without requiring repeated logins.

### Tokens
Tokens (e.g., JWT - JSON Web Tokens) are used for secure authentication, especially in API-based systems. Unlike session cookies, tokens can be used for stateless authentication, allowing decentralized verification.

---

## Project Structure
```
/alphabot_project
│── /static
│   ├── styles.css
│   ├── alphabot_image.png  <-- Image of the AlphaBot
│── /templates
│   ├── index.html  <-- Main control interface
│   ├── login.html  <-- User login page
│   ├── register.html  <-- Account creation page
│── /database
│   ├── users.db  <-- SQLite database for storing user credentials
│── app.py  <-- Main Flask application
│── requirements.txt  <-- Dependencies
```

---

## Image Path
The image of the AlphaBot used in this project can be found at:

---

## Setup Instructions
### 1. Install Dependencies
```sh
pip install flask hashlib
```

### 2. Run the Flask Application
```sh
python app.py
```

### 3. Access the Web Interface
Open a browser and go to:
```
http://127.0.0.1:5000/
```

---

## Future Enhancements
- Implement WebSocket communication for real-time AlphaBot control.
- Add OAuth-based authentication.
- Enhance security with CSRF protection.

This project provides a foundation for secure and interactive AlphaBot control via a Flask-based web interface.

