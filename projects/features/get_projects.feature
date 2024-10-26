Feature: Retrieve Projects
  As a user, I want to retrieve all projects so I can view and manage them.

  Background:
    Given the API is responsive
    And there are multiple projects in the database

  Scenario: Successfully retrieve all projects
    When the user retrieves all projects
    Then the status code 200 will be received
    And the response contains a list of projects
    And the project with title "Project Alpha" is included in the list

  Scenario: Retrieve projects when there are no projects available
    Given the database is empty
    When the user retrieves all projects
    Then the status code 200 will be received
    And the response contains an empty list for "projects"

  Scenario: Fail to retrieve a non-existent project
    When the user attempts to retrieve a project with id 123456789
    Then the status code 404 will be received
    And an error message "Project not found" will be displayed
