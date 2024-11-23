from abc import abstractmethod
from typing import List, Dict
from datetime import date
from sqlalchemy import func
from src.core.module.employee.models import Employee
from src.core.database import db as database
from src.core.module.charges.models import Charge
from src.core.module.common.repositories import apply_filters, apply_search_criteria
from .mappers import ChargeMapper as Mapper


class AbstractChargeRepository:
    """
    Abstract base class for charge repositories.

    This class defines the interface for charge repositories, including methods
    for adding, retrieving, updating, archiving, deleting, and recovering charges.
    """

    @abstractmethod
    def add_charge(self, charge: Charge) -> Dict:
        """
        Add a new charge to the repository.

        Args:
            charge (Charge): The charge to add.

        Returns:
            Dict: The added charge as a dictionary.
        """
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: list = None,
    ):
        """
        Retrieve a paginated list of charges.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of charges per page.
            search_query (Dict, optional): The search query to filter charges.
            order_by (list, optional): The order by criteria.

        Returns:
            A paginated list of charges.
        """
        pass

    @abstractmethod
    def get_by_id(self, charge_id: int) -> Dict | None:
        """
        Retrieve a charge by its ID.

        Args:
            charge_id (int): The ID of the charge to retrieve.

        Returns:
            Dict | None: The charge data as a dictionary, or None if the charge does not exist.
        """
        pass

    @abstractmethod
    def update_charge(self, charge_id: int, data: Dict) -> bool:
        """
        Update a charge's information.

        Args:
            charge_id (int): The ID of the charge to update.
            data (Dict): The updated charge data.

        Returns:
            bool: True if the charge was updated successfully, False otherwise.
        """
        pass

    @abstractmethod
    def delete_charge(self, charge_id: int) -> bool:
        """
        Delete a charge.

        Args:
            charge_id (int): The ID of the charge to delete.

        Returns:
            bool: True if the charge was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def archive_charge(self, charge_id) -> bool:
        """
        Archive a charge.

        Args:
            charge_id (int): The ID of the charge to archive.

        Returns:
            bool: True if the charge was archived successfully, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def recover_charge(self, charge_id) -> bool:
        """
        Recover an archived charge.

        Args:
            charge_id (int): The ID of the charge to recover.

        Returns:
            bool: True if the charge was recovered successfully, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def current_month_income(self) -> float:
        """
        Get the total income for the current month.

        Returns:
            float: The total income for the current month.
        """
        pass

    @abstractmethod
    def last_payments_data(self, limit: int = 10) -> List[Charge]:
        """
        Get the most recent payments.

        Args:
            limit (int): The number of recent payments to retrieve. Defaults to 10.

        Returns:
            List[Charge]: A list of the most recent payments.
        """
        pass


class ChargeRepository(AbstractChargeRepository):
    """
    Concrete implementation of the AbstractChargeRepository.

    This class provides methods for adding, retrieving, updating, archiving, deleting,
    and recovering charges.
    """

    def __init__(self):
        """
        Initialize the ChargeRepository.
        """
        self.db = database

    def add_charge(self, charge: Charge):
        """
        Add a new charge to the repository.

        Args:
            charge (Charge): The charge to add.

        Returns:
            Dict: The added charge as a dictionary.
        """
        self.db.session.add(charge)
        self.db.session.flush()
        self.save()
        return Mapper.from_entity(charge)

    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        """
        Retrieve a paginated list of charges.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of charges per page.
            search_query (Dict, optional): The search query to filter charges.
            order_by (List, optional): The order by criteria.

        Returns:
            A paginated list of charges.
        """
        max_per_page = 100

        query = Charge.query

        # since name and lastname aren't in the Charge model, we need to apply the filters separately
        if search_query and "text" in search_query and "field" in search_query:
            employee_query = apply_search_criteria(Employee, Employee.query, search_query).all()
            employee_ids = [employee.id for employee in employee_query]
            query = query.filter(Charge.employee_id.in_(employee_ids))
            search_query.pop("text")
            search_query.pop("field")

        # apply_filters doesn't handle dates so we filter it here
        if "filters" in search_query and search_query["filters"]:
            if "start_date" in search_query["filters"] and "finish_date" in search_query["filters"]:
                query = (query
                         .filter(Charge.date_of_charge
                                 .between(search_query["filters"]["start_date"],
                                          search_query["filters"]["finish_date"])))
                search_query["filters"].pop("start_date")
                search_query["filters"].pop("finish_date")

        query = apply_filters(Charge, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def __get_by_id(self, charge_id: int):
        """
        Retrieve a charge by its ID.

        Args:
            charge_id (int): The ID of the charge to retrieve.

        Returns:
            Charge: The charge entity.
        """
        return Charge.query.get(charge_id)

    def get_by_id(self, charge_id: int) -> Dict | None:
        """
        Retrieve a charge by its ID.

        Args:
            charge_id (int): The ID of the charge to retrieve.

        Returns:
            Dict | None: The charge data as a dictionary, or None if the charge does not exist.
        """
        charge = self.db.session.query(Charge).filter(Charge.id == charge_id).first()
        return Mapper.from_entity(charge) if charge else None

    def update_charge(self, charge_id: int, data: Dict) -> bool:
        """
        Update a charge's information.

        Args:
            charge_id (int): The ID of the charge to update.
            data (Dict): The updated charge data.

        Returns:
            bool: True if the charge was updated successfully, False otherwise.
        """
        charge = Charge.query.filter_by(id=charge_id)
        if not charge:
            return False
        charge.update(data)
        self.save()
        return True

    def delete_charge(self, charge_id: int) -> bool:
        """
        Delete a charge.

        Args:
            charge_id (int): The ID of the charge to delete.

        Returns:
            bool: True if the charge was deleted successfully, False otherwise.
        """
        charge = self.__get_by_id(charge_id)
        if not charge:
            return False
        self.db.session.delete(charge)
        self.save()
        return True

    def archive_charge(self, charge_id) -> bool:
        """
        Archive a charge.

        Args:
            charge_id (int): The ID of the charge to archive.

        Returns:
            bool: True if the charge was archived successfully, False otherwise.
        """
        charge = Charge.query.get(charge_id)
        if not charge or charge.is_archived:
            return False
        charge.is_archived = True
        self.save()
        return True

    def recover_charge(self, charge_id) -> bool:
        """
        Recover an archived charge.

        Args:
            charge_id (int): The ID of the charge to recover.

        Returns:
            bool: True if the charge was recovered successfully, False otherwise.
        """
        charge = Charge.query.get(charge_id)
        if not charge or not charge.is_archived:
            return False
        charge.is_archived = False
        self.save()
        return True

    def save(self):
        """
        Commit the current transaction to the database.

        Returns:
            None
        """
        self.db.session.commit()

    def current_month_income(self) -> float:
        """
        Get the total income for the current month.

        Returns:
            float: The total income for the current month.
        """
        return (Charge.query.filter(
            func.extract('year', Charge.date_of_charge) == date.today().year,
            func.extract('month', Charge.date_of_charge) == date.today().month
        )
                .with_entities(func.sum(Charge.amount)).scalar() or 0.0)

    def last_payments_data(self, limit: int = 10) -> List[Charge]:
        """
        Get the most recent payments.

        Args:
            limit (int): The number of recent payments to retrieve. Defaults to 10.

        Returns:
            List[Charge]: A list of the most recent payments.
        """
        return Charge.query.order_by(Charge.date_of_charge.desc()).limit(limit).all()


