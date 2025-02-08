## Movie App Backend  

### Overview  
This is the backend for the Movie App, built using Django and Django REST Framework (DRF). It provides APIs for managing movies and user authentication. An admin panel is also included for CRUD operations.  

### Technologies Used  
<li>Django – Backend framework</li>  
<li>Django REST Framework (DRF) – API handling</li>  
<li>PostgreSQL – Database</li>  
<li>AWS – Deployment (future requirement)</li>  

### Setup Instructions  
#### Prerequisites  
<li>Python installed (>= 3.x)</li>  
<li>PostgreSQL installed and running</li>  
<li>Virtual environment set up</li>  

#### Installation
<ol>
    <li>Clone the repository:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
        git clone https://github.com/your-repo/movieapp-backend.git
        cd movieapp-backend
    </p>
    <li>Create a virtual environment and activate it:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
        python -m venv env
        source env/bin/activate  # macOS/Linux
        env\Scripts\activate.bat  # Windows
    </p>
    <li>Install dependencies:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
        pip install -r requirements.txt
    </p>
    <li>Configure the database: Update settings.py with PostgreSQL details:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
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
    </p>
    <li>Run migrations:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
        python manage.py makemigrations
        python manage.py migrate
    </p>
    <li>Create a superuser:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
        python manage.py createsuperuser
    </p>
    <li>Run the server:</li>
    <p style="width: 100%; background-color= black; padding: 3px 5px"}>
       python manage.py runserver
    </p>
</ol>  

### API Endpoints  
|Method|Endpoint|Description|
|------|--------|-----------|
|      |        |           |  

### Deployment on AWS (Planned)  
<li>The backend will be deployed using AWS services such as EC2 or Elastic Beanstalk.</li>  
<li>The database can be hosted on AWS RDS (PostgreSQL).</li>  

### Contribution  
<ol>
    <li>Fork the repository</li>  
    <li>Create a branch: git checkout -b feature-branch</li>
    <li>Make changes and commit: git commit -m 'Add feature'</li>
    <li>Push to GitHub: git push origin feature-branch</li>
    <li>Open a Pull Request</li>
<ol>
