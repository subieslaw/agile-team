Feature: Update a team

  Scenario: Successfully update a team name
    Given the API is running
    And a team named "Platform" already exists
    When I update the team name to "Platform Engineering"
    Then the response status is 200
    And the response data contains team name "Platform Engineering"

  Scenario: Updating a team that does not exist returns 404
    Given the API is running
    When I update team "00000000-0000-0000-0000-000000000000" name to "Ghost"
    Then the response status is 404

  Scenario: Updating a team name to a duplicate returns 409
    Given the API is running
    And a team named "Platform" already exists
    And a team named "Data" already exists
    When I update the "Data" team name to "Platform"
    Then the response status is 409
