# To-do-list


This project is a task planner.
It gives you the following opportunities:

- create new tasks;
- add tags to the tasks;
- monitor task status (whether it is done or not);


## How to run the project >>>

1. Run the command below in your terminal
    - `git@github.com:MarharytaSovpenko/To-do-list.git`
2. Open the project folder in your IDE
3. If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements
   in it, but if not:
    - python -m venv venv
    - source venv/Scripts/activate (on Windows/Git Bash)
    - venv\Scripts\activate (on Windows/PowerShell)
    - source venv/bin/activate (on macOS)
    - pip install -r requirements.txt
4. Don't forget to do migrations
    - `python manage.py migrate`
5. Run your server using the command below
    - `python manage.py runserver`

In this project you should also use environment variables. Create .env file and fill it with variables from .env.sample.