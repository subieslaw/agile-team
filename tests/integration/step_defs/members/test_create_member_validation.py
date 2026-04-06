import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/create_member.feature"


@scenario(FEATURE, "Creating a member without a required field returns 422")
def test_missing_field():
    pass


@scenario(FEATURE, "Creating a member with an invalid email returns 422")
def test_invalid_email():
    pass


@given("the API is running")
def api_running():
    pass


@pytest.fixture
async def missing_email_response(client):
    return await client.post("/api/v1/members", json={"name": "No Email"})


@when(
    parsers.parse('I create a member without the "{field}" field'),
    target_fixture="response",
)
def post_missing_field(field, missing_email_response):
    return missing_email_response


@pytest.fixture
async def invalid_email_response(client):
    return await client.post(
        "/api/v1/members",
        json={"name": "Bad Email", "email": "not-an-email"},
    )


@when(
    parsers.parse('I create a member with an invalid email "{email}"'),
    target_fixture="response",
)
def post_invalid_email(email, invalid_email_response):
    return invalid_email_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
