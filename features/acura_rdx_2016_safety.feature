 
Feature: Vehicle Safety Features

  Given a 2016 Acura RDX with the following safety features:
  - Overall Rating: 5.0
  - Front Collision Warning: Optional
  - Lane Departure Warning: Optional
  - Crash Imminent Brake: Optional
  - Dynamic Brake Support: Optional
  - Blind Spot Detection: Optional

  When the vehicle is started and the safety features are enabled

  And the vehicle is driven on a variety of roads and highways

  Then the safety features should function as expected

  And the overall safety rating should match the NHTSA's assessment

  And the vehicle should pass crash tests

  Scenario: Validating the Basic Safety Rating

  Given the vehicle has an overall safety rating of 5.0

  When the safety features are enabled

  And the vehicle is driven on a variety of roads and highways

  Then the safety rating should be validated

  And the vehicle should maintain a 5.0 safety rating

  Scenario: Verifying Front Collision Warning

  Given the vehicle has Front Collision Warning as an optional feature

  When the safety features are enabled

  And the vehicle is driven on a busy highway

  Then the Front Collision Warning system should detect potential collisions

  And alert the driver with visual and audible cues

  Scenario: Checking Lane Departure Warning

  Given the vehicle has Lane Departure Warning as an optional feature

  When the safety features are enabled

  And the vehicle is driven on a winding road

  Then the Lane Departure Warning system should detect lane drift

  And alert the driver with visual and audible cues

  Scenario: Ensuring Crash Imminent Brake

  Given the vehicle has Crash Imminent Brake as an optional feature

  When the safety features are enabled

  And the vehicle is driven at high speeds on a straight road

  Then the Crash Imminent Brake system should activate

  And slow down the vehicle in time to avoid a collision

  Scenario: Validating Dynamic Brake Support

  Given the vehicle has Dynamic Brake Support as an optional feature

  When the safety features are enabled

  And the vehicle is driven on a variety of roads and highways

  Then the Dynamic Brake Support system should adjust braking force

  And maintain optimal braking performance

  Scenario: Checking Blind Spot Detection

  Given the vehicle has Blind Spot Detection as an optional feature

  When the safety features are enabled

  And the vehicle is driven with the blind spots activated

  Then the Blind Spot Detection system should detect objects in the blind spots

  And alert the driver with visual and audible cues

  This feature file covers the basic safety rating validation, advanced safety feature verification, NHTSA compliance checks, and crash test performance validation. It can be extended further to include more scenarios and test additional safety features.