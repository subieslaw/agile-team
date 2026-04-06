import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/skills/create_skill.feature"


@scenario(FEATURE, "Successfully create a skill with valid data")
def test_create_skill():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def create_skill_response(client):
    return await client.post("/api/v1/skills", json={"name": "Python", "category": "Language"})


@when(
    parsers.parse('I POST to "/api/v1/skills" with name "{name}" and category "{category}"'),
    target_fixture="response",
)
def post_skill(name, category, create_skill_response):
    return create_skill_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse('the response data has skill name "{value}"'))
def check_skill_name(response, value):
    assert response.json()["data"]["name"] == value


@then(parsers.parse('the response data has category "{value}"'))
def check_category(response, value):
    assert response.json()["data"]["category"] == value


@then(parsers.parse('the response data has an "{field}" field'))
def check_field_exists(response, field):
    data = response.json()["data"]
    assert field in data and data[field] is not None
