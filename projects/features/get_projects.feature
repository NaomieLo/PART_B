Feature: Retrieve Projects
  As a user, I want to retrieve all projects so I can view and manage them.

  Background:
    Given the API is responsive
    And there are multiple projects in the database

  # Normal Flow
  Scenario: Successfully retrieve all projects
    Given the API is responsive
    And the database contains several projects
    When the user retrieves all projects
    Then the status code 200 will be received
    And the response contains a list of projects
    And the project with title "<project_title>" is included in the list

    Examples:
      | "<project_title>"      |
      | Grocery Shopping    |
      | Complete Homework   |
      | Pay Bills           |

  # Alternate Flow
  Scenario: Retrieve projects when there are no projects available
    Given the API is responsive
    And the database contains several projects
    Given the database is empty
    When the user retrieves all projects
    Then the status code 200 will be received
    And the response contains an empty list for 'projects'

  # Error Flow
  Scenario: Fail to retrieve a non-existent project
    Given the API is responsive
    And the database contains several projects
    When the user attempts to retrieve a project with id 123456789
    Then the status code 404 will be received
    And an error message 'Could not find an instance with projects/123456789' will be displayed
