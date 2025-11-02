# Bank Account Management System

A simple CLI-based bank account management system built with Python that handles user registration and login with secure password storage.

## Features

- User Registration with validation:
  - First name and last name validation
  - Phone number validation (7-15 digits)
  - Email validation and uniqueness check
  - Strong password requirements:
    - Minimum 8 characters
    - Must include lowercase and uppercase letters
    - Must include at least one digit
    - Must include special characters
  - Password confirmation check
  - Secure password hashing using SHA-256

- User Login:
  - Email-based authentication
  - Secure password verification

## Data Storage

User data is stored in `users.txt` as JSON lines format. Each line contains one user record with the following structure:

```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890",
  "password": "<hashed_password>",
  "created_at": "2025-11-02T12:34:56Z"
}
```

## How to Run

1. Make sure you have Python 3.6+ installed
2. Navigate to the project directory
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Registration
1. Choose option `1` for registration
2. Follow the prompts to enter:
   - First name
   - Last name
   - Phone number (7-15 digits)
   - Email address (must be unique)
   - Password (must meet strength requirements)
   - Confirm password

### Login
1. Choose option `2` for login
2. Enter your registered email
3. Enter your password

### Exit
- Choose option `3` to exit the application

## Security Features

- Passwords are hashed using SHA-256 before storage
- Input validation for all fields
- Email uniqueness check
- Strong password requirements
- Password confirmation during registration

## File Structure

```
Bank-Project-Paython/
├── main.py          # Main application code
├── users.txt        # User data storage (JSON lines)
└── README.md        # Project documentation
```