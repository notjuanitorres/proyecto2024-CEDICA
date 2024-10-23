from abc import abstractmethod
from operator import and_
from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from src.core.database import db as database
from src.core.module.payment.models import Payment
from src.core.module.common.repositories import apply_filters


class AbstractPaymentRepository:
    """
    Abstract interface for the payment repository.

    Methods:
        add(payment: Payment) -> Payment | None:
            Adds a new payment to the repository.

        get_page(page: int, per_page: int, max_per_page: int, search_query: Dict = None, order_by: list = None) -> Pagination:
            Retrieves a page of payments based on search and order parameters.

        get_by_id(payment_id: int) -> Payment:
            Retrieves a payment by its ID.

        update(payment_id: int, data: Dict) -> bool:
            Updates an existing payment with the provided data.

        delete(payment_id: int) -> bool:
            Deletes a payment by its ID.
    """
    @abstractmethod
    def add(self, payment: Payment) -> Payment | None:
        """
        Adds a new payment to the repository.

        Args:
            payment (Payment): The payment instance to add.

        Returns:
            Payment | None: The added payment instance or None if the addition failed.
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
    ) -> Pagination:
        """
        Retrieves a page of payments based on search and order parameters.

        Args:
            page (int): The page number.
            per_page (int): The number of items per page.
            max_per_page (int): The maximum number of items per page.
            search_query (Dict, optional): The search parameters.
            order_by (list, optional): The order parameters.

        Returns:
            Pagination: A pagination instance with the results.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Payment:
        """
        Retrieves a payment by its ID.

        Args:
            payment_id (int): The ID of the payment.

        Returns:
            Payment: The retrieved payment instance.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, payment_id: int, data: Dict) -> bool:
        """
        Updates an existing payment with the provided data.

        Args:
            payment_id (int): The ID of the payment to update.
            data (Dict): The data to update in the payment.

        Returns:
            bool: True if the payment was successfully updated, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, payment_id: int) -> bool:
        """
        Deletes a payment by its ID.

        Args:
            payment_id (int): The ID of the payment to delete.

        Returns:
            bool: True if the payment was successfully deleted, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def archive_payment(self, payment_id) -> bool:
        """
        Archives a payment by its ID.

        Args:
            payment_id (int): The ID of the payment to archive.

        Returns:
            bool: True if the payment was successfully archived, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def unarchive_payment(self, payment_id) -> bool:
        """
        Unarchives a payment by its ID.

        Args:
            payment_id (int): The ID of the payment to unarchive.

        Returns:
            bool: True if the payment was successfully unarchived, False otherwise.
        """
        raise NotImplementedError


class PaymentRepository(AbstractPaymentRepository):
    """
    Concrete implementation of the payment repository using SQLAlchemy.

    Methods:
        __init__():
            Initializes the payment repository.

        save():
            Commits the changes to the database.

        add(payment: Payment) -> Payment:
            Adds a new payment to the repository and commits it to the database.

        get_page(page: int, per_page: int, max_per_page: int, search_query: Dict = None, order_by: List = None) -> Pagination:
            Retrieves a page of payments based on search and order parameters.

        get_by_id(payment_id: int) -> Payment:
            Retrieves a payment by its ID.

        update(payment_id: int, data: Dict) -> bool:
            Updates an existing payment with the provided data.

        archive_payment(payment_id: int) -> Payment:
            Archives a payment by its ID.

        unarchive_payment(payment_id: int) -> Payment:
            Unarchives a payment by its ID.

        delete(payment_id: int) -> bool:
            Deletes a payment by its ID.
    """
    def __init__(self):
        self.db: SQLAlchemy = database

    def save(self):
        """
        Commits the changes to the database.
        """
        self.db.session.commit()

    def add(self, payment: Payment):
        self.db.session.add(payment)
        self.db.session.flush()
        self.save()

        return payment

    def get_page(
        self,
        page: int,
        per_page: int,
        search_query: Dict = None,
        order_by: List = None,
    ):
        query = Payment.query

        # Aplicar filtros
        if search_query:
            if "payment_date__gte" in search_query:
                query = query.filter(Payment.payment_date >= search_query["payment_date__gte"])
            if "payment_date__lte" in search_query:
                query = query.filter(Payment.payment_date <= search_query["payment_date__lte"])
            if "payment_type" in search_query:
                query = query.filter(Payment.payment_type == search_query["payment_type"])
            if "is_archived" in search_query:
                query = query.filter(Payment.is_archived == search_query["is_archived"])

        # Aplicar orden
        if order_by:
            for order in order_by:
                column, direction = order
                query = query.order_by(getattr(getattr(Payment, column), direction)())

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, payment_id: int) -> Payment:
        return (
            self.db.session.query(Payment).filter(Payment.id == payment_id).first()
        )

    def update(self, payment_id: int, data: Dict) -> bool:
        payment = Payment.query.filter_by(id=payment_id)
        if not payment:
            return False
        payment.update(data)
        self.save()
        return True

    def archive_payment(self, payment_id) -> bool:
        payment = Payment.query.get(payment_id)
        if not payment or payment.is_archived:
            return False
        payment.is_archived = True
        self.save()
        return True

    def unarchive_payment(self, payment_id) -> bool:
        payment = Payment.query.get(payment_id)
        if not payment or not payment.is_archived:
            return False
        payment.is_archived = False
        self.save()
        return True

    def delete(self, payment_id: int) -> bool:
        payment = Payment.query.filter_by(id=payment_id).first()
        if not payment:
            return False
        self.db.session.delete(payment)
        self.save()
        return True
