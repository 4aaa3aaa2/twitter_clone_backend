
'''
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
'''

import os
import sys

# Add project root to PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
import pytest
from src.twitter_clone_app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_user(client):
    print("test start")
    email = "test001@abc.def"
    response = client.post('/api/auth/test-login',json={"email": email})
    print("RESPONSE DATA:", response.get_json())
    print("api call over")
    #assert response.status_code == 200
    # Add more assertions to check the response data


'''def test_list_all_routes(client):
    print("\n--- Registered Routes ---")
    for rule in client.application.url_map.iter_rules():
        print(rule)
    print("--- End of Routes ---\n")'''
