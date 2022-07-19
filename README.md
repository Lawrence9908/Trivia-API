# Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.

2- Delete questions.

3- Add questions and require that they include question and answer text.

4- Search for questions based on a text query string.

5- Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

All required packages are included in the requirements file.

```
cd backend/
pip install requirements.txt


```
To set up database in your local machine
'''
    psql trivia < trivia.psql
'''
To run the application, execute the follow:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

### Frontend

From the root folder, run the following commands to start the client:

```
cd frontend/
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate from the root folder and run the following commands:

```
cd backend/
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "Bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 422: Not Processable
- 404: Resource Not Found
- 500: Internal Server Error
- 405: Method Not Found

# Endpoints

### GET /categories

- General:
  - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs

```
curl http://127.0.0.1:5000/categories
```

- Sample Response:

```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

### GET /questions?page=${integer}

- General:
  - fetches paginated questions in  group of 10, total number off qustions, all categories and  carent categories string.
  - Returns a JSON object with 10 paginated questions, total questions, object with all categories, and current category 

```
Example: curl http://127.0.0.1:5000/questions
```
- Sample Response:

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_question": 10
```

### GET /categories/${category_id}/questions

- General:
  - It fatches the question that follows under the passed category_id and the category_id must be of type integer 
  - Returns an object with questions for the specified category, total questions, and current category string

```
curl http://127.0.0.1:5000/categories/4/questions
```

- Sample Response:

```
{
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

### DELETE /questions/{question_id}

- General:
  - Detelets the question of specified question_id, the question it the question_id passed will be deleted
  - Returns the JSON object with success and id of the deleted question, 
- Sample Request:

```
Example: curl -X DELETE http://127.0.0.1:5000/questions/4
```

- Sample Response:

```
{
    "success":True,
    "deleted": 4,
}
```

### POST /quizzes

- General:
  - Sends a post request in order to get the next question
  - Takes the previous_questions and quiz_category
  - Returns: a single new question object that is not in the previous_questions
- Sample Request: (gets from any category)

```
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": []
    quiz_category": {"type":"Science", "id":1}'
```

- Sample Response:

```
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```

### POST /questions

- General:
  - Sends a post request in order to add a new question, takes a JSON object containing keys: question, answer, difficulty, category
  - Returns success massage and the new question
- Sample Request:

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"How hard is vasity programming", "answer":"if it your first programming class it will be hard for you", "difficulty":3, "category":1}'
```

- Sample Response:

```
{
    'question': {
        'id': 24,
        'question': 'How hard is vasity programming',
        'answer': 'if it your first programming class it will be hard for you',
        'difficulty': 1,
        'category': 3
    }
}
```

### POST /questions

- General:
  - Sends a post request in order to search for a specific question by search term ,takes a JSON object containing key: searchTerm
  - Returns any array of questions, a number of total questions that met the search term and the current category string
- Sample Request:

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Which country won the first ever soccer World Cup in 1930?"}'
```

- Sample Response:

```
{
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "sueccess": true,
    "total_questions": 1
}
```
## Authors

Lawrence Mugwena

