# Jiseti

Jiseti is a civic-tech platform built to fight corruption and promote transparency across Africa. It empowers citizens to anonymously report corrupt practices and highlight areas needing government action. By bridging the gap between the public and oversight institutions, Jiseti aims to drive accountability and inspire positive change.

# Jiseti Backend

This repository contains the backend of the Jiseti platform, built with Flask and PostgreSQL, following RESTful API principles. It serves as the core engine that handles data processing, user management, record reporting, and secure authentication.

---

## Features

- RESTful API architecture using Flask
- Secure user authentication and authorization
- Role-based access control (Admin & User)
- Record CRUD operations (Create, Read, Update, Delete)
- PostgreSQL database integration with SQLAlchemy ORM
- Input validation and error handling
- CORS support for frontend-backend communication
- JSON responses for frontend consumption

---

## Tech Stack

- Flask (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Flask-CORS, Flask-Migrate, Flask-JWT-Extended
- Alembic (Database migrations)

---
## Project Structure (Important Files/Folders)

Jiseti-Backend/
├── app.py # Entry point
├── models.py # Database models
├── routes/ # API routes and views
├── migrations/ # Alembic migrations
└── README.md 

---

## Installation & Setup

## Prerequisites

- Python 3.8+
- PostgreSQL
- pipenv or virtualenv

### Step-by-Step Setup
# 1. Clone the repo
git clone https://github.com/JamesNyamweya/Jiseti-Backend
cd Jiseti-backend

# 2. Create virtual environment and activate
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 5. Run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 6. Run the app
flask run

 ## API Endpoints
 Auth
Method	Endpoint	Description
POST	/signup	Register a new user
POST	/login	Login and receive JWT

### Records (Red-Flags & Interventions)
Method	Endpoint	Description
GET	/records	Get all records
POST	/records	Create a new record
GET	/records/<id>	Get a specific record by ID
PATCH	/records/<id>	Update a record (by owner/admin)
DELETE	/records/<id>	Delete a record (admin/owner only)


## Error Handling
The API returns standard error responses:
{
  "error": "Unauthorized access",
  "code": 401
}
Status Code	Meaning
200	OK
201	Created
400	Bad Request
401	Unauthorized
403	Forbidden
404	Not Found
500	Server Error

## Authors

**Jiseti** was collaboratively built by:

1. **Irene Peter**
2. **Rahma Mohammed**
3. **Collins Kiprono**
4. **Jerald Nyaga**
5. **James Nyamweya**

**We welcome contributions!** To contribute:
Fork this repo
Create a new branch
Make your changes
Submit a pull request

## License
This project is licensed under the MIT License. See LICENSE for more details.

## Support
For help, questions, or bug reports, Contact any of the contributors above.

## Link
https://jiseti-frontend-kgib.onrender.com/

## Presentation Slides
https://docs.google.com/presentation/d/1JcYFthWx5LZyZhVCvytpqHiQ6DwlA8Rq/edit?usp=sharing&ouid=112882931007072286996&rtpof=true&sd=true