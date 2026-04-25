Feature: Archive a team

  Scenario: Successfully archive an existing team
    Given the API is running
    And a team named "Platform" already exists
    When I delete the team by its ID
    Then the response status is 204

  Scenario: Archiving a team that does not exist returns 404
    Given the API is running
    When I delete a team with id "00000000-0000-0000-0000-000000000000"
    Then the response status is 404
