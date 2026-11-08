"""Validation rules for booking requests (BR1, BR2, BR4).

Design notes
------------
* Pure functions: no state, no I/O, so each rule is easy to test alone.
* All violations are collected and returned together, so a resident sees
  every problem in one go instead of fixing them one at a time.
* Messages are plain-language and specific (WCAG 2.2 SC 3.3.1).
"""
from __future__ import annotations

import re
from datetime import date, time
from typing import Tuple

from src.booking import BookingRequest, SlotPolicy

UK_POSTCODE = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$")

MSG_POSTCODE = "Please enter a valid UK postcode."
MSG_FUTURE_DATE = "Appointments must be booked for a future date."
MSG_WEEKDAY = "Appointments are only available on weekdays."
MSG_HOURS = "Appointments are available from 09:00 to 16:30."


def _minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def is_valid_postcode(postcode: str) -> bool:
    """BR4: UK postcode format, case-insensitive, surrounding spaces ignored."""
    return bool(UK_POSTCODE.match(postcode.strip().upper()))


def is_future_date(day: date, today: date) -> bool:
    """BR2: the appointment must be after today."""
    return day > today


def is_weekday(day: date) -> bool:
    """BR1 (part 1): Monday to Friday only."""
    return day.weekday() < 5


def is_valid_slot(slot: time, policy: SlotPolicy) -> bool:
    """BR1 (part 2): inside opening hours and aligned to the slot length."""
    start, end, current = (
        _minutes(policy.first_slot),
        _minutes(policy.last_slot),
        _minutes(slot),
    )
    return start <= current <= end and (current - start) % policy.slot_minutes == 0


def validate_request(
    request: BookingRequest, policy: SlotPolicy, today: date
) -> Tuple[str, ...]:
    """Return every rule violation as a tuple of messages (empty = valid)."""
    errors = []
    if not is_valid_postcode(request.postcode):
        errors.append(MSG_POSTCODE)
    if not is_future_date(request.day, today):
        errors.append(MSG_FUTURE_DATE)
    if not is_weekday(request.day):
        errors.append(MSG_WEEKDAY)
    if not is_valid_slot(request.slot, policy):
        errors.append(MSG_HOURS)
    return tuple(errors)
