Feature: Delete Project
  As a user, I want to delete a project so that I can remove projects that are no longer relevant.

  Background:
    Given the API is responsive
    And there is an existing project with title 'Delete Me' in the database

  # Normal Flow
  Scenario: Successfully delete a project
    When the user deletes the project with title 'Delete Me'
    Then the status code 200 will be received
    And the project with title 'Delete Me' should no longer exist in the database

 # Alternate Flow
  Scenario: Successfully delete a project by title when there are duplicate project instances
    Given there is a second project with title 'Delete Me' in the database
    When the user deletes the project with title 'Delete Me'
    Then the status code 200 will be received
    And only one project with title 'Delete Me' should exist in the database

  # Error Flow
  Scenario: Fail to delete a non-existent project
    When the user attempts to delete a project with id 123456789
    Then the status code 404 will be received
    And the error message will be empty
