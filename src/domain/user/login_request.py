
from dataclasses import dataclass
from typing import Optional

class LoginRequest:
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None