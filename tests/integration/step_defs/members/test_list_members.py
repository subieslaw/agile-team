import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/list_members.feature"


@scenario(FEATURE, "Returns all active members")
def test_list_active_members():
    pass


@scenario(FEATURE, "Returns empty list when no members exist")
def test_list_empty():
    pass


@scenario(FEATURE, "Inactive members are not returned")
def test_inactive_excluded():
    pass


# --- given ---


@pytest.fixture
async def seed_two_active(client):
    await client.post("/api/v1/members", json={"name": "Alice", "email": "alice@example.com"})
    await client.post("/api/v1/members", json={"name": "Bob", "email": "bob@example.com"})


@given("two active members exist", target_fixture="setup")
def two_active(seed_two_active):
    return seed_two_active


@given("no members exist", target_fixture="setup")
def no_members():
    pass


@pytest.fixture
async def seed_active_and_inactive(client, session):
    await client.post("/api/v1/members", json={"name": "Alice", "email": "alice@example.com"})
    # create inactive member directly via DB
    from app.db.models import TeamMember

    inactive = TeamMember(name="Inactive Bob", email="bob@example.com", is_active=False)
    session.add(inactive)
    await session.commit()


@given("an active member and an inactive member exist", target_fixture="setup")
def active_and_inactive(seed_active_and_inactive):
    return seed_active_and_inactive


# --- when ---


@pytest.fixture
async def list_response(client):
    return await client.get("/api/v1/members")


@when(parsers.parse('I GET "{path}"'), target_fixture="response")
def get_members(path, list_response):
    return list_response


# --- then ---


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse("the response data is a list of {count:d} members"))
def check_count(response, count):
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) == count, f"Expected {count} members, got {len(data)}"


@then("the response data is an empty list")
def check_empty(response):
    data = response.json()["data"]
    assert data == []
