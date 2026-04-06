import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/create_member.feature"


@scenario(FEATURE, "Successfully create a team member with valid data")
def test_create_member():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def create_member_response(client):
    """Performs the POST /api/v1/members request used by the happy-path scenario."""
    return await client.post(
        "/api/v1/members",
        json={
            "name": "Alice Smith",
            "email": "alice@example.com",
            "role": "Backend Engineer",
            "team": "Platform",
        },
    )


_WHEN_CREATE = (
    'I create a member with name "Alice Smith" email "alice@example.com"'
    ' role "Backend Engineer" team "Platform"'
)


@when(_WHEN_CREATE, target_fixture="response")
def post_member(create_member_response):
    return create_member_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse('the response data contains name "{value}"'))
def check_name(response, value):
    assert response.json()["data"]["name"] == value


@then(parsers.parse('the response data contains email "{value}"'))
def check_email(response, value):
    assert response.json()["data"]["email"] == value


@then(parsers.parse('the response data has an "{field}" field'))
def check_field_exists(response, field):
    data = response.json()["data"]
    assert field in data and data[field] is not None


@then(parsers.parse('the response data has "{field}" equal to {expected}'))
def check_bool_field(response, field, expected):
    data = response.json()["data"]
    expected_val = expected.lower() == "true"
    assert data[field] == expected_val
