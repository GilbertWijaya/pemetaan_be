# Backend API Project

A modern Flask application with layered architecture (Models, Repositories, Services, and API endpoints).

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes & blueprints
│   ├── middlewares/      # Custom middlewares
│   ├── models/           # Database models
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic layer
│   ├── utils/            # Utility functions
│   ├── __init__.py       # Flask app factory
│   ├── config.py         # Configuration settings
│   └── extension.py      # Flask extensions
├── migrations/           # Database migrations (Alembic)
├── test/                 # Test files
├── .env                  # Environment variables
├── requirement.txt       # Python dependencies
├── run.py               # Application entry point
└── readme.md            # This file
```

## Architecture Layers

### 1. **Models Layer** (`app/models/`)
- Database model definitions
- Uses SQLAlchemy ORM
- Inherits from `BaseModel` with timestamps

### 2. **Repositories Layer** (`app/repositories/`)
- Data access abstraction
- CRUD operations
- Database queries logic
- Extends `BaseRepository`

### 3. **Services Layer** (`app/services/`)
- Business logic implementation
- Data processing
- Validation logic
- Uses repositories for data access

### 4. **API Layer** (`app/api/`)
- Flask blueprints
- Route handlers
- Request/response handling
- Uses services for business logic

### 5. **Utilities** (`app/utils/`)
- Helper functions
- Decorators
- Common utilities

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirement.txt
```

### 3. Configure Environment Variables
Copy `.env` and update with your settings:
```bash
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Initialize Database
```bash
# Create database first in PostgreSQL
createdb your_db_name

# Run migrations
flask db upgrade
# Or initialize from scratch
flask init-db
```

### 5. Run the Application
```bash
python run.py
# Or using Flask CLI
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check if API is running

## Development Commands

### Flask Shell
```bash
flask shell
```

### Database Commands
```bash
# Initialize database
flask init-db

# Drop database
flask drop-db

# Create migration
flask db migrate -m "description"

# Apply migration
flask db upgrade
```

## Creating New Features

### Example: Create a User Model

1. **Create Model** (`app/models/user.py`):
```python
from app.models.base_model import BaseModel
from app.extension import db

class User(BaseModel):
    __tablename__ = 'users'
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'name': self.name,
            'email': self.email,
        })
        return data
```

2. **Create Repository** (`app/repositories/user_repository.py`):
```python
from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def find_by_email(self, email):
        return self.find_one_by(email=email)
```

3. **Create Service** (`app/services/user_service.py`):
```python
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def get_user(self, user_id):
        return self.user_repo.find_by_id(user_id)
    
    def create_user(self, name, email):
        return self.user_repo.create(name=name, email=email)
```

4. **Create API Route** (`app/api/users.py`):
```python
from flask import Blueprint, request
from app.services.user_service import UserService
from app.utils.helpers import success_response, error_response

users_bp = Blueprint('users', __name__, url_prefix='/users')
user_service = UserService()

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return error_response('User not found', 404)
    return success_response(user.to_dict())
```

5. **Register Blueprint** in `app/__init__.py`:
```python
def register_blueprints(app):
    from app.api.users import users_bp
    api_bp.register_blueprint(users_bp)
```

## Testing

Create test files in the `test/` directory:
```bash
python -m pytest test/
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_APP` | Flask app entry point | run.py |
| `FLASK_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Secret key for sessions | dev-key-change-this |
| `DB_HOST` | Database host | localhost |
| `DB_PORT` | Database port | 5432 |
| `DB_NAME` | Database name | dev_db |
| `DB_USER` | Database user | postgres |
| `DB_PASSWORD` | Database password | password |
| `CORS_ORIGINS` | CORS allowed origins | * |
| `DEBUG` | Debug mode | True |

## Common Issues

### ImportError when running the app
- Make sure all imports use relative imports within the `app` package
- Check that `__init__.py` files exist in all directories

### Database connection error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### Port already in use
- Change port in `run.py`: `app.run(port=5001)`
- Or kill the process using port 5000

## Dependencies

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - CORS support
- **python-dotenv** - Environment variables
- **psycopg2-binary** - PostgreSQL adapter

## License

MIT

## Author

Your Name
