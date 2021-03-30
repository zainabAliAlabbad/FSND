#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, movie, actor, init_db

assistant='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MTg0NjRmYjc3NDIwMDY5ODQzY2Q1IiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MDg2NzMwLCJleHAiOjE2MTcwOTM5MzAsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.UtLJmqLExBRz71U9mnLPMp55srDUcmqB5hDnUBz-LVoInXzEGZ2ebbijoqLg3G_cPBF5TmFOr8G7qxsSjrrBT7exxc7jouL6oCy5M4dRPTyxhZOHPbpoywoVJvB3P4cRWGPZW7Fx4F_eAtyDkKJTRhoTcdtIp7SUsWitjt1NcxiDzGeFFTwTwW9ruH-Bbgsr6zXucil_O7hdvmuuEpB6EyNMlB0caBfSS276fwNtaIV9gnXfjLkvFssaQbUuW9fr1SyRf8RT8FjNNvwoO2u6HqYtCnXIsPtf0YGvwqdoSETKvdulDJjYVCpHgGxoMrQJ3CvC_yL4McIlS1eLo1iUzA'

director='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MmM3ZjFhYTI5NGEwMDY5YTYwMjc4IiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MDg2NTYwLCJleHAiOjE2MTcwOTM3NjAsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.mWXE45EXvRY4CNMT-5kNMYZ08XReS3u7NUPxCs5HVLmezM0KhJ9pTYk7tpIV39Mn0-Wh5qmRk3pdPl6pZul66FPdg_Qn6Ri4v2B6bO-MdzCE3G1FacA4SpH3ZLiOTqbVSf00HEgo-dMhjVBN7DLzaCWVTTdDc6euD5SFATOItHbuithW2LURz65DVH7iFQZF-EpbjgGUSN2KCJRiRLYj3eLpSoi0TnbpunQgoO1hJ1E_u_qvENXdfL4m4HdbJbaEMLNVS_Fn2bV-i2SZMKDxOPEXyMuPxTK3D6IgCG6DBbObgYYt4oyviwDYkTl3KhVdXaP3W5Hrb91lQnFrcMZHTw'

producer='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNTUzYjAzNDAyODUwMDcxNjBlZWIyIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MDg0ODQ0LCJleHAiOjE2MTcwOTIwNDQsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.m3EF6FQ6dHiJUP0iF6PDZIDTXCJyrmKQJOKovPlf4gYXoTdnNLfNqlwR1fJpkVAAqNGuyROn8torQ8o7pllWYXD58k7Y5EI8-H9gb12tk7qnNG0crR4nnFq4jyoSv5yUOqsH8Y60PgDGLqGZdATZqje1SvD_83riA6M07Wrf55JoRBcaIW8o5AIbBMNRxM978xR2M8N2ATFQk-roJbK4YI6jVg3-i5m91sv_xdptHyiplLWLH6R-hAXW8JixDX6317dVL_xVcXzUB0-4mh1fV_zxyB-G_IaPwaEBYUxhU8vnvvINkqyiLFPr4n8zXDsuWLN1JK73z9LvoBP0-fjMbw'

unath = {'code': 'unauthorized', 'description': 'Permission not authorized.'}


class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://postgres:A1b2c3d4@localhost:5432/capstone-project'
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

#  Movie Tests

    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + assistant})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movie_byID(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        response = self.client().get(
            f'/movies/{movie_id}',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], mov.format())

    def test_404_get_movie_byID(self):
        response = self.client().get(
            '/movies/1000',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_movie(self):
        new_movie = {
            'title': 'capstone',
            'genres': 'Drama',
            'year': '2021'
        }

        mov = movie(title='capstone', genres='Drama', year='2021')
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + producer}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'added Successfully')

    def test_422_post_movie(self):
        new_movie = {
            'title': 'capstone'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + producer}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_Unauth_post_movie(self):

        new_movie = {
            'title': 'capstone',
            'genres': 'Drama',
            'year': '2021'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + director}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)

    def test_patch_movie(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        edit_movie = {
            'title': 'capstone2',
            'genres': 'comedy',
            'year': '2022'
        }
        response = self.client().patch(
            f'/movies/{movie_id }',
            headers={"Authorization": " Bearer " + producer}, json=edit_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Updated Successfully')
        self.assertEqual(data['movie'], mov.format())

    def test_404_patch_movie(self):

        edit_movie = {
            'title': 'capstone2',
            'genres': 'comedy',
            'year': '2022'
        }
        response = self.client().patch(
            '/movies/1800',
            headers={"Authorization": " Bearer " + producer}, json=edit_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        response = self.client().delete(
            f'/movies/{movie_id }',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted Successfully')
        self.assertEqual(data['movie'], mov.title)

    def test_404_delete_movie(self):

        response = self.client().delete(
            f'/movies/50',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_Unauth_delete_movie(self):

        response = self.client().delete(
            '/movies/50',
            headers={"Authorization": " Bearer " + director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)

    # Actors Test

    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + assistant})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_byID(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().get(
            f'/actors/{actor_id}',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], act.format())

    def test_404_get_actor_byID(self):
        response = self.client().get(
            '/actors/1000',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_actor(self):
        new_actor = {
            'name': 'name',
            'age': 50,
            'gender': 'male'
        }

        act = actor(name='name', age=50, gender='male')
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + producer}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'added Successfully')

    def test_422_post_actor(self):
        new_actor = {
            'age': 54
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + producer}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_Unauth_post_actor(self):

        new_actor = {
            'name': 'name',
            'age': 50,
            'gender': 'male'
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + assistant}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)

    def test_patch_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        edit_actor = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(
            f'/actors/{actor_id }',
            headers={"Authorization": " Bearer " + producer}, json=edit_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Updated Successfully')
        self.assertEqual(data['actor'], act.format())

    def test_404_patch_actor(self):

        edit_actor = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(
            '/actors/1800',
            headers={"Authorization": " Bearer " + producer}, json=edit_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().delete(
            f'/actors/{actor_id}',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted Successfully')
        self.assertEqual(data['actor'], act.name)

    def test_404_delete_actor(self):

        response = self.client().delete(
            f'/actors/20',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_Unauth_delete_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().delete(
            '/actors/50',
            headers={"Authorization": " Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
