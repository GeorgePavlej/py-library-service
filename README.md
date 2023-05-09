# Library Service
This project provides a RESTful API for managing library system in your city, by implementing an online management system for book borrowings. Also project focuses on developing an online management system for book borrowings to modernize the library's processes, improve user experience, and streamline administrative tasks.



## Installation
Python3 must be already installed
```shell
git clone https://github.com/GeorgePavlej/py-library-service.git
cd py-library-service
python -m venv venv
venv\Scripts\activate (Windows) or source venv/bin/activate (Linux or macOS)
pip install -r requirements.txt
copy .env.sample -> .env and populate with all required data
```

## Run migrations and server:

```shell
python manage.py migrate
python manage.py runserver
```
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

## API documentation

The API documentation is available at:
- api/doc/swagger/
