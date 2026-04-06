import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/get_member.feature"


@scenario(FEATURE, "Returns a member by ID")
def test_get_member():
    pass


@scenario(FEATURE, "Returns 404 for an unknown ID")
def test_get_member_not_found():
    pass


# --- given ---


@pytest.fixture
async def created_member(client):
    resp = await client.post(
        "/api/v1/members",
        json={"name": "Alice Smith", "email": "alice@example.com"},
    )
    return resp.json()["data"]


@given(
    parsers.parse('a member exists with name "{name}" and email "{email}"'),
    target_fixture="existing_member",
)
def member_exists(name, email, created_member):
    return created_member


@given("no members exist", target_fixture="existing_member")
def no_members():
    return None


# --- when ---


@pytest.fixture
async def get_by_id_response(client, existing_member):
    member_id = existing_member["id"]
    return await client.get(f"/api/v1/members/{member_id}")


@when("I GET the member by their ID", target_fixture="response")
def get_member_by_id(get_by_id_response):
    return get_by_id_response


@pytest.fixture
async def get_unknown_response(client):
    return await client.get("/api/v1/members/00000000-0000-0000-0000-000000000000")


@when(
    parsers.parse('I GET "{path}"'),
    target_fixture="response",
)
def get_path(path, get_unknown_response):
    return get_unknown_response


# --- then ---


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse('the response data has name "{value}"'))
def check_name(response, value):
    assert response.json()["data"]["name"] == value


@then(parsers.parse('the response data has email "{value}"'))
def check_email(response, value):
    assert response.json()["data"]["email"] == value
