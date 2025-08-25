from enum import Enum


class RecurrenceType(str,Enum):
  DAILY = 'daily'
  WEEKLY = 'weekly'
  MONTHLY = 'monthly'
  YEARLY = 'yearly'
  CUSTOM = 'custom'