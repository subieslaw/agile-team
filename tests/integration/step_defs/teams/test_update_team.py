import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/update_team.feature"


@scenario(FEATURE, "Successfully update a team name")
def test_update_team():
    pass


@scenario(FEATURE, "Updating a team that does not exist returns 404")
def test_update_team_not_found():
    pass


@scenario(FEATURE, "Updating a team name to a duplicate returns 409")
def test_update_team_duplicate():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def created_platform(client):
    resp = await client.post("/api/v1/teams", json={"name": "Platform"})
    return resp.json()["data"]


@pytest.fixture
async def created_data(client):
    resp = await client.post("/api/v1/teams", json={"name": "Data"})
    return resp.json()["data"]


@given('a team named "Platform" already exists', target_fixture="team_platform")
def team_platform(created_platform):
    return created_platform


@given('a team named "Data" already exists', target_fixture="team_data")
def team_data(created_data):
    return created_data


@pytest.fixture
async def update_response(client, team_platform):
    return await client.patch(
        f"/api/v1/teams/{team_platform['id']}",
        json={"name": "Platform Engineering"},
    )


@when('I update the team name to "Platform Engineering"', target_fixture="response")
def update_team_name(update_response):
    return update_response


@pytest.fixture
async def update_unknown_response(client):
    return await client.patch(
        "/api/v1/teams/00000000-0000-0000-0000-000000000000",
        json={"name": "Ghost"},
    )


@when(
    parsers.parse('I update team "{team_id}" name to "Ghost"'),
    target_fixture="response",
)
def update_unknown(update_unknown_response):
    return update_unknown_response


@pytest.fixture
async def update_duplicate_response(client, team_platform, team_data):
    return await client.patch(
        f"/api/v1/teams/{team_data['id']}",
        json={"name": "Platform"},
    )


@when('I update the "Data" team name to "Platform"', target_fixture="response")
def update_to_duplicate(update_duplicate_response):
    return update_duplicate_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse('the response data contains team name "{value}"'))
def check_name(response, value):
    assert response.json()["data"]["name"] == value
