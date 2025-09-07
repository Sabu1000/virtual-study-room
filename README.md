# Virtual Study Room

## Project Overview
The Virtual Study Room is a web application designed to facilitate collaborative learning. It allows users to create and join virtual study rooms, chat in real-time, and manage their profiles. This project is built using Flask, a lightweight Python web framework, and includes features like user authentication, real-time chat, and study room management.

---

## Features
- **User Authentication**: Secure login and registration system.
- **Profile Management**: Users can upload profile pictures and update their information.
- **Study Rooms**: Create, edit, and manage virtual study rooms.
- **Real-Time Chat**: Communicate with other users in real-time using WebSockets.
- **Password Reset**: Email-based password reset functionality.
- **Responsive Design**: User-friendly interface with responsive templates.

---

## Project Structure
```
virtual-study-room/
├── app/
│   ├── auth/                # Handles user authentication
│   ├── main/                # Main application routes
│   ├── studyroom/           # Study room-related features
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS, JS, images)
│   ├── extensions.py        # Flask extensions initialization
│   ├── models.py            # Database models
│   ├── sockets.py           # WebSocket logic
│   └── __init__.py          # Application factory
├── instance/
│   └── site.db              # SQLite database
├── migrations/              # Database migrations
├── utils/
│   └── token.py             # Token generation utilities
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation
```

---

## Installation

### Prerequisites
- Python 3.10 or higher
- A virtual environment tool (e.g., `venv`)

### Steps
1. **Clone the Repository**:
   ```powershell
   git clone https://github.com/Sabu1000/virtual-study-room.git
   cd virtual-study-room
   ```

2. **Set Up a Virtual Environment**:
   ```powershell
   python -m venv venv
   & .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   ```powershell
   flask db upgrade
   ```

5. **Run the Application**:
   ```powershell
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000/`.

---

## Usage

### Environment Configuration
- The `config.py` file manages environment-specific settings.
- Use environment variables to switch between development and production modes.

### Running Tests
- Tests can be added using `unittest` or `pytest`.
- Run tests with:
  ```powershell
  python -m unittest discover
  ```

### Deployment
- For production, use a WSGI server like Gunicorn.
- Example deployment command:
  ```powershell
  gunicorn -w 4 -b 0.0.0.0:5000 run:app
  ```

---

## Key Features Explained

### Real-Time Chat
- Implemented using Flask-SocketIO.
- Enables WebSocket communication for real-time messaging.

### Authentication
- Uses Flask-Login for session management.
- Passwords are hashed using `bcrypt` for security.

### File Uploads
- Profile pictures are stored in `static/profile_pics/`.
- File names are managed to avoid conflicts.

---

## Future Improvements
- Add video conferencing to study rooms.
- Implement notifications for chat messages.
- Optimize database queries for better performance.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For any questions or feedback, please contact the repository owner at [GitHub](https://github.com/Sabu1000).
