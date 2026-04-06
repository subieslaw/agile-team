import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/assign_skill.feature"


@scenario(FEATURE, "Assigning a skill to an unknown member returns 404")
def test_assign_skill_unknown_member():
    pass


@pytest.fixture
async def skill_only(client):
    return (await client.post("/api/v1/skills", json={"name": "Python"})).json()["data"]


@given("a skill exists", target_fixture="context")
def setup_skill(skill_only):
    return {"skill": skill_only}


@pytest.fixture
async def assign_to_unknown_member_response(client, context):
    return await client.post(
        "/api/v1/members/00000000-0000-0000-0000-000000000000/skills",
        json={"skill_id": context["skill"]["id"], "proficiency": 1},
    )


@when(parsers.parse('I assign the skill to member "{member_id}"'), target_fixture="response")
def assign_skill_unknown_member(member_id, assign_to_unknown_member_response):
    return assign_to_unknown_member_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
