import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_qusetions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    qusetions = [qusetion.format() for qusetion in selection]
    current_qusetions = qusetions[start:end]

    return current_qusetions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    ''' @TODO: Set up CORS. Allow '*' for origins. '''
    CORS(app, resources={r'/*': {'origins': '*'}})


''' @TODO: Use the after_request decorator to set Access-Control-Allow '''


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


''' @TODO: Create an endpoint to handle GET requests for all available categories. '''


@app.route('/categories', methods=['GET'])
def get_all_categories():
    try:
        AllCategories = Category.query.all()
        categories = {}
        for category in AllCategories:
            categories[category.id] = category.type
            return jsonify({
                'success': True,
                'categories': categories
                })
    except:
        abort(500)


''' @TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions).
This endpoint should return a list of questions, number of total questions, current category, categories. '''


@app.route('/questions', methods=['GET'])
def retrieve_questions():
    categories = {}
    for category in Category.query.all():
        categories[category.id] = category.type
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_qusetions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': categories,
            'total_questions': len(questions)
            })


''' @TODO: Create an endpoint to DELETE question using a question ID. '''


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.get(question_id)

        if question is None:
            abort(404, f'No question found with id: {question_id}')

        question.delete()
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_qusetions(request, questions)

        return jsonify({
          'success': True,
          'deleted': question_id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
          })

    except:
        abort(422)


''' @TODO: Create an endpoint to POST a new question, which will require the question and answer text,
category, and difficulty score. '''


@app.route('/questions', methods=['POST'])
def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)

    try:
        question = Question(question=new_question, answer=new_answer, category=category, difficulty=difficulty)
        question.insert()

        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_qusetions(request, questions)

        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
            })

    except:
        abort(422)


''' @TODO: Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term is a substring of the question. '''


@app.route('/search', methods=['POST'])
def search():
    search_term = request.json.get('searchTerm', '')

    if search_term == '':
        abort(422)

    try:
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if len(questions) == 0:
            abort(404)

        current_questions = paginate_qusetions(request, questions)

        return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': len(Question.query.all())
            })

    except:
        abort(404)


''' @TODO: Create a GET endpoint to get questions based on category. '''


@app.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
    if not category_id:
        return abort(400, 'Invalid category id')

    questions = Question.query.filter(Question.category == category_id)
    current_questions = paginate_qusetions(request, questions)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'current_category': category_id
        })


''' @TODO: Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions. '''


@app.route('/quizzes', methods=['POST'])
def play_quiz_questions():
    previous_questions = request.json.get('previous_questions')
    quiz_category = request.json.get('quiz_category')

    if not quiz_category:
        return abort(400)

    category_id = int(quiz_category.get('id'))
    questions = Question.query.filter(Question.category == category_id).all()
    question = questions.order_by(func.random()).first()

    if not question:
        return jsonify({})

    found = True
    while found:
        if question.id in previous_questions:
            next_question = question
        else:
            found = False
        return jsonify({
            'success': True,
            'question': question.format()
            })

''' @TODO: Create error handlers for all expected errors including 404 and 422. '''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422


return app
