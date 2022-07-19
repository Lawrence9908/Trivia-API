import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_TEST_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path ="postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
        
    def test_get_quetions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        
        
    def test_add_question(self):
        res = self.client().post('/questions',json={
            "question":"My new question",
            "answer":"Answer to new question",
            "difficulty":1,
            "category":3
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        
    def test_400_add_question_invalid_or_empty(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'Resource Not Found')
        
    def test_search_question(self):
        res = self.client().post('/questions/search',json={
            "searchTerm": "My Question"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertIn('questions',data)
        
        
    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 4)
        
        
    def test_405_delete_question_no_id(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'Method Not Allowed')
        
    def test_404_delete_question_no_id(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'Resource Not Found')
        
        
    def test_get_question_by_category(self):
        res = self.client().get('categories/5/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        
    def test_404_get_question_by_category_not_exist(self):
        res = self.client().get('categories/6000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],"Resource Not Found")
        
    def test_get_quizzes(self):
        res =self.client().post('/quizzes',json={
            "previous_questions":[],
            "quiz_category":{
                "id":4,
                "type":"History"
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        
    def test_404_get_quizzes(self):
        res =self.client().post('/quizzes',json={
            "previous_questions":[]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()