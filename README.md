# Fake CSV generator

An application for generating CSV files with fake data.


## Description

- User can create any number of data schemas to create datasets with fake data.
- Each such data schema has a name and the list of columns with names and specified data types.
- Users can build the data schema with any number of columns.
- After creating the schema the user can input the number of records he/she needs to generate.
- After generating process the result is saved in the file and user can download datasets.

## Requirements

- Python 3.8+
- Docker
- Redis
- Cloudinary

## Installing and usage

1. Clone the repository
```
git clone git@github.com:AnnaKatunina/FakeCSV_generator.git
```

2. Create .env file in root directory with variables: 

- For Django project: SECRET_KEY
- For DB: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, DB_HOST, DB_PORT
- For Redis: REDIS_TLS_URL, REDIS_URL
- For Cloudinary: CLOUD_NAME, API_KEY, API_SECRET

3. Build a docker container
```
docker-compose up --build
```

4. Migrate all migrations to postgres database
```
docker exec -it web python manage.py migrate
```

5. Create superuser to gain access to the application
```
docker exec -it web python manage.py createsuperuser
```

6. Then, navigate to http://localhost:8000/ to sign in and view the web application.
