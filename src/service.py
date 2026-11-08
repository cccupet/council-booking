"""Application service: orchestrates a booking request.

Design notes
------------
* The clock is injected, so tests are deterministic and never depend on
  the real date.
* Persistence sits behind a small repository class, so the in-memory
  store can later be swapped for a database without touching the
  business rules.
* Format rules (BR1, BR2, BR4) are checked first by the validation module.
  Slot availability (BR3) depends on stored state, so it is checked here,
  where the repository is available.
* A rejected request never changes stored data (AC2, AC3).
"""
from __future__ import annotations

from datetime import date, time
from typing import Callable, List, Optional, Tuple

from src.booking import Booking, BookingRequest, BookingResult, SlotPolicy
from src.validation import validate_request

MSG_SLOT_TAKEN = "That slot is already booked. Please choose another time."


class InMemoryBookingRepository:
    """Minimal persistence layer; replaceable by a database adapter."""

    def __init__(self) -> None:
        self._items: List[Booking] = []

    def add(self, booking: Booking) -> None:
        self._items.append(booking)

    def count(self) -> int:
        return len(self._items)

    def find_by_slot(self, day: date, slot: time) -> Optional[Booking]:
        """Return the booking that occupies this slot, or None if it is free."""
        for booking in self._items:
            if booking.request.day == day and booking.request.slot == slot:
                return booking
        return None

    def all(self) -> Tuple[Booking, ...]:
        return tuple(self._items)


class BookingService:
    """Receives a BookingRequest and returns a BookingResult."""

    REFERENCE_PREFIX = "CT"

    def __init__(
        self,
        policy: SlotPolicy,
        repository: InMemoryBookingRepository,
        clock: Callable[[], date],
    ) -> None:
        self._policy = policy
        self._repository = repository
        self._clock = clock

    def book(self, request: BookingRequest) -> BookingResult:
        errors = list(validate_request(request, self._policy, self._clock()))
        if not errors and self._repository.find_by_slot(request.day, request.slot):
            errors.append(MSG_SLOT_TAKEN)  # BR3
        if errors:
            return BookingResult(
                success=False,
                message="Booking rejected. Please correct the details and try again.",
                errors=tuple(errors),
            )
        reference = self._next_reference()
        booking = Booking(reference=reference, request=request)
        self._repository.add(booking)
        return BookingResult(
            success=True,
            message=f"Appointment confirmed. Your reference is {reference}.",
            booking=booking,
        )

    def stored_count(self) -> int:
        """Number of bookings held; used to prove rejected requests are not stored."""
        return self._repository.count()

    def stored_bookings(self) -> Tuple[Booking, ...]:
        """Read-only snapshot of all stored bookings."""
        return self._repository.all()

    def _next_reference(self) -> str:
        return f"{self.REFERENCE_PREFIX}-{self._repository.count() + 1:04d}"
