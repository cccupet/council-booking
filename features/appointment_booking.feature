@US-001
Feature: Book a council tax appointment
  As a resident of the borough
  I want to book a council tax appointment online
  So that I can speak to an adviser without queuing or phoning

  Background:
    Given the service offers 30-minute slots from "09:00" to "16:30" on weekdays
    And today is "2026-11-09"

  @AC1 @happy-path
  Scenario: Resident books an available slot
    Given the resident "Sam Taylor" with postcode "SW1A 1AA"
    When the resident books a "council tax" appointment on "2026-11-10" at "10:00"
    Then the booking is confirmed
    And the resident receives a booking reference
