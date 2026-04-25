import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/create_team.feature"


@scenario(FEATURE, "Creating a team with a duplicate name returns 409")
def test_create_team_duplicate():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def seed_platform(client):
    await client.post("/api/v1/teams", json={"name": "Platform"})


@given('a team named "Platform" already exists', target_fixture="existing_team")
def existing_platform(seed_platform):
    return "Platform"


@pytest.fixture
async def duplicate_response(client, existing_team):
    return await client.post("/api/v1/teams", json={"name": existing_team})


@when('I try to create another team named "Platform"', target_fixture="response")
def post_duplicate(duplicate_response):
    return duplicate_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
