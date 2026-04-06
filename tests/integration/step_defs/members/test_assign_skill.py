import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/assign_skill.feature"


@scenario(FEATURE, "Successfully assign a skill to a member")
def test_assign_skill():
    pass


@pytest.fixture
async def member_and_skill(client):
    resp = await client.post(
        "/api/v1/members", json={"name": "Alice", "email": "alice@example.com"}
    )  # noqa: E501
    member = resp.json()["data"]
    skill = (await client.post("/api/v1/skills", json={"name": "Python"})).json()["data"]
    return {"member": member, "skill": skill}


@given("a member and a skill exist", target_fixture="context")
def setup_member_and_skill(member_and_skill):
    return member_and_skill


@pytest.fixture
async def assign_skill_response(client, context):
    member_id = context["member"]["id"]
    skill_id = context["skill"]["id"]
    return await client.post(
        f"/api/v1/members/{member_id}/skills",
        json={"skill_id": skill_id, "proficiency": 3},
    )


@when(
    parsers.parse("I assign the skill to the member with proficiency {proficiency:d}"),
    target_fixture="response",
)
def assign_skill(proficiency, assign_skill_response):
    return assign_skill_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text


@then("the response data has the skill name")
def check_skill_name(response, context):
    assert response.json()["data"]["skill_name"] == context["skill"]["name"]


@then(parsers.parse("the response data has proficiency {value:d}"))
def check_proficiency(response, value):
    assert response.json()["data"]["proficiency"] == value
