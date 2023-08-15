# Database Migration With Alembic & FastAPI
To properly run this project, please do the following:

- Create a virtual environment and install the requirements - "requirements\requirements.txt"
- Generate migration script and run migration to create database tables - *alembic files provided*
  - To create a migration file: `$alembic revision --autogenerate -m "some_comment"`. *NOTE: Properly update the following files with your database URL and credentials: `settings.py`, `alembic.ini`, and `.env`*
  - To update database with migration file: `$alembic upgrade head`
- Run the FastAPI application: `$python ./app/run.py`
