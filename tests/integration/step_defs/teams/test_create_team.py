import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/teams/create_team.feature"


@scenario(FEATURE, "Successfully create a team with a name")
def test_create_team():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def create_team_response(client):
    return await client.post(
        "/api/v1/teams",
        json={"name": "Platform", "description": "Platform engineering"},
    )


@when(
    'I create a team with name "Platform" and description "Platform engineering"',
    target_fixture="response",
)
def post_team(create_team_response):
    return create_team_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse('the response data contains team name "{value}"'))
def check_team_name(response, value):
    assert response.json()["data"]["name"] == value


@then(parsers.parse('the response data contains description "{value}"'))
def check_description(response, value):
    assert response.json()["data"]["description"] == value


@then(parsers.parse('the response data has an "{field}" field'))
def check_field_exists(response, field):
    data = response.json()["data"]
    assert field in data and data[field] is not None


@then(parsers.parse('the response data has status "{value}"'))
def check_status_field(response, value):
    assert response.json()["data"]["status"] == value
