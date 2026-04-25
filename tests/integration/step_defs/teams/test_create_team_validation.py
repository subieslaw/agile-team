import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/create_team.feature"


@scenario(FEATURE, "Creating a team without a name returns 422")
def test_create_team_no_name():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def missing_name_response(client):
    return await client.post("/api/v1/teams", json={"description": "No name"})


@when("I create a team without a name", target_fixture="response")
def post_no_name(missing_name_response):
    return missing_name_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
