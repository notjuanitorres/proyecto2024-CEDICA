from abc import abstractmethod
from typing import List, Dict
from src.core.database import db as database
from src.core.module.common.repositories import (
    apply_filters,
    apply_multiple_search_criteria,
)
from .models import ProfilePhoto, User
from .mappers import UserMapper
from sqlalchemy import and_


class AbstractUserRepository:
    """
    Abstract base class for user repositories.

    This class defines the interface for user repositories, including methods
    for adding, retrieving, updating, archiving, deleting, and recovering users,
    as well as toggling activation status and checking system administrator status.
    """
    def __init__(self):
        self.storage_path = "users/"

    @abstractmethod
    def add(self, user: User) -> User | None:
        """
        Add a new user to the repository.

        Args:
            user (User): The user to add.

        Returns:
            User | None: The added user, or None if the operation failed.
        """
        pass

    @abstractmethod
    def get_page(
        self,
        page: int,
        per_page: int,
        max_per_page: int,
        search_query: Dict = None,
        order_by: list = None,
    ):
        """
        Retrieve a paginated list of users.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of users per page.
            max_per_page (int): The maximum number of users per page.
            search_query (Dict, optional): The search query to filter users.
            order_by (list, optional): The order by criteria.

        Returns:
            A paginated list of users.
        """
        pass

    @abstractmethod
    def get_active_users(self, page: int, search: str = ""):
        """
        Retrieve a paginated list of active users.

        Args:
            page (int): The page number to retrieve.

        Returns:
            A paginated list of active users.
        """
        pass
    @abstractmethod
    def get_profile_image_url(self, user_id: int) -> str | None:
        pass
    @abstractmethod
    def get_user(self, user_id: int) -> Dict | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Dict | None: The user data as a dictionary, or None if the user does not exist.
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User | None: The user, or None if the user does not exist.
        """
        pass

    @abstractmethod
    def update(self, user_id: int, data: Dict) -> None:
        """
        Update a user's information.

        Args:
            user_id (int): The ID of the user to update.
            data (Dict): The updated user data.

        Returns:
            None
        """
        pass

    @abstractmethod
    def archive(self, user_id: int) -> bool:
        """
        Archive a user.

        Args:
            user_id (int): The ID of the user to archive.

        Returns:
            bool: True if the user was archived successfully, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def recover(self, user_id: int) -> bool:
        """
        Recover an archived user.

        Args:
            user_id (int): The ID of the user to recover.

        Returns:
            bool: True if the user was recovered successfully, False otherwise.
        """
        pass

    @abstractmethod
    def toggle_activation(self, user_id: int) -> None:
        """
        Toggle the activation status of a user.

        Args:
            user_id (int): The ID of the user to toggle activation status.

        Returns:
            None
        """
        pass

    @abstractmethod
    def is_sys_admin(self, user_id: int) -> bool:
        """
        Check if a user is a system administrator.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is a system administrator, False otherwise.
        """
        pass

    @abstractmethod
    def is_user_enabled(self, user_id: int) -> bool:
        """
        Check if a user is enabled.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is enabled, False otherwise.
        """
        pass

    @abstractmethod
    def can_be_linked(self, email: str) -> int | None:
        """
        Check if a user can be linked by their email address.

        Args:
            email (str): The email address to check.

        Returns:
            int | None: The user ID if the user can be linked, None otherwise.
        """
        pass

    @abstractmethod
    def change_profile_photo(self, user_id: int, profile_photo_id: int) -> bool:
        """
        Changes the profile photo of a user.
        Args:
            user_id (int): The ID of the user.
            profile_photo_id (int): The ID of the profile photo.
        Returns: 
            bool: True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_profile_photo_url(self, profile_photo_id: int) -> str:
        """
        Returns the URL of the profile photo based on the ID.

        Args:
            profile_photo_id (int): The ID of the profile photo.

        Returns:
            str: The URL of the profile photo.
        """
    @abstractmethod
    def save_new_photo(self, profile_photo_url: str) -> int:
        """
        Saves a new profile photo and returns its ID.

        Args:
            profile_photo_url (str): The URL of the new profile photo.

        Returns:
            int: The ID of the newly created profile photo.
        """
        pass

class UserRepository(AbstractUserRepository):
    """
    Concrete implementation of the AbstractUserRepository.

    This class provides methods for adding, retrieving, updating, archiving, deleting,
    and recovering users, as well as toggling activation status and checking system
    administrator status.
    """

    def __init__(self):
        """
        Initialize the UserRepository.
        """
        super().__init__()
        self.db = database

    def add(self, user: User):
        """
        Add a new user to the repository.

        Args:
            user (User): The user to add.

        Returns:
            User: The added user.
        """
        self.db.session.add(user)
        self.db.session.flush()
        self.save()

        return UserMapper.from_entity(user)

    def get_page(
        self,
        page: int = 1,
        per_page: int = 10,
        max_per_page: int = 30,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """
        Retrieve a paginated list of users.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of users per page.
            max_per_page (int): The maximum number of users per page.
            search_query (Dict, optional): The search query to filter users.
            order_by (List, optional): The order by criteria.

        Returns:
            A paginated list of users.
        """
        query = User.query

        query = apply_filters(User, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_active_users(self, page: int = 1, search: str = ""):
        """
        Retrieve a paginated list of active users.

        Args:
            page (int): The page number to retrieve.
            search (str, optional): The search query to filter users.

        Returns:
            A paginated list of active users.
        """
        per_page = 7

        query = self.db.session.query(User).filter(
            and_(User.enabled == True, User.employee == None)
        )

        if search:
            search_fields = ["alias", "email"]
            query = apply_multiple_search_criteria(
                User, query, search_query={"text": search, "fields": search_fields}
            )

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The user, or None if the user does not exist.
        """
        return self.db.session.query(User).filter(User.id == user_id).first()

    def get_user(self, user_id: int) -> Dict | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Dict | None: The user data as a dictionary, or None if the user does not exist.
        """
        user = self.get_by_id(user_id)
        if not user:
            return None     
        return UserMapper.from_entity(user)
    def get_profile_image_url(self, user_id: int) -> str | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        return user.profile_image.url if user.profile_image else None
    
    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User | None: The user, or None if the user does not exist.
        """
        return self.db.session.query(User).filter(User.email == email).first()

    def update(self, user_id: int, data: Dict):
        """
        Update a user's information.

        Args:
            user_id (int): The ID of the user to update.
            data (Dict): The updated user data.

        Returns:
            bool: True if the user was updated successfully, False otherwise.
        """
        user = User.query.filter_by(id=user_id)
        if not user:
            return False
        if data["profile_image_url"]!= None:
            self.change_profile_photo(user_id, data["profile_image_url"]) 
        data.pop("profile_image_url")
        user.update(data)
        self.save()
        return True

    def delete(self, user_id):
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        user = User.query.get(user_id)
        if not user:
            return False
        self.db.session.delete(user)
        self.save()
        return True
    
    def archive(self, user_id):
        """
        Archive a user.

        Args:
            user_id (int): The ID of the user to archive.

        Returns:
            bool: True if the user was archived successfully, False otherwise.
        """
        user = User.query.get(user_id)
        if not user or user.system_admin or user.is_deleted:
            return False
        user.is_deleted = True
        user.enabled = False
        self.save()
        return True
    
    def recover(self, user_id):
        """
        Recover an archived user.

        Args:
            user_id (int): The ID of the user to recover.

        Returns:
            bool: True if the user was recovered successfully, False otherwise.
        """
        user = User.query.get(user_id)
        if not user or not user.is_deleted:
            return False
        user.is_deleted = False
        user.enabled = True
        self.save()
        return True

    def toggle_activation(self, user_id: int) -> bool:
        """
        Toggle the activation status of a user.

        Args:
            user_id (int): The ID of the user to toggle activation status.

        Returns:
            bool: True if the activation status was toggled successfully, False otherwise.
        """
        if self.is_sys_admin(user_id):
            return False
        user = self.get_by_id(user_id)
        user.enabled = not user.enabled
        self.save()
        return True

    def is_sys_admin(self, user_id: int) -> bool:
        """
        Check if a user is a system administrator.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is a system administrator, False otherwise.
        """
        if not user_id:
            return False
        user = self.get_by_id(user_id)
        return user.system_admin

    def is_user_enabled(self, user_id: int) -> bool:
        """
        Check if a user is enabled.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is enabled, False otherwise.
        """
        if not user_id:
            return False
        user = self.get_by_id(user_id)
        return user.enabled

    def save(self):
        """
        Commit the current transaction to the database.

        Returns:
            None
        """
        self.db.session.commit()

    def can_be_linked(self, email: str) -> int | None:
        """
        Check if a user can be linked by their email address.

        Args:
            email (str): The email address to check.

        Returns:
            int | None: The user ID if the user can be linked, None otherwise.
        """
        user = self.get_by_email(email)
        if not user or user.employee:
            return None
        if user.email == email:
            return user.id

        return None
    def get_profile_photo_url(self, profile_photo_id):
        profile_photo = ProfilePhoto.query.get(profile_photo_id)
        return profile_photo.url if profile_photo else None
    

    def change_profile_photo(self, user_id: int, profile_photo_url:str) -> bool:
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            if user.profile_image_id:
                profile_photo = ProfilePhoto.query.get(user.profile_image_id)
                if profile_photo:
                    profile_photo.url = profile_photo_url
            else:
                user.profile_image_id = self.save_new_photo(profile_photo_url)
            self.save()
            return True
        except Exception:
            return False
        

    def save_new_photo(self, profile_photo_url: str) -> int:
        new_profile_photo = ProfilePhoto(url=profile_photo_url)
        self.db.session.add(new_profile_photo)
        self.db.session.flush()
        self.save()
        return new_profile_photo.id