Feature: Assign a skill to a team member

  Scenario: Successfully assign a skill to a member
    Given a member and a skill exist
    When I assign the skill to the member with proficiency 3
    Then the response status is 201
    And the response data has the skill name
    And the response data has proficiency 3

  Scenario: Assigning a skill to an unknown member returns 404
    Given a skill exists
    When I assign the skill to member "00000000-0000-0000-0000-000000000000"
    Then the response status is 404

  Scenario: Assigning an unknown skill to a member returns 404
    Given a member exists
    When I assign skill "00000000-0000-0000-0000-000000000000" to the member
    Then the response status is 404

  Scenario: Assigning the same skill twice returns 409
    Given a member and a skill exist
    And the skill is already assigned to the member
    When I assign the skill to the member with proficiency 3
    Then the response status is 409
