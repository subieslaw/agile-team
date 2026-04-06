import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/list_member_skills.feature"


@scenario(FEATURE, "Returns all skills assigned to a member")
def test_list_member_skills():
    pass


@scenario(FEATURE, "Returns empty list when member has no skills")
def test_list_member_skills_empty():
    pass


@scenario(FEATURE, "Returns 404 for an unknown member")
def test_list_member_skills_not_found():
    pass


# --- given ---


@pytest.fixture
async def member_with_two_skills(client):
    resp = await client.post(
        "/api/v1/members", json={"name": "Alice", "email": "alice@example.com"}
    )  # noqa: E501
    member = resp.json()["data"]
    skill1 = (await client.post("/api/v1/skills", json={"name": "Python"})).json()["data"]
    skill2 = (await client.post("/api/v1/skills", json={"name": "Docker"})).json()["data"]
    await client.post(f"/api/v1/members/{member['id']}/skills", json={"skill_id": skill1["id"]})
    await client.post(f"/api/v1/members/{member['id']}/skills", json={"skill_id": skill2["id"]})
    return member


@given("a member has two skills assigned", target_fixture="context")
def setup_member_with_skills(member_with_two_skills):
    return {"member": member_with_two_skills}


@pytest.fixture
async def member_no_skills(client):
    resp = await client.post("/api/v1/members", json={"name": "Bob", "email": "bob@example.com"})
    return resp.json()["data"]


@given("a member exists with no skills", target_fixture="context")
def setup_member_no_skills(member_no_skills):
    return {"member": member_no_skills}


# --- when ---


@pytest.fixture
async def list_skills_for_member_response(client, context):
    member_id = context["member"]["id"]
    return await client.get(f"/api/v1/members/{member_id}/skills")


@when("I GET the skills for that member", target_fixture="response")
def get_member_skills(list_skills_for_member_response):
    return list_skills_for_member_response


@pytest.fixture
async def list_skills_unknown_member_response(client):
    return await client.get("/api/v1/members/00000000-0000-0000-0000-000000000000/skills")


@when(parsers.parse('I GET skills for member "{member_id}"'), target_fixture="response")
def get_unknown_member_skills(member_id, list_skills_unknown_member_response):
    return list_skills_unknown_member_response


# --- then ---


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then(parsers.parse("the response data is a list of {count:d} skills"))
def check_count(response, count):
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) == count, f"Expected {count} skills, got {len(data)}"


@then("the response data is an empty list")
def check_empty(response):
    assert response.json()["data"] == []
