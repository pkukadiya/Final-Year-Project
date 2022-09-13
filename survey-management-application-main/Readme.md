# Installation
First activate a virtual enviornment 
TO download virtual enviornment:
```
pip install virtualenv
python -m venv virtualenvname
```
To activate in windows:
```
./virtualenvname/Scripts/activate
```
Note: might see error scripts not allowed contact me if it comes
<br>
To activate in linux:
```
source virtualenvname/bin/activate
```
<br>
then run following command 

```
cd survey_management_project
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

To run server:
```
python manage.py runserver
```

To create a superuser:
```
python manage.py createsuperuser
```

To collect all static files:
```
python manage.py collectstatic
```
```

Django ORM link : 127.0.0.1:8000/admin/ <br>
Go to following address to access server : http://127.0.0.1:8000/
