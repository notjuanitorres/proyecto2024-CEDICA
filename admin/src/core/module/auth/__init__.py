"""
__init__.py

This module initializes the auth package by importing and exposing key components
such as repositories, services, forms, and enums. These components are used for managing
authentication and authorization, including user login, registration, and role-based access control.

Exposed Components:
    - AbstractAuthRepository: The abstract base class for authentication repositories.
    - AuthRepository: The concrete implementation of the authentication repository.
    - AbstractAuthServices: The abstract base class for authentication services.
    - AuthServices: The concrete implementation of the authentication services.
    - UserLoginForm: The form for user login.
    - UserRegisterForm: The form for user registration.
    - RoleEnum: The enumeration for user roles.
    - PermissionEnum: The enumeration for user permissions.
"""

from .repositories import AbstractAuthRepository, AuthRepository
from .services import AbstractAuthServices, AuthServices
from .forms import UserLoginForm, UserRegisterForm
from .data import RoleEnum, PermissionEnum

__all__ = [
    "AbstractAuthRepository",
    "AuthRepository",
    "AbstractAuthServices",
    "AuthServices",
    "UserLoginForm",
    "UserRegisterForm",
    "RoleEnum",
    "PermissionEnum"
]