# Library Service
This project provides a RESTful API for managing library system in your city, by implementing an online management system for book borrowings. Also project focuses on developing an online management system for book borrowings to modernize the library's processes, improve user experience, and streamline administrative tasks.


## Prerequisites
- Python 3 must be already installed
- Docker and Docker Compose installed on your system
- Postgres DB

## Installation

```shell
git clone https://github.com/GeorgePavlej/py-library-service.git
```

```shell
python -m venv venv
```
```shell
venv\Scripts\activate (Windows)
```
```shell
source venv/bin/activate (Linux or macOS)
```

```shell
copy .env.sample -> .env and populate with all required data
```

```shell
pip install -r requirements.txt
```

## Run docker to start the development server and other required services:

```shell
docker-compose up --build
```

## Test User credentials are:
    Email: testuser@example.com
    Password: testpassword123

## API documentation

The API documentation is available at:
- api/doc/swagger/

## Getting access
<hr>

- Create user via /api/user/register/
- Get access token via /api/user/token/

## Features
<hr>

- JWT authenticated;
- Users authentication & registration
- Managing users borrowings of books
- Telegram notifications for borrowing events
- Stripe payments integration for book borrowings
