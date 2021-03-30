# Capstone

Capstone project FSND provided by Udicity

## Hosted on heroku.


Link](https://movieagencies.herokuapp.com).

## Working with the application locally
Make sure you have [python 3](https://www.python.org/downloads/) or later installed

1. **Clone The Repo**
    ```bash
    git clone https://github.com/Haddadmj/FSND_Capstone_Casting_Agency
    ```
2. **Set up a virtual environment**:
    ```bash
    virtualenv env
    source env/Scripts/activate # for Windows
    source env/bin/activate # for MacOs/Linux
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt # for Windows/Linux
    pip3 install -r requirements.txt # for MacOs
    ```
4. **Export Environment Variables**

    Refer to the `setup.sh` file and export the environment variables for the project.

5. **Create Local Database**:

    Create a local database and export the database URI as an environment variable with the key `DATABASE_URL`.

6. **Run Database Migrations**:
    ```bash
    python3 manage.py db init
    python3 manage.py db migrate
    python3 manage.py db upgrade
    ```

7. **Run the Flask Application locally**:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run

    # if using CMD in Windows

    set FLASK_APP=app.py
    set FLASK_ENV=development
    flask run
    ```

## Dependencies

Use this command " pip3 install -r requirements.txt "

## Authentication

The API has three users :

Assistant


Credentials:
```
Email: boob.75@hotmail.com
Password: A1b2c3d4
```


Roles:
```
a- Get actors
b- Get movies
```

Director


Credentials:
```
Email: zainab.ali.1415@hotmail.com
Password: A1b2c3d4
```


Roles:
```
a- Get actors
b- Get movies
c- add actor
d- edit actor
e- edit movie
f- delete actor
```


Producer

Credentials:
```
Email: zainab.ali.1415@hotmail.com
Password: A1b2c3d4
```


Roles:
```
a- Get actors
b- Get movies
c- add actor
d- add movie
e- edit actor
f- edit movie
g- delete actor
h- delete movie
```


The Auth0 domain and api audience can be found in `setup.sh`.

## Endpoints

### `GET /movies`

Gets all movies



```

"movies": [
        {
            "genres": "Romance,Drama",
            "id": 1,
            "title": "Titanic",
            "year": "1998"
        },
        {
            "genres": "Action,Comedy",
            "id": 2,
            "title": "Bad Boys 4",
            "year": "2019"
        }
    ],
    "success": true
}
```

### `POST /movies`

Adds a new movie



```
{
    "message": "added Successfully",
    "movie": {
        "genres": "Action,Comedy",
        "id": 1,
        "title": "Bad Boys 4",
        "year": "2019"
    },
    "success": true
}
```



### `PATCH /movies/<int:id>`

Edit data on a movie in the db.


```
{
    "message": "Updated Successfully",
    "movie": {
        "genres": "Romance",
        "id": 1,
        "title": "Titanic",
        "year": "1999"
    },
    "success": true
}
```

### `DELETE /movies/<int:id>`

Delete a movie



```
{
    "message": "Deleted Successfully",
    "movie": "Titanic",
    "success": true
}
```

### `GET /actors`

Gets all actors



```
{
    "actors": [
        {
            "Roles": "all acted movies here",
            "age": 83,
            "gender": "Male",
            "id": 1,
            "name": "Morgan Freeman"
        },
        {
            "Roles": "all acted movies here",
            "age": 51,
            "gender": "Male",
            "id": 2,
            "name": "Leonrdo De Capreo"
        },
        {
            "Roles": "all acted movies here",
            "age": 30,
            "gender": "Female",
            "id": 3,
            "name": "Emma Watson"
        }
    ],
    "success": true
}
```

### `POST /actors`

Adds a new actor


```
{
    "actors": {
        "age": 30,
        "gender": "Female",
        "id": 1,
        "name": "Emma Watson"
    },
    "message": "added Successfully",
    "success": true
}
```


### `PATCH /actors/<int:id>`

Edit actor


```
{
    "actor": {
        "age": 73,
        "gender": "Male",
        "id": 1,
        "name": "Robert De Niro"
    },
    "message": "Updated Successfully",
    "success": true
}
```

### `DELETE /actors/<int:id>`

Delete a actor

```
{
    "actor": "Robert De Niro",
    "message": "Deleted Successfully",
    "success": true
}
```
