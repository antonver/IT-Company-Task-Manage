# IT-Company-Task-Manage

The IT Company Task Manager is a task management system designed to organize workflow in an IT company. The system allows you to create, track, and manage tasks, projects, and employee teams.

## Features

- **Tasks**
  - Create and edit tasks with title, description, deadline, and priority.
  - Assign tasks to different task types.
  - Assign employees to tasks.
  - Link tasks to projects.

- **Task Types**
  - Manage different categories or types of tasks.

- **Projects**
  - Create projects with participants and deadlines.
  - Associate projects with teams.

- **Teams**
  - Manage teams and assign team leads.
  - Add team slogans.

- **Workers**
  - Create users with positions and team assignments.
  - Manage employee profiles.
  - Assign workers to projects and tasks.

- **Positions**
  - Manage employee roles or job titles.


## Installation and Setup

### Requirements
- requierements.txt

### Installation Steps
1. Clone the repository:
   ```bash
    git clone https://github.com/antonver/IT-Company-Task-Manage.git
    cd IT-Company-Task-Manage cd IT-Company-Task-Manage
# Set Up for Unix, MacOS:


```
    $ virtualenv env
    $ source env/bin/activate
    $ pip3 install -r requirements.txt
```

Set up Database:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Start the app:
 ```
$ python manage.py runserver
```
# Set Up for Windows: 
```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```
Set Up Database
```
$ python manage.py makemigrations
$ python manage.py migrate
```

Start the app
```
$ python manage.py runserver
```

# Structure:
![Диаграмма без названия drawio](https://github.com/user-attachments/assets/207eb4fe-84fa-4e7b-b91e-52b64ecd3dd6)


  



