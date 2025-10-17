from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from app.models.appointment_reminder import AppointmentReminder

class IAppointmentReminderService(ABC):
    @abstractmethod
    def create(self, *, user_id: int, clinic_id: int, specialty_id: int,
               doctor_id: int, starts_at: datetime, notes: str | None) -> AppointmentReminder:
        pass

    @abstractmethod
    def list_upcoming(self, *, user_id: int, now: datetime) -> List[AppointmentReminder]:
        pass

    @abstractmethod
    def list_overdue(self, *, user_id: int, now: datetime) -> List[AppointmentReminder]:
        pass

    @abstractmethod
    def set_status(self, *, user_id: int, reminder_id: int, status: str) -> AppointmentReminder:
        pass

    @abstractmethod
    def delete(self, *, user_id: int, reminder_id: int) -> None:
        pass
