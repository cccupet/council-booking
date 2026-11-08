# Council Tax Appointment Booking (SWE6301 prototype)

A small Python prototype that lets a resident book a council tax enquiry
appointment. Behaviour is specified with Behaviour-Driven Development (BDD)
using Gherkin scenarios and the behave framework.

## Structure

| Path | Purpose |
|------|---------|
| docs/user_story.md | User story, business rules (BR1-BR4), acceptance criteria (AC1-AC3) and traceability |
| features/appointment_booking.feature | Executable specification in Given-When-Then (Gherkin) |
| features/steps/booking_steps.py | Step definitions linking Gherkin to the source code |
| src/booking.py | Immutable domain model (booking, request, result, slot policy) |
| src/validation.py | Validation rules BR1, BR2, BR4 |
| src/service.py | Booking service and in-memory repository (BR3) |

## Run the tests (macOS / Linux)

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    behave

## Scenarios

- AC1: A resident books an available slot and receives a booking reference.
- AC2: Invalid requests (postcode, past date, weekend, outside hours) are
  rejected with a specific message; nothing is stored.
- AC3: Double booking is prevented and the original booking is unchanged.

Dates use the UK format DD-MM-YYYY. The service receives "today" from the
scenario, so results are the same on every run.
