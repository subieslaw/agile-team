Feature: List teams

  Scenario: List teams returns all active teams
    Given the API is running
    And a team named "Platform" already exists
    And a team named "Data" already exists
    When I list all teams
    Then the response status is 200
    And the response data is a list with 2 teams

  Scenario: List teams returns empty list when no teams exist
    Given the API is running
    When I list all teams
    Then the response status is 200
    And the response data is an empty list
