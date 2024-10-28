 
Feature: Vehicle Safety Testing

  Scenario: Basic safety rating validation
    Given the 2024 Alfa Giulia has an overall safety rating of nan
    When the vehicle is inspected for safety
    Then the safety rating should match the provided data

  Scenario: Advanced safety feature verification
    Given the 2024 Alfa Giulia is equipped with:
      - Front Collision Warning: Standard
      - Lane Departure Warning: Optional
      - Crash Imminent Brake: Standard
      - Dynamic Brake Support: Standard
      - Blind Spot Detection: Standard
    When the vehicle is tested for advanced safety features
    Then all features should function as expected

  Scenario: NHTSA compliance checks
    Given the 2024 Alfa Giulia is tested against NHTSA safety standards
    When the vehicle is inspected for compliance
    Then it should meet all required safety standards

  Scenario: Crash test performance validation
    Given the 2024 Alfa Giulia is subjected to crash tests
    When the vehicle is evaluated for crash test performance
    Then it should achieve a satisfactory rating in all relevant tests

Examples:

  Example: Basic safety rating validation
    Given the 2024 Alfa Giulia has an overall safety rating of nan
    When the vehicle is inspected for safety
    Then the safety rating should match the provided data

  Example: Advanced safety feature verification
    Given the 2024 Alfa Giulia is equipped with:
      - Front Collision Warning: Standard
      - Lane Departure Warning: Optional
      - Crash Imminent Brake: Standard
      - Dynamic Brake Support: Standard
      - Blind Spot Detection: Standard
    When the vehicle is tested for advanced safety features
    Then all features should function as expected

  Example: NHTSA compliance checks
    Given the 2024 Alfa Giulia is tested against NHTSA safety standards
    When the vehicle is inspected for compliance
    Then it should meet all required safety standards

  Example: Crash test performance validation
    Given the 2024 Alfa Giulia is subjected to crash tests
    When the vehicle is evaluated for crash test performance
    Then it should achieve a satisfactory rating in all relevant tests