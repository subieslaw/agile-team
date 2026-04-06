import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/skills/create_skill.feature"


@scenario(FEATURE, "Creating a duplicate skill name returns 409")
def test_duplicate_skill():
    pass


@pytest.fixture
async def seed_python_skill(client):
    await client.post("/api/v1/skills", json={"name": "Python", "category": "Language"})


@given('a skill named "Python" already exists', target_fixture="existing_skill")
def python_exists(seed_python_skill):
    return seed_python_skill


@pytest.fixture
async def duplicate_skill_response(client, existing_skill):
    return await client.post("/api/v1/skills", json={"name": "Python", "category": "Language"})


@when(
    parsers.parse('I POST to "/api/v1/skills" with name "{name}" and category "{category}"'),
    target_fixture="response",
)
def post_duplicate(name, category, duplicate_skill_response):
    return duplicate_skill_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
