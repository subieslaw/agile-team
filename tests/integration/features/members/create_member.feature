Feature: Create a team member

  Scenario: Successfully create a team member with valid data
    Given the API is running
    When I create a member with name "Alice Smith" email "alice@example.com" role "Backend Engineer" team "Platform"
    Then the response status is 201
    And the response data contains name "Alice Smith"
    And the response data contains email "alice@example.com"
    And the response data has an "id" field
    And the response data has "is_active" equal to true

  Scenario: Creating a member without a required field returns 422
    Given the API is running
    When I create a member without the "email" field
    Then the response status is 422

  Scenario: Creating a member with an invalid email returns 422
    Given the API is running
    When I create a member with an invalid email "not-an-email"
    Then the response status is 422

  Scenario: Creating a member with a duplicate email returns 409
    Given the API is running
    And a member with email "alice@example.com" already exists
    When I try to create another member with email "alice@example.com"
    Then the response status is 409
