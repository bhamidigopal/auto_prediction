 
Feature: Vehicle Safety Testing

  Scenario: Basic Safety Rating Validation
    Given a 2015 Bentley Mulsanne is present
    And the overall safety rating is nan
    When we check the overall safety rating
    Then it should be validated as nan

  Scenario: Advanced Safety Feature Verification
    Given a 2015 Bentley Mulsanne is present
    And the front collision warning is nan
    When we activate the front collision warning system
    Then it should emit a warning signal
    And display a message on the dashboard

  Scenario: NHTSA Compliance Checks
    Given a 2015 Bentley Mulsanne is present
    And the vehicle is equipped with all required safety features
    When we perform a NHTSA compliance check
    Then it should pass all required tests

  Scenario: Crash Test Performance Validation
    Given a 2015 Bentley Mulsanne is present
    And a crash test is performed
    When we analyze the crash test results
    Then the vehicle should have achieved a high rating
    And all safety features should have functioned properly

Examples:

  Example 1: Basic Safety Rating Validation
    Given a 2015 Bentley Mulsanne is present
    And the overall safety rating is nan
    When we check the overall safety rating
    Then it should be validated as nan

  Example 2: Advanced Safety Feature Verification
    Given a 2015 Bentley Mulsanne is present
    And the front collision warning is nan
    When we activate the front collision warning system
    Then it should emit a warning signal
    And display a message on the dashboard

  Example 3: NHTSA Compliance Checks
    Given a 2015 Bentley Mulsanne is present
    And the vehicle is equipped with all required safety features
    When we perform a NHTSA compliance check
    Then it should pass all required tests

  Example 4: Crash Test Performance Validation
    Given a 2015 Bentley Mulsanne is present
    And a crash test is performed
    When we analyze the crash test results
    Then the vehicle should have achieved a high rating
    And all safety features should have functioned properly