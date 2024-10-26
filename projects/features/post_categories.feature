Feature: Link Category to Project
  As a user, I want to link categories to projects to organize them better.

  Background:
    Given the API is responsive
    And there is an existing project with title "Organized Project" in the database
    And there is a category with title "Urgent"

  Scenario: Successfully link a category to a project
    When the user links the category "Urgent" to the project with title "Organized Project"
    Then the status code 201 will be received
    And the project with title "Organized Project" will contain the category "Urgent"

  Scenario: Fail to link a category to a non-existent project
    When the user attempts to link the category "Urgent" to a project with id 123456789
    Then the status code 404 will be received
    And an error message "Project not found" will be displayed
