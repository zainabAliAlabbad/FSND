# Full Stack Trivia API Backend

## Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://localhost:3000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating  to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.



### Endpoints

#### GET '/categories'
General: Returns a list of category objects and success value
Sample: curl http://localhost:3000/categories
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",    
  }
}

#### GET '/questions'
General:
Returns a list of question objects, success value, and total number of questions, type of category
Results are paginated in groups of 10 questions. Include a request argument to choose page number, starting from 1.
Sample: curl http://localhost:3000/questions
{
  "success": true,
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
    },
    {...},
    .
    .
    .],
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",    
  },
  "total_questions": 4
}

#### GET '/categories/<int:category_id>/questions'
General:
Returns a list of question objects based on category, total number of questions, current category and success value
Sample: curl http://localhost:3000/categories/1/questions
{
  "success": true,
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
    },
    {...},
    .
    .
    .],
  "total_questions": 2 ,
  "current_category": 1
 }

#### POST '/questions'
General:
Creates a new question using the submitted question, answer, category  and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend.
Sample: curl http://localhost:3000/questions
{
  "success": true,
  "created": 5,
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
    },
    {...},
    .
    .
    .],
  "total_questions": 5
 }

#### POST '/search'
General:
Returns a list of question objects based on a search term, total number of questions and success value
Sample: curl http://localhost:3000/search
{
  "success": true,
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
    },
    {...},
    .
    .
    .],
  "total_questions": 4
}

#### POST '/quizzes'
General:
Returns a random and unrepetitive  questions within the given category and success value
Sample: curl http://localhost:3000/quizzes
{
  "success": true,
  "question": {
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }
}

#### DELETE '/questions/<int:question_id>'
Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend.
Sample: curl http://localhost:3000/questions/3
{
  "success": true,
  "deleted": 3 ,
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  },
  {...},
  .
  .
  .],
  "total_questions": 3
}

### Error Handling

The API will return two error types when requests fail:

404: Resource Not Found
Errors are returned as JSON objects in the following format:
{
    "success": False,
    "error": 404,
    "message":  "Not found"
}

422: Not Processable
Errors are returned as JSON objects in the following format:
{
    "success": False,
    "error": 422,
    "message":  "unprocessable"
}


```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
