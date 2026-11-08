"""Application service: orchestrates a booking request.

Design notes
------------
* The clock is injected, so tests are deterministic and never depend on
  the real date.
* Persistence sits behind a small repository class, so the in-memory
  store can later be swapped for a database without touching the
  business rules.
* Validation runs before anything is stored, so a rejected request leaves
  no trace (AC2).
"""
from __future__ import annotations

from datetime import date
from typing import Callable, List

from src.booking import Booking, BookingRequest, BookingResult, SlotPolicy
from src.validation import validate_request


class InMemoryBookingRepository:
    """Minimal persistence layer; replaceable by a database adapter."""

    def __init__(self) -> None:
        self._items: List[Booking] = []

    def add(self, booking: Booking) -> None:
        self._items.append(booking)

    def count(self) -> int:
        return len(self._items)


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
        errors = validate_request(request, self._policy, self._clock())
        if errors:
            return BookingResult(
                success=False,
                message="Booking rejected. Please correct the details and try again.",
                errors=errors,
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

    def _next_reference(self) -> str:
        return f"{self.REFERENCE_PREFIX}-{self._repository.count() + 1:04d}"
