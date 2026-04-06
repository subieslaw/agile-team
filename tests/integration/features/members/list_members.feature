Feature: List team members

  Scenario: Returns all active members
    Given two active members exist
    When I GET "/api/v1/members"
    Then the response status is 200
    And the response data is a list of 2 members

  Scenario: Returns empty list when no members exist
    Given no members exist
    When I GET "/api/v1/members"
    Then the response status is 200
    And the response data is an empty list

  Scenario: Inactive members are not returned
    Given an active member and an inactive member exist
    When I GET "/api/v1/members"
    Then the response status is 200
    And the response data is a list of 1 members
