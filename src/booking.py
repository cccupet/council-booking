"""Domain model for the council tax appointment booking service.

Design notes
------------
* Value objects are immutable (frozen dataclasses), so a stored booking
  cannot be altered by accident.
* Opening rules (BR1) live in a SlotPolicy object rather than being
  hard-coded inside the service.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from typing import Optional, Tuple


class EnquiryType(Enum):
    """Kinds of enquiry a resident can book; extend here for new services."""
    COUNCIL_TAX = "council tax"


@dataclass(frozen=True)
class SlotPolicy:
    """Opening rules for appointment slots (BR1)."""
    slot_minutes: int
    first_slot: time
    last_slot: time
    weekdays_only: bool = True


@dataclass(frozen=True)
class BookingRequest:
    """What the resident submits: the input to the service."""
    name: str
    postcode: str
    enquiry_type: EnquiryType
    day: date
    slot: time


@dataclass(frozen=True)
class Booking:
    """A confirmed appointment, identified by a unique reference."""
    reference: str
    request: BookingRequest


@dataclass(frozen=True)
class BookingResult:
    """What the service returns: success flag, message and any errors."""
    success: bool
    message: str
    errors: Tuple[str, ...] = ()
    booking: Optional[Booking] = None
