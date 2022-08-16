# ESTL-Tech-Assessment

# Instructions

## Clone repo

```
git clone https://github.com/zainul1996/ESTL-tech-assessment.git
```

## Setup database

```
Setup Postgres DB and create tables
docker build -t my-postgres-db ./
docker run -d --name my-postgresdb-container -p 5432:5432 my-postgres-db

Setup pgadmin4
docker pull dpage/pgadmin4
docker run --name my-pgadmin -p 82:80 -e 'PGADMIN_DEFAULT_EMAIL=pgadmin@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=postgresmaster' -d
dpage/pgadmin4

Visit localhost:82 on your browser and login with:
username: pgadmin@gmail.com
password: postgresmaster

Right click "Server" > Click "Register" > "Server"
Under the General Tab:
Name: postgres_db

Under the connection tab:
Hostname/Address: {Enter the IP of the Container running postgres}
Port: 5432
Username: postgres
Password: postgres

To find out the IP of the Container running postgres, use the below command:
docker inspect my-postgresdb-container -f "{{json .NetworkSettings.Networks}}"
```

## Install requirements file

```
cd public
pip install -r requirements.txt
```

## DB Credentials

Input DB credentials in public > app > controller > main.py

## Start Application

```
flask run
```
