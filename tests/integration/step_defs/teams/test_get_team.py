import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/get_team.feature"


@scenario(FEATURE, "Successfully retrieve an existing team")
def test_get_team():
    pass


@scenario(FEATURE, "Getting a team that does not exist returns 404")
def test_get_team_not_found():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def created_team(client):
    resp = await client.post("/api/v1/teams", json={"name": "Platform"})
    return resp.json()["data"]


@given('a team named "Platform" already exists', target_fixture="existing_team")
def existing_team(created_team):
    return created_team


@pytest.fixture
async def get_by_id_response(client, existing_team):
    return await client.get(f"/api/v1/teams/{existing_team['id']}")


@when("I get the team by its ID", target_fixture="response")
def get_team(get_by_id_response):
    return get_by_id_response


@pytest.fixture
async def get_unknown_response(client):
    return await client.get("/api/v1/teams/00000000-0000-0000-0000-000000000000")


@when(
    parsers.parse('I get a team with id "{team_id}"'),
    target_fixture="response",
)
def get_unknown_team(get_unknown_response):
    return get_unknown_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse('the response data contains team name "{value}"'))
def check_name(response, value):
    assert response.json()["data"]["name"] == value
