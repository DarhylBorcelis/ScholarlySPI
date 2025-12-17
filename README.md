## Backend Setup (Django)

# 1. Create virtual environment

```bash
python -m venv venv              # required for first-time setup
```

# 2. Activate virtual environment

```bash
venv\Scripts\activate    
```

# 3. Install backend dependencies

```bash
pip install -r requirements.txt   # required for first-time setup
```

# 4. Run migrations

```bash
python manage.py migrate
```

# 5. Run Django server

```bash
python manage.py runserver
```