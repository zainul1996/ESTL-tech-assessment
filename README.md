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

## Tasks

USER STORY 1: Upload Users (Prioritized)
[x] Successful uploading our good test data file with comments, both new and existing records.
[x] Unsuccessful upload of an empty file.
[x] Unsuccessful upload of files with partial number of incorrect number of columns (both too many and too few).
[x] Unsuccessful upload of files with some but not all rows with incorrectly formatted salaries.
[x] Unsuccessful upload of files with some but not all rows with salary < 0.0.
[x] Upload 2 files concurrently and receive expected results, or failure.

USER STORY 2: Employee Dashboard Feature (Prioritized)
[x] When I click on the next page, it should be able to display records, with no overlapping records in page 1 and page 2
[x] When performing a search for min salary of 0 and max salary of 4000, it should only return records with salary between 0 <= salary <= 4000
[x] When sorting by name in ascending order, it should display in ascending order by name
[x] When sorting by salary in ascending order, it should display in ascending order by salary
[x] When sorting by login descending order, it should display in descending order by login

USER STORY 3: CRUD Feature (Bonus)
[x] When I resize my web browser into phone form, the layout should be automatically changed to the appropriate form factor layout.
[x] When I click on the edit function on an employee on USER story #2, I should be able to edit the employee details on the user interface
[x] When I click on the save button, the modification should persist on the backend. At the employee dashboard page, you should be able to see the modified information
[x] When I click on the delete button, a confirmation prompt should ask me if I really want to delete this employee.
[x] When confirmed, the deletion should persist on the backend
[x] At the employee dashboard page, you should not be able to see this employee.

USER STORY 4: Better UX When Uploading Large CSV Files (Bonus)
[] I want to be able to upload a good file with 5000 entries with success.
[] I want to be able to start two concurrent uploads of files with 5000 entries in two different tabs and check that I obtain proper feedback.

USER STORY 5: UI Localization (Bonus)
[] If I change my desktop environment’s language to Chinese, I should be viewing it in English still because there are no Chinese translations. I would like to be able to get indicators that it acknowledges that the language is to be in Chinese but Chinese is not available.

# Images

Dashboard

[Desktop]
<img src="https://cdn.discordapp.com/attachments/933291645733072926/1009093480435433564/unknown.png" alt="ESTL-Tech-Assessment" width="100%" height="auto">

[Mobile]
<img src="https://cdn.discordapp.com/attachments/933291645733072926/1009093542188159006/unknown.png" alt="ESTL-Tech-Assessment" width="100%" height="auto">

[Sort/Filter]
<img src="https://cdn.discordapp.com/attachments/933291645733072926/1009093752993882122/unknown.png" alt="ESTL-Tech-Assessment" width="100%" height="auto">

[Update/Delete]
<img src="https://cdn.discordapp.com/attachments/933291645733072926/1009093785503928340/unknown.png" alt="ESTL-Tech-Assessment" width="100%" height="auto">

Upload Page
<img src="https://cdn.discordapp.com/attachments/933291645733072926/1009093480435433564/unknown.png" alt="ESTL-Tech-Assessment" width="100%" height="auto">
