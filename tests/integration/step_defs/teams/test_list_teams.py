import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/list_teams.feature"


@scenario(FEATURE, "List teams returns all active teams")
def test_list_teams():
    pass


@scenario(FEATURE, "List teams returns empty list when no teams exist")
def test_list_teams_empty():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def seed_two_teams(client):
    await client.post("/api/v1/teams", json={"name": "Platform"})
    await client.post("/api/v1/teams", json={"name": "Data"})


@given('a team named "Platform" already exists', target_fixture="team_platform")
def team_platform_exists(seed_two_teams):
    pass


@given('a team named "Data" already exists', target_fixture="team_data")
def team_data_exists(seed_two_teams):
    pass


@pytest.fixture
async def list_response(client):
    return await client.get("/api/v1/teams")


@when("I list all teams", target_fixture="response")
def get_teams(list_response):
    return list_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse("the response data is a list with {count:d} teams"))
def check_list_length(response, count):
    assert len(response.json()["data"]) == count


@then("the response data is an empty list")
def check_empty(response):
    assert response.json()["data"] == []
