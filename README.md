# Setting up the environment

## 1. Install Python

```bash
sudo apt update && apt upgrade -y

Use Python 3.13.2
```

## 2. install all dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

## 3. Make migrations

This is to create the database schema. Migrate will apply the changes to the database.

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Create a superuser

This is to access the admin panel

```bash
python manage.py createsuperuser
```

## 5. Create a .env file

This is to store the environment variables

```bash
cp .env_example .env
```
## 7. Load the data

```bash
python manage.py backup_db
```

## 8. Run the server

Server will be running on http://localhost:8000 with the following command

```bash
python manage.py runserver 0.0.0.0:8000
```

```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile - flora_admin.wsgi:application
```

## 9. Create a model based on the previous database

```bash
python manage.py inspectdb > [APP_NAME]/models.py
```

## 10. Create a backup of the database without the Django models can conflict

```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions --exclude admin --output dump_flora_[DATE].JSON
```

## 11. Dump a specific table in the database and load its data (if it's necessary)

```bash
python manage.py dumpdata myapp.Familia

python manage.py loaddata myapp.json --include='myapp.Familia'
```

## 12. Load data from JSON to database
```bash
python manage.py loaddata data.json
```
