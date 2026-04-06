import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "../../features/members/assign_skill.feature"


@scenario(FEATURE, "Assigning an unknown skill to a member returns 404")
def test_assign_unknown_skill():
    pass


@pytest.fixture
async def member_only(client):
    resp = await client.post(
        "/api/v1/members", json={"name": "Alice", "email": "alice@example.com"}
    )  # noqa: E501
    return resp.json()["data"]


@given("a member exists", target_fixture="context")
def setup_member(member_only):
    return {"member": member_only}


@pytest.fixture
async def assign_unknown_skill_response(client, context):
    return await client.post(
        f"/api/v1/members/{context['member']['id']}/skills",
        json={"skill_id": "00000000-0000-0000-0000-000000000000", "proficiency": 1},
    )


@when(parsers.parse('I assign skill "{skill_id}" to the member'), target_fixture="response")
def assign_unknown_skill(skill_id, assign_unknown_skill_response):
    return assign_unknown_skill_response


@then(parsers.parse("the response status is {code:d}"))
def check_status(response, code):
    assert response.status_code == code, response.text
