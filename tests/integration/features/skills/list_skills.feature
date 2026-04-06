Feature: List skills

  Scenario: Returns all skills
    Given two skills exist
    When I GET "/api/v1/skills"
    Then the response status is 200
    And the response data is a list of 2 skills

  Scenario: Returns empty list when no skills exist
    Given no skills exist
    When I GET "/api/v1/skills"
    Then the response status is 200
    And the response data is an empty list
