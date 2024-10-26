Feature: Delete Project
  As a user, I want to delete a project so that I can remove projects that are no longer relevant.

  Background:
    Given the API is responsive
    And there is an existing project with title "Delete Me" in the database

  Scenario: Successfully delete a project
    When the user deletes the project with title "Delete Me"
    Then the status code 204 will be received
    And the project with title "Delete Me" should no longer exist in the database

  Scenario: Fail to delete a non-existent project
    When the user attempts to delete a project with id 123456789
    Then the status code 404 will be received
    And an error message "Project not found" will be displayed
