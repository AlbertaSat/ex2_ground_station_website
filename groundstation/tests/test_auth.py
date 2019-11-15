import json
from flask import current_app
from groundstation import db
from groundstation.backend_api.utils import add_user
from groundstation.tests.base import BaseTestCase

class TestAuthentication(BaseTestCase):

    def setUp(self):
        db.create_all()
        db.session.commit()
        current_app.config.update(BYPASS_AUTH=False)

    def test_login_happy(self):
        user = add_user('Nick', 'testing123')
        with self.client:
            login_data = {'username':'Nick', 'password':'testing123'}
            post_data = json.dumps(login_data)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/auth/login', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response_data['status'])
            auth_token = response_data.get('auth_token')
            self.assertTrue(auth_token is not None)

    def test_login_invalid_password(self):
        user = add_user('Nick', 'testing123')
        with self.client:
            login_data = {'username':'Nick', 'password':'wrong-password'}
            post_data = json.dumps(login_data)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/auth/login', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', response_data['status'])
            self.assertIn('Username and/or password is incorrect', response_data['message'])

    def test_login_invalid_username(self):
        user = add_user('Nick', 'testing123')
        with self.client:
            login_data = {'username':'wrong-username', 'password':'testing123'}
            post_data = json.dumps(login_data)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/auth/login', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', response_data['status'])
            self.assertIn('Username and/or password is incorrect', response_data['message'])

    def test_logout_happy(self):
        user = add_user('Nick', 'testing123')
        auth_token = user.encode_auth_token_by_id().decode()
        with self.client:
            response = self.client.get('/api/auth/logout', headers={'Authorization': f'Bearer {auth_token}'})
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response_data['status'])

    def test_logout_no_token(self):
        user = add_user('Nick', 'testing123')
        with self.client:
            response = self.client.get('/api/auth/logout')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)

    def test_logout_invalid_token(self):
        user = add_user('Nick', 'testing123')
        auth_token = user.encode_auth_token_by_id()
        with self.client:
            response = self.client.get('/api/auth/logout', headers={'Authorization': f'Bearer INVALIDTOKEN'})
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('fail', response_data['status'])

    def test_logout_expired_token(self):
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        user = add_user('Nick', 'testing123')
        auth_token = user.encode_auth_token_by_id().decode()
        with self.client:
            response = self.client.get('/api/auth/logout', headers={'Authorization': f'Bearer {auth_token}'})
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('fail', response_data['status'])
            self.assertIn('Signature expired. Please log in again.', response_data['message'])
