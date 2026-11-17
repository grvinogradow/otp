
# OTP
### An one-time token authentication system designed for integration into Python applications.

## Features

- Modular architecture
- One-time login tokens with expiration
- Asynchronous database for tokens
- Cookie-based sessions
- Login and logout endpoints

## Tech Stack

- Python
- FastAPI
- SQLite via aiosqlite

## Getting Started

1. Clone the repository and install the requirements

```bash
git clone https://github.com/grvinogradow/otp.git
cd otp
pip install -r requirements.txt
```

2. Create a `.env` file in the project root

```env
SECRET=your-random-secret-key
```

3. Start the Application
```bash
python main.py
```

Optional command-line arguments:

```bash
python main.py [--host HOST] [--port PORT] [--debug]
```

In debug mode, the application creates sample users and makes unique tokens for them.

Open `http://127.0.0.1:8000/login?token=YOUR_TOKEN` to authenticate.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Authenticated user's profile |
| GET | `/login?token=...` | Authenticates using a one-time token |
| GET | `/logout` | Clears the current session |

## Project Structure

```text
otp/
├── main.py
├── web.py
├── modules/
│   ├── tokens.py
│   └── users.py
├── database/
│   ├── database.py
│   └── modules/
│       └── tokens.py
└── requirements.txt
```

## License

Licensed under the Apache License 2.0.
