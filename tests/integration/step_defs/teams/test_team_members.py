import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/team_members.feature"


@scenario(FEATURE, "Successfully assign a member to a team")
def test_assign_member():
    pass


@scenario(FEATURE, "Listing members of a team returns assigned members")
def test_list_team_members():
    pass


@scenario(FEATURE, "Assigning a member to a team that does not exist returns 404")
def test_assign_to_unknown_team():
    pass


@scenario(FEATURE, "Assigning a member who does not exist to a team returns 404")
def test_assign_unknown_member():
    pass


@scenario(FEATURE, "Removing a member from a team")
def test_remove_member():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def team(client):
    resp = await client.post("/api/v1/teams", json={"name": "Platform"})
    return resp.json()["data"]


@pytest.fixture
async def member(client):
    resp = await client.post(
        "/api/v1/members",
        json={"name": "Alice Smith", "email": "alice@example.com"},
    )
    return resp.json()["data"]


@given('a team named "Platform" already exists', target_fixture="existing_team")
def existing_team(team):
    return team


@given('a member with email "alice@example.com" exists', target_fixture="existing_member")
def existing_member(member):
    return member


@pytest.fixture
async def assign_response(client, existing_team, existing_member):
    return await client.post(f"/api/v1/teams/{existing_team['id']}/members/{existing_member['id']}")


@given("the member is assigned to the team", target_fixture="assignment")
def member_assigned(assign_response):
    return assign_response


@when("I assign the member to the team", target_fixture="response")
def assign_member(assign_response):
    return assign_response


@pytest.fixture
async def assign_unknown_team_response(client, existing_member):
    return await client.post(
        f"/api/v1/teams/00000000-0000-0000-0000-000000000000/members/{existing_member['id']}"
    )


@when(
    'I assign the member to team "00000000-0000-0000-0000-000000000000"',
    target_fixture="response",
)
def assign_to_unknown_team(assign_unknown_team_response):
    return assign_unknown_team_response


@pytest.fixture
async def assign_unknown_member_response(client, existing_team):
    return await client.post(
        f"/api/v1/teams/{existing_team['id']}/members/00000000-0000-0000-0000-000000000000"
    )


@when(
    'I assign member "00000000-0000-0000-0000-000000000000" to the team',
    target_fixture="response",
)
def assign_unknown_member(assign_unknown_member_response):
    return assign_unknown_member_response


@pytest.fixture
async def list_members_response(client, existing_team, assignment):
    return await client.get(f"/api/v1/teams/{existing_team['id']}/members")


@when("I list members of the team", target_fixture="response")
def list_members(list_members_response):
    return list_members_response


@pytest.fixture
async def remove_response(client, existing_team, existing_member, assignment):
    return await client.delete(
        f"/api/v1/teams/{existing_team['id']}/members/{existing_member['id']}"
    )


@when("I remove the member from the team", target_fixture="response")
def remove_member(remove_response):
    return remove_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then("the response data contains the member id")
def check_member_id(response):
    data = response.json()["data"]
    assert "id" in data and data["id"] is not None


@then(parsers.parse("the response data is a list with {count:d} members"))
def check_list_length(response, count):
    assert len(response.json()["data"]) == count
