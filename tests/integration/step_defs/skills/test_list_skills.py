import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/skills/list_skills.feature"


@scenario(FEATURE, "Returns all skills")
def test_list_skills():
    pass


@scenario(FEATURE, "Returns empty list when no skills exist")
def test_list_skills_empty():
    pass


# --- given ---


@pytest.fixture
async def seed_two_skills(client):
    await client.post("/api/v1/skills", json={"name": "Python"})
    await client.post("/api/v1/skills", json={"name": "Docker"})


@given("two skills exist", target_fixture="setup")
def two_skills(seed_two_skills):
    return seed_two_skills


@given("no skills exist", target_fixture="setup")
def no_skills():
    pass


# --- when ---


@pytest.fixture
async def list_skills_response(client):
    return await client.get("/api/v1/skills")


@when(parsers.parse('I GET "{path}"'), target_fixture="response")
def get_skills(path, list_skills_response):
    return list_skills_response


# --- then ---


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse("the response data is a list of {count:d} skills"))
def check_count(response, count):
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) == count, f"Expected {count} skills, got {len(data)}"


@then("the response data is an empty list")
def check_empty(response):
    assert response.json()["data"] == []
