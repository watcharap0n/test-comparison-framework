import logging
import os
from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient
from mongomock import MongoClient
from server.main import app

LOGGER = logging.getLogger(__name__)
payload = {
    'username': 'dev',
    'firstname': 'watcharapon',
    'lastname': 'weeraborirak'
}


class TestUnitAPI(TestCase):
    def setUp(self):
        # Create a mock MongoDB client using mongomock
        self.db = MongoClient()

        # Use the TestClient with the FastAPI app
        self.client = TestClient(app)

        # Set the authorization header
        self.authorization_header = {'user-agent': os.environ.get('USER_AGENT')}

        # Create a user and get the created_id
        response = self.client.post('/user/create', json=payload, headers=self.authorization_header)
        self.created_user_by_id = response.json()['_id']

    def tearDown(self):
        # Cleanup after all tests are executed
        self.client.delete(f'/user/delete/{self.created_user_by_id}', headers=self.authorization_header)

        # Close the mock MongoDB client
        self.db.close()

    def test_create_success(self):
        response = self.client.get(f'/user/find/{self.created_user_by_id}', headers=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_duplicate(self):
        response = self.client.post('/user/create', json=payload, headers=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_unprocessable(self):
        n_payload = payload.copy()
        del n_payload['username']
        response = self.client.post('/user/create', json=n_payload, headers=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # testing method put status code 200
    def test_update_user_success(self):
        payload['username'] = 'kane'
        response = self.client.put(f'/user/update/{self.created_user_by_id}', json=payload,
                                   headers=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # testing method put status code 400
    def test_update_user_duplicate(self):
        payload['username'] = 'kane'
        response = self.client.put(f'/user/update/{self.created_user_by_id}', json=payload,
                                   headers=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        response = self.client.delete(f'/user/delete/{self.created_user_by_id}', headers=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
