import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/assign_skill.feature"


@scenario(FEATURE, "Assigning the same skill twice returns 409")
def test_assign_skill_duplicate():
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
async def first_assignment(client, context):
    await client.post(
        f"/api/v1/members/{context['member']['id']}/skills",
        json={"skill_id": context["skill"]["id"], "proficiency": 2},
    )


@given("the skill is already assigned to the member", target_fixture="already_assigned")
def skill_already_assigned(first_assignment):
    return first_assignment


@pytest.fixture
async def duplicate_assign_response(client, context, already_assigned):
    return await client.post(
        f"/api/v1/members/{context['member']['id']}/skills",
        json={"skill_id": context["skill"]["id"], "proficiency": 3},
    )


@when(
    parsers.parse("I assign the skill to the member with proficiency {proficiency:d}"),
    target_fixture="response",
)
def assign_duplicate(proficiency, duplicate_assign_response):
    return duplicate_assign_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
