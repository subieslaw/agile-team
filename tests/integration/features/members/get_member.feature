Feature: Get a single team member

  Scenario: Returns a member by ID
    Given a member exists with name "Alice Smith" and email "alice@example.com"
    When I GET the member by their ID
    Then the response status is 200
    And the response data has name "Alice Smith"
    And the response data has email "alice@example.com"

  Scenario: Returns 404 for an unknown ID
    Given no members exist
    When I GET "/api/v1/members/00000000-0000-0000-0000-000000000000"
    Then the response status is 404
