from abc import abstractmethod
from operator import and_
from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from src.core.database import db as database
from src.core.module.payment.models import Payment
from src.core.module.common.repositories import apply_filters


class AbstractPaymentRepository:
    @abstractmethod
    def add(self, payment: Payment) -> Payment | None:
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
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def update(self, payment_id: int, data: Dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, payment_id: int) -> bool:
        raise NotImplementedError


class PaymentRepository(AbstractPaymentRepository):
    def __init__(self):
        self.db: SQLAlchemy = database

    def save(self):
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
        max_per_page: int,
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
                query = query.filter(Payment.is_archived==search_query["is_archived"])

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

    def archive_payment(self, payment_id):
        payment = Payment.query.filter_by(id=payment_id).first()
        if payment:
            payment.is_archived = True
            self.save()
        return payment

    def unarchive_payment(self, payment_id):
        payment = Payment.query.filter_by(id=payment_id).first()
        if payment:
            payment.is_archived = False
            self.payment_repository.update(payment)
            self.save()
        return payment

    def delete(self, payment_id: int) -> bool:
        payment = Payment.query.filter_by(id=payment_id).first()
        if not payment:
            return False
        self.db.session.delete(payment)
        self.save()
        return True