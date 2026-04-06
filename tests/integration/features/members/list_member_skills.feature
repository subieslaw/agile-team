Feature: List skills for a team member

  Scenario: Returns all skills assigned to a member
    Given a member has two skills assigned
    When I GET the skills for that member
    Then the response status is 200
    And the response data is a list of 2 skills

  Scenario: Returns empty list when member has no skills
    Given a member exists with no skills
    When I GET the skills for that member
    Then the response status is 200
    And the response data is an empty list

  Scenario: Returns 404 for an unknown member
    When I GET skills for member "00000000-0000-0000-0000-000000000000"
    Then the response status is 404
