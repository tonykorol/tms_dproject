from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from config import SECRET
from database.database import get_user_db
from database.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    UserManager class that handles user-related operations.

    Inherits from IntegerIDMixin and BaseUserManager to manage users with integer IDs.
    """

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Callback function that is called after a user registers.

        :param user: The registered user instance.
        :param request: The request object, if available.
        """
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Dependency function to get an instance of UserManager.

    :param user_db: The user database dependency injected by FastAPI.

    :yield: UserManager: An instance of UserManager initialized with the user database.
    """
    yield UserManager(user_db)
