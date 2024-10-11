from abc import abstractmethod
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

        query = apply_filters(Payment, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

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

    def delete(self, payment_id: int) -> bool:
        payment = Payment.query.filter_by(id=payment_id).first()
        if not payment:
            return False
        self.db.session.delete(payment)
        self.save()
        return True