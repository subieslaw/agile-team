Feature: Create a team

  Scenario: Successfully create a team with a name
    Given the API is running
    When I create a team with name "Platform" and description "Platform engineering"
    Then the response status is 201
    And the response data contains team name "Platform"
    And the response data contains description "Platform engineering"
    And the response data has an "id" field
    And the response data has status "active"

  Scenario: Creating a team without a name returns 422
    Given the API is running
    When I create a team without a name
    Then the response status is 422

  Scenario: Creating a team with a duplicate name returns 409
    Given the API is running
    And a team named "Platform" already exists
    When I try to create another team named "Platform"
    Then the response status is 409
