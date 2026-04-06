import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/create_member.feature"


@scenario(FEATURE, "Creating a member with a duplicate email returns 409")
def test_duplicate_email():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def seed_member(client):
    await client.post(
        "/api/v1/members",
        json={"name": "Alice Smith", "email": "alice@example.com"},
    )


@given(
    parsers.parse('a member with email "{email}" already exists'),
    target_fixture="existing_member",
)
def existing_member(email, seed_member):
    return email


@pytest.fixture
async def duplicate_post_response(client, existing_member):
    return await client.post(
        "/api/v1/members",
        json={"name": "Bob Jones", "email": existing_member},
    )


@when(
    parsers.parse('I try to create another member with email "{email}"'),
    target_fixture="response",
)
def try_duplicate(email, duplicate_post_response):
    return duplicate_post_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
