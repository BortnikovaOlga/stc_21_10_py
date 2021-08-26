from enum import Enum


class Status(Enum):
    not_accepted = "not_accepted"
    in_progress = "in_progress"
    cancelled = "cancelled"
    done = "done"


class Transaction:
    transitions = {
        Status.not_accepted: (Status.in_progress, Status.cancelled),
        Status.in_progress: (Status.cancelled, Status.done)
    }

    @classmethod
    def is_valid(cls, status_old, status_new: Status) -> bool:
        return status_new in cls.transitions[status_old]

"""
st1 = Status.not_accepted
st2 = Status.in_progress
print(Transaction.is_valid_transaction(st1, st2))"""
