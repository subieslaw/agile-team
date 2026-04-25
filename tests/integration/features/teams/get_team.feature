Feature: Get a team by ID

  Scenario: Successfully retrieve an existing team
    Given the API is running
    And a team named "Platform" already exists
    When I get the team by its ID
    Then the response status is 200
    And the response data contains team name "Platform"

  Scenario: Getting a team that does not exist returns 404
    Given the API is running
    When I get a team with id "00000000-0000-0000-0000-000000000000"
    Then the response status is 404
