@US-001
Feature: Book a council tax appointment
  As a resident of the borough
  I want to book a council tax appointment online
  So that I can speak to an adviser without queuing or phoning

  Background:
    Given the service offers 30-minute slots from "09:00" to "16:30" on weekdays
    And today is "09-11-2026"

  @AC1 @happy-path
  Scenario: Resident books an available slot
    Given the resident "Sam Taylor" with postcode "SW1A 1AA"
    When the resident books a "council tax" appointment on "10-11-2026" at "10:00"
    Then the booking is confirmed
    And the resident receives a booking reference

  @AC2 @validation
  Scenario Outline: Invalid requests are rejected with a specific message
    Given the resident "Sam Taylor" with postcode "<postcode>"
    When the resident books a "council tax" appointment on "<day>" at "<slot>"
    Then the booking is rejected
    And the resident is told "<message>"
    And no booking is stored

    Examples: Business rule violations
      | rule | postcode | day        | slot  | message                                         |
      | BR4  | 12345    | 10-11-2026 | 10:00 | Please enter a valid UK postcode.               |
      | BR2  | SW1A 1AA | 09-11-2026 | 10:00 | Appointments must be booked for a future date.  |
      | BR1  | SW1A 1AA | 14-11-2026 | 10:00 | Appointments are only available on weekdays.    |
      | BR1  | SW1A 1AA | 10-11-2026 | 08:00 | Appointments are available from 09:00 to 16:30. |

  @AC3 @alternative-flow
  Scenario: Double booking is prevented
    Given the resident "Sam Taylor" with postcode "SW1A 1AA"
    And the slot "10-11-2026" at "10:00" is already booked by "Jordan Lee"
    When the resident books a "council tax" appointment on "10-11-2026" at "10:00"
    Then the booking is rejected
    And the resident is told "That slot is already booked. Please choose another time."
    And the original booking is unchanged
