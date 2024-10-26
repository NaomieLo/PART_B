Feature: Link Category to Project
  As a user, I want to link categories to projects to organize them better.

  Background:
    Given the API is responsive
    And there is an existing project with title 'Organized Project' in the database

  # Normal Flow
  Scenario: Successfully post categories to a project
    When the user posts the category 'Urgent' for the project with title 'Organized Project'
    Then the status code 201 will be received
    And the response contains categories 'Urgent' for the project with the title 'Organized Project'

 # Alternate Flow
  Scenario: Post multiple categories to a project
    Given the project with title 'Organized Project' already has categories 'Not Urgent' and 'Not Categorized'
    When the user posts the category 'Urgent' for the project with title 'Organized Project'
    Then the status code 201 will be received
    And the response contains categories 'Not Urgent, Not Categorized, Urgent' for the project with the title 'Organized Project'

  # Error Flow
  Scenario: Fail to link a category to a non-existent project
    When the user attempts to post the category 'Non-Urgent' for a non-existent project
    Then the status code 404 will be received
    And the error message will be empty
