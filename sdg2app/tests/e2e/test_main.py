import pytest
import requests
import yaml

with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Read config successful")

url = "{}://{}:{}".format(config['server']['schema'], config['server']['host'],
                          config['server']['port'])
session = requests.session()


@pytest.fixture(scope='class')
def register_and_login():
    # register_response = session.post(url + "/auth/register", json={
    #     "email": config['account']['username'],
    #     "password": config['account']['password'],
    #     "is_active": True,
    #     "is_superuser": True,
    #     "is_verified": True
    # })
    login_response = session.post(
        url + "/auth/jwt/login",
        data={
            'username': config['account']['username'],
            'password': config['account']['password']
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return login_response.json()


@pytest.mark.usefixtures("register_and_login")
class TestScenarios:
    def test_hello(self, register_and_login):
        response = session.get(url + "/hello")
        assert response.status_code == 200
        assert response.json() == "Hello!"
        user_r = register_and_login
        assert user_r['token_type'] == 'bearer'
