# Library Service
This project provides a RESTful API for managing library system in your city, by implementing an online management system for book borrowings. Also project focuses on developing an online management system for book borrowings to modernize the library's processes, improve user experience, and streamline administrative tasks.



## Installation
Python3 must be already installed
```shell
git clone https://github.com/GeorgePavlej/py-library-service.git
```
```shell
cd py-library-service
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
pip install -r requirements.txt
```
```shell
copy .env.sample -> .env and populate with all required data
```

## Run migrations and server:

```shell
python manage.py migrate
```

```shell
python manage.py runserver
```

## Test User
- To create a test user, run the following command:

```shell
python manage.py create_test_user
```

The test user credentials are:

    Email: testuser@example.com
    Password: testpassword123

## Loading Fixture Data
- To load the fixture data into your database, run the following command:

```shell
python manage.py loaddata fixtures/initial_data.json

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
