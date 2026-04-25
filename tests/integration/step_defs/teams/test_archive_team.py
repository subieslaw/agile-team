import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/archive_team.feature"


@scenario(FEATURE, "Successfully archive an existing team")
def test_archive_team():
    pass


@scenario(FEATURE, "Archiving a team that does not exist returns 404")
def test_archive_team_not_found():
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
async def delete_response(client, existing_team):
    return await client.delete(f"/api/v1/teams/{existing_team['id']}")


@when("I delete the team by its ID", target_fixture="response")
def delete_team(delete_response):
    return delete_response


@pytest.fixture
async def delete_unknown_response(client):
    return await client.delete("/api/v1/teams/00000000-0000-0000-0000-000000000000")


@when(
    parsers.parse('I delete a team with id "{team_id}"'),
    target_fixture="response",
)
def delete_unknown(delete_unknown_response):
    return delete_unknown_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
