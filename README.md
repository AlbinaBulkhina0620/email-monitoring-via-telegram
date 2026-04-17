# Secure Email Log Monitoring and Alerting System with Telegram Integration.

This project is a system that reads log messages from a user’s email and forwards important ones to Telegram. The goal is to make it easier to monitor important events in real time without constantly checking email.


## System Architecture
### 1. User mail
- Source of incoming log messages
### 2. Email reader
- Authenticates using OAuth2 or App Password
- Uses secure IMAPS connection
- Has read-only access to the mailbox
### 3. Filtering
- Checks sender against a list of trusted sources
- Ignores all other emails
- Other filters will be added in the MVP2 (keyword-based filtering)
### 4. Telegram Alert Service
- Sends alerts via Telegram Bot API
- Only authorized users receive messages


## We aim to focus on security in this project, therefore we deploy:
- Encrypted communication (IMAPS, HTTPS)
- Read-only access to email (no modification or sending)
- Credentials stored in environment variables (.env)
- Telegram access restricted to specific user ID


## Tech Stack:
- Python – core logic:
    - imaplib – secure email access (IMAPS)
    - python-telegram-bot – Telegram integration
    - python-dotenv – environment variable
- Docker & Docker Compose – containerization
- PostgreSQL – store emails
