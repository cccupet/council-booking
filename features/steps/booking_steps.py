"""Step definitions binding the Gherkin scenarios to the booking service.

Each decorated function matches one line of the .feature file; the text in
quotes inside the step becomes a function argument.
"""
from datetime import datetime

from behave import given, then, when

from src.booking import BookingRequest, EnquiryType, SlotPolicy
from src.service import BookingService, InMemoryBookingRepository


def to_date(text):
    return datetime.strptime(text, "%d-%m-%Y").date()


def to_time(text):
    return datetime.strptime(text, "%H:%M").time()


# ---- Background -------------------------------------------------------------

@given('the service offers {minutes:d}-minute slots from "{first}" to "{last}" on weekdays')
def step_policy(context, minutes, first, last):
    context.policy = SlotPolicy(
        slot_minutes=minutes,
        first_slot=to_time(first),
        last_slot=to_time(last),
        weekdays_only=True,
    )


@given('today is "{today}"')
def step_today(context, today):
    fixed_today = to_date(today)
    context.service = BookingService(
        policy=context.policy,
        repository=InMemoryBookingRepository(),
        clock=lambda: fixed_today,
    )


# ---- Scenario steps ---------------------------------------------------------

@given('the resident "{name}" with postcode "{postcode}"')
def step_resident(context, name, postcode):
    context.name = name
    context.postcode = postcode


@when('the resident books a "{enquiry}" appointment on "{day}" at "{slot}"')
def step_book(context, enquiry, day, slot):
    request = BookingRequest(
        name=context.name,
        postcode=context.postcode,
        enquiry_type=EnquiryType(enquiry),
        day=to_date(day),
        slot=to_time(slot),
    )
    context.result = context.service.book(request)


@then("the booking is confirmed")
def step_confirmed(context):
    assert context.result.success, f"Expected success, got: {context.result.message}"


@then("the resident receives a booking reference")
def step_reference(context):
    booking = context.result.booking
    assert booking is not None, "No booking was returned"
    assert booking.reference.startswith("CT-"), f"Unexpected reference: {booking.reference}"


# ---- AC2: rejection steps ---------------------------------------------------

@then("the booking is rejected")
def step_rejected(context):
    assert not context.result.success, "Expected the booking to be rejected"
    assert context.result.booking is None, "A rejected request must not return a booking"


@then('the resident is told "{message}"')
def step_told(context, message):
    assert message in context.result.errors, (
        f"Expected message {message!r}, got {context.result.errors!r}"
    )


@then("no booking is stored")
def step_nothing_stored(context):
    assert context.service.stored_count() == 0, "A rejected request must not be stored"
