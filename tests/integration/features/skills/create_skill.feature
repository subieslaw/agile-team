Feature: Create a skill

  Scenario: Successfully create a skill with valid data
    Given the API is running
    When I POST to "/api/v1/skills" with name "Python" and category "Language"
    Then the response status is 201
    And the response data has skill name "Python"
    And the response data has category "Language"
    And the response data has an "id" field

  Scenario: Creating a skill without a name returns 422
    Given the API is running
    When I POST to "/api/v1/skills" without a name
    Then the response status is 422

  Scenario: Creating a duplicate skill name returns 409
    Given a skill named "Python" already exists
    When I POST to "/api/v1/skills" with name "Python" and category "Language"
    Then the response status is 409
