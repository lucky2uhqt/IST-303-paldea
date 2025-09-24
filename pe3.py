"""
pe3.py — Pair Exercise #3: Functions and Classes

Partner(s): <PUT YOUR NAMES HERE>
Course Repo: 303_Fall_25

Implements:
- encode(input_text, shift) -> (alphabet_list, encoded_text)
- decode(input_text, shift) -> decoded_text
- BankAccount, SavingsAccount, CheckingAccount classes
"""

import datetime
import string
from typing import List, Tuple

# ---------- Functions ----------

def _shift_char_lower(c: str, shift: int) -> str:
    """Shift a single alphabetic character to lowercase by `shift` within a-z."""
    if c.isalpha():
        # Always work in lowercase per examples/tests
        base = 'a'
        idx = ord(c.lower()) - ord(base)
        shifted = (idx + (shift % 26)) % 26
        return chr(ord(base) + shifted)
    return c

def encode(input_text: str, shift: int) -> Tuple[List[str], str]:
    """
    Return (list_of_lowercase_letters, encoded_text).
    Non-letters are left unchanged. Letters become lowercase in output.
    """
    alphabet_list = list(string.ascii_lowercase)
    encoded_chars = [_shift_char_lower(c, shift) for c in input_text]
    return (alphabet_list, ''.join(encoded_chars))

def decode(input_text: str, shift: int) -> str:
    """
    Return decoded text by shifting letters backwards.
    Output is lowercase for letters, matching encode behavior.
    """
    decoded_chars = [_shift_char_lower(c, -shift) for c in input_text]
    return ''.join(decoded_chars)


# ---------- Classes ----------

class BankAccount:
    """
    Base bank account.
    Attributes:
        name: owner's name (default "Rainy")
        ID: alphanumeric id (default "1234")
        creation_date: datetime.date of account creation (default today)
        balance: numeric balance (default 0)
    Rules:
        - creation_date cannot be in the future -> raise Exception
        - negative deposit amounts are not allowed (ignored)
        - deposit/withdraw should display (print) resulting balance
    """
    def __init__(self, name: str = "Rainy", ID="1234",
                 creation_date: datetime.date = None, balance: float = 0):
        if creation_date is None:
            creation_date = datetime.date.today()
        # Ensure date type and not future
        if not isinstance(creation_date, datetime.date):
            raise Exception("creation_date must be datetime.date")
        if creation_date > datetime.date.today():
            raise Exception("creation_date cannot be in the future")
        self.name = name
        self.ID = ID
        self.creation_date = creation_date
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Deposit a positive amount; ignore non-positive amounts."""
        if amount is None or amount <= 0:
            # Not allowed per spec; do nothing (could print a message)
            print(f"Deposit ignored. Balance: {self.balance}")
            return
        self.balance += amount
        print(f"Balance after deposit: {self.balance}")

    def withdraw(self, amount: float) -> None:
        """Withdraw a positive amount; ignore non-positive amounts."""
        if amount is None or amount <= 0:
            print(f"Withdrawal ignored. Balance: {self.balance}")
            return
        self.balance -= amount
        print(f"Balance after withdrawal: {self.balance}")

    def view_balance(self):
        """Return the current balance (and also print it)."""
        print(f"Current balance: {self.balance}")
        return self.balance


class SavingsAccount(BankAccount):
    """
    SavingsAccount:
        - Withdrawals only permitted after account age >= 180 days
        - No overdrafts (balance cannot go below 0)
    """
    MIN_AGE_DAYS = 180

    def withdraw(self, amount: float) -> None:
        if amount is None or amount <= 0:
            print(f"Withdrawal ignored. Balance: {self.balance}")
            return
        today = datetime.date.today()
        age_days = (today - self.creation_date).days
        if age_days < self.MIN_AGE_DAYS:
            # Not permitted yet
            print(f"Withdrawal denied (account age {age_days} days < {self.MIN_AGE_DAYS}). Balance: {self.balance}")
            return
        if self.balance - amount < 0:
            # Overdrafts not permitted
            print(f"Withdrawal denied (insufficient funds). Balance: {self.balance}")
            return
        self.balance -= amount
        print(f"Balance after withdrawal: {self.balance}")


class CheckingAccount(BankAccount):
    """
    CheckingAccount:
        - Overdrafts permitted, but incur a $30 fee each time a withdrawal results in a negative balance.
    """
    OVERDRAFT_FEE = 30

    def withdraw(self, amount: float) -> None:
        if amount is None or amount <= 0:
            print(f"Withdrawal ignored. Balance: {self.balance}")
            return
        # Apply withdrawal
        self.balance -= amount
        # If this withdrawal results in a negative balance, charge fee
        if self.balance < 0:
            self.balance -= self.OVERDRAFT_FEE
        print(f"Balance after withdrawal: {self.balance}")
