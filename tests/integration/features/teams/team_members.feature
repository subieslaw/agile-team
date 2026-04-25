Feature: Manage team membership

  Scenario: Successfully assign a member to a team
    Given the API is running
    And a team named "Platform" already exists
    And a member with email "alice@example.com" exists
    When I assign the member to the team
    Then the response status is 200
    And the response data contains the member id

  Scenario: Listing members of a team returns assigned members
    Given the API is running
    And a team named "Platform" already exists
    And a member with email "alice@example.com" exists
    And the member is assigned to the team
    When I list members of the team
    Then the response status is 200
    And the response data is a list with 1 members

  Scenario: Assigning a member to a team that does not exist returns 404
    Given the API is running
    And a member with email "alice@example.com" exists
    When I assign the member to team "00000000-0000-0000-0000-000000000000"
    Then the response status is 404

  Scenario: Assigning a member who does not exist to a team returns 404
    Given the API is running
    And a team named "Platform" already exists
    When I assign member "00000000-0000-0000-0000-000000000000" to the team
    Then the response status is 404

  Scenario: Removing a member from a team
    Given the API is running
    And a team named "Platform" already exists
    And a member with email "alice@example.com" exists
    And the member is assigned to the team
    When I remove the member from the team
    Then the response status is 204
