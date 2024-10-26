Feature: Create Project
  As a user, I want to create a new project so that I can manage a set of tasks within that project.

  Background:
    Given the API is responsive
    
  # Normal Flow
  Scenario: Successfully create a new project
    When the user creates a project with title 'New Project' and description 'Project Description'
    Then the status code 201 will be received
    And the response will contain a project with title 'New Project'

  # Alternate Flow
  Scenario: Create a project without a description
    When the user creates a project with title 'Project without Description'
    Then the status code 201 will be received
    And the response will contain a project with title 'Project without Description'

  # Error Flow
  Scenario: Fail to create a project with an existing title
    Given there is an existing project with title 'Duplicate Project' in the database
    When the user attempts to create a project with title 'Duplicate Project'
    Then the status code 409 will be received
    And an error message 'Project with this title already exists' will be displayed
