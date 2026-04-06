import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/skills/create_skill.feature"


@scenario(FEATURE, "Creating a skill without a name returns 422")
def test_missing_name():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def missing_name_response(client):
    return await client.post("/api/v1/skills", json={"category": "Language"})


@when('I POST to "/api/v1/skills" without a name', target_fixture="response")
def post_skill_no_name(missing_name_response):
    return missing_name_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
