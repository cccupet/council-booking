# US-001: Online booking of council tax enquiry appointments

| Field                  | Value                                |
|------------------------|--------------------------------------|
| Epic                   | Resident self-service                |
| Primary stakeholder    | Resident of the borough              |
| Secondary stakeholders | Council tax adviser; service manager |
| Priority (MoSCoW)      | Must have                            |

## Problem statement
Residents currently phone or queue in person to reach a council tax adviser.
This is slow, limited to office hours and gives the service no visibility of
demand. An online booking channel removes the queue and lets advisers plan
their day.

## User story
As a resident, I want to book a council tax appointment online, so that I can
speak to an adviser at a time that suits me without queuing.

## Business rules
- BR1: Appointments are offered on weekdays only, in 30-minute slots from
  09:00 to 16:30.
- BR2: An appointment must be booked for a date after today.
- BR3: A slot can hold at most one booking.
- BR4: The postcode must follow the UK postcode format.

## Acceptance criteria and traceability
| ID  | Criterion                                                                          | Rules       | Scenario                         |
|-----|------------------------------------------------------------------------------------|-------------|----------------------------------|
| AC1 | Valid details and a free slot produce a confirmed booking with a unique reference  | BR1-BR4     | Resident books an available slot |
| AC2 | Invalid input is rejected with a specific message; nothing is stored               | BR1,BR2,BR4 | Invalid requests are rejected    |
| AC3 | An already booked slot is refused; the first booking is unchanged                  | BR3         | Double booking is prevented      |

## Non-functional constraints
- Data minimisation (UK GDPR Art. 5(1)(c)): only name, postcode, enquiry type
  and slot are held.
- Error messages are specific and in plain language, supporting WCAG 2.2
  success criterion 3.3.1 (Error Identification).
