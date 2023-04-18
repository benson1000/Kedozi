# KEDOZI Real Estate company
---
- This project is for Kedozi Real Estate. Kedozi builds and sells houses in major cities, counties and Towns in the country. Kedozi builds houses according to the customers requirements and at an affordable rate. The houses are for all the income classes.

### Modules used

---
| Module Name    | Usage in Application |
|----------------|----------------------|
|Flask           |Web Framework to create Application|
|Flask-Login     | User Session Management in Flask|
|Flask-SQLAlchemy|Adding support of SQLAlchemy into application|
|Flask-WTF       | provide the interactive user interface for the user |
|psycopg2        |This is for connecting the code with the POSTGRESQL database |
|Bcrypt          | For hashing and checking password|
|WTForms         |flexible forms validation and rendering|



### Installation
---
- Install all the dependancies using requirements.txt file...
- ```pip install requirements.txt```


### Running

---
##### Setup on Windows
- setting flask application in Windows
- ```set FLASK_APP=app.py```
- ```set FLASK_DEBUG=1```

##### Setup on Unix
- setting flask application in Unix
- ```export FLASK_APP=app.py```
- ```export FLASK_DEBUG=1```



#### Run Application
- After setting flask application, To run application use below command
- ```flask run --port=5000```
- ```--port``` is optional