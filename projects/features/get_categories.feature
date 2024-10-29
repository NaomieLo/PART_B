Feature: Retrieve Categories of a Project
  As a user, I want to retrieve categories for a project so that I can view the categories associated with it.

  Background:
    Given the API is responsive
    And there is an existing project with title 'Organized Project' in the database

  # Normal Flow: Retrieve categories for an existing project that has categories
  Scenario: Successfully retrieve categories for an existing project with categories
    Given the project with title 'Organized Project' already has categories 'Urgent' and 'Not Urgent'
    When the user retrieves the categories for the project with title 'Organized Project'
    Then the status code 200 will be received
    And the response contains categories 'Urgent, Not Urgent' for the project with the title 'Organized Project'

  # Alternate Flow: Attempt to retrieve categories for an existing project with no categories
  Scenario: Successfully retrieve an empty list of categories for an existing project with no categories
    Given the project with title 'Organized Project' has no categories
    When the user retrieves the categories for the project with title 'Organized Project'
    Then the status code 200 will be received
    And the response contains an empty list for 'categories'

  # Error Flow: Attempt to retrieve categories for a non-existent project
  Scenario: Fail to retrieve categories for a non-existent project with a numerical ID
    Given there is no project with ID 3 in the database
    When the user attempts to retrieve categories for the project with ID 3
    Then the status code 404 will be received
    And the error message will be empty
