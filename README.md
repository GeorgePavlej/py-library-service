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
copy .env.sample -> .env and populate with all required data
```

```shell
pip install -r requirements.txt
```

```shell
python manage.py migrate
```

```shell
python manage.py runserver
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

## Endpoints
Books Service:
Managing books amount (CRUD for Books)
API:
- POST: books/ - add new
- GET:  books/ - get a list of books
- GET:  books/id/- get book's detail info
- PUT/PATCH: books/id/ - update book
- DELETE: books/id/ - delete book

## Users Service:
Managing authentication & user registration
API:
- POST: users/ - register a new user
- POST: users/token/ - get JWT tokens
- POST: users/token/refresh/ - refresh JWT token
- GET:  users/me/ - get my profile info
- PUT/PATCH: users/me/ - update profile info

## Borrowings Service:
Managing users' borrowings of books
API:
- POST: borrowings/ - add new borrowing
- GET:  borrowings/  - get borrowings
- GET:  borrowings/id/ - get specific borrowing
- POST: borrowings/id/return/ - return borrowed book