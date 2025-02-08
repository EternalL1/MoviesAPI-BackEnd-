## Movie App Backend

### Overview
This is the backend for the Movie App, built using Django and Django REST Framework (DRF). It provides APIs for managing movies and user authentication. An admin panel is also included for CRUD operations.

### Technologies Used
- Django – Backend framework
- Django REST Framework (DRF) – API handling
- PostgreSQL – Database
- AWS – Deployment (future requirement)

### Setup Instructions

#### Prerequisites
- Python installed (>= 3.x)
- PostgreSQL installed and running
- Virtual environment set up

#### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/movieapp-backend.git
    cd movieapp-backend
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # macOS/Linux
    env\Scripts\activate.bat  # Windows
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Configure the database: Update `settings.py` with PostgreSQL details:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'yourpassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
5. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
7. Run the server:
    ```bash
    python manage.py runserver
    ```

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
|        |          |             |

### Deployment on AWS (Planned)
- The backend will be deployed using AWS services such as EC2 or Elastic Beanstalk.
- The database can be hosted on AWS RDS (PostgreSQL).

### Contribution
1. Fork the repository
2. Create a branch: `git checkout -b feature-branch`
3. Make changes and commit: `git commit -m 'Add feature'`
4. Push to GitHub: `git push origin feature-branch`
5. Open a Pull Request
  
### License  
This project is licensed under the MIT License.