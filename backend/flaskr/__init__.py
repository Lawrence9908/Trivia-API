import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Allow-Control-Headers","Content-Type,Authorazetion")
        response.headers.add("Access-Alloe-Ciontol-Methods","GET,POST,PATCH,DELETE")
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).with_entities(Category.id, Category.type).all()
       
        if categories is None:
            abort(404)

        return jsonify({
            "success": True,
            "categories": dict(categories)
        })
        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        pages = request.args.get('page', 1, type=int)
        questions = Question.query.all()
        if len(questions) ==0:
            abort(404)
        start = (pages-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in questions]
        current_questions= questions[start:end] 

        categories = Category.query.order_by(Category.id).with_entities(Category.id, Category.type).all()

        return jsonify({
            "success":True,
            "questions": current_questions,
            "total_questions": len(current_questions),
            "current_category":dict(categories)[1],
            "categories": dict(categories)
        })
           
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)
        try:
            question.delete()
        except:
            abort(500)

        return jsonify({
            "success": True,
            "deleted": question_id
        })

       
            
        
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions' ,methods=['POST'])
    def add_question():
        question_to_add = request.get_json()

        if 'question' in question_to_add and 'answer' and 'difficulty' in question_to_add and 'category' in question_to_add :
            category = question_to_add.get("category",None)
            answer= question_to_add.get("answer",None)
            question =question_to_add.get("question",None)
            difficulty = question_to_add.get('difficulty',None)

            try:

                question = Question(
                    question= question,
                    answer= answer,
                    category= category,
                    difficulty= difficulty
                )

                question.insert()
            except:
                abort(422)
            return jsonify({
                "success":True,
                "question":question.format()
            })
        else:
            abort(404)
        
      
        
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search',methods=['POST'])
    def get_search_question():
        question_to_search = request.get_json()
        
        if 'searchTerm' in question_to_search:

            searchTerm = question_to_search.get('searchTerm','').strip()
            march_questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
            questions = [question.format() for question in march_questions]

            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": None
            })
        else:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        
        questions = Question.query.filter(Question.category==category_id).all()
        questions = [question.format() for question in questions]
        return jsonify({
            "success": True,
            "questions":questions,
            "total_questions":len(questions),
        })

        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes',methods=['POST'])
    def get_quizzes():
        body =request.get_json()
        category =None
        quiz_questions =None
        
         
        if 'quiz_category' in body and 'previous_questions' in body:
            
            quiz_category = body.get('quiz_category',None)
            previous_questions = body.get('previous_questions',None)
            category_id = quiz_category['id']
            category= Category.query.get(category_id)
            
            if category is not None:
                 quiz_questions= Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previous_questions)).all()
            else:
                quiz_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            
            if quiz_questions is not None:
                questions = random.choice(quiz_questions)

            return jsonify({
                "success": True,
                "question":questions.format()
            })

        else:
            abort(404)
        
       
            
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400


    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not Processable"
        }), 422

    return app