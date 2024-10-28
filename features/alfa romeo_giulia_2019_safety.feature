 
Feature: Vehicle Safety Testing

  Scenario: Basic Safety Rating Validation
    Given the 2019 ALFA ROMEO GIULIA has an overall safety rating of nan
    When the vehicle's safety rating is accessed
    Then the rating should match the provided data

  Scenario: Advanced Safety Feature Verification
    Given the 2019 ALFA ROMEO GIULIA is equipped with the following safety features:
      - Front Collision Warning: Optional
      - Lane Departure Warning: Optional
      - Crash Imminent Brake: Optional
      - Dynamic Brake Support: Optional
      - Blind Spot Detection: Optional
    When the vehicle is driven on a test track
    Then the front collision warning should activate in the event of an impending collision
    Then the lane departure warning should activate when the vehicle drifts out of its lane
    Then the crash imminent brake should activate in the event of a simulated collision
    Then the dynamic brake support should maintain optimal braking performance during hard braking
    Then the blind spot detection should alert the driver when a vehicle is detected in the blind spot

  Scenario: NHTSA Compliance Checks
    Given the 2019 ALFA ROMEO GIULIA is tested against NHTSA safety standards
    When the vehicle's safety features are tested
    Then the vehicle should pass all required safety tests

  Scenario: Crash Test Performance Validation
    Given the 2019 ALFA ROMEO GIULIA is subjected to a crash test
    When the vehicle is involved in a crash test
    Then the vehicle should come to a stop safely
    Then all safety systems should function correctly during the crash test
    Then there should be no major damage to the vehicle or its occupants
    Then the safety features should have mitigated the severity of the crash

These feature files will help ensure the proper testing and validation of the 2019 ALFA ROMEO GIULIA's safety features.