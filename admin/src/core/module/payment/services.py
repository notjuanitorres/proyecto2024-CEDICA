from abc import abstractmethod
from typing import Dict
from .repositories import AbstractPaymentRepository
from .models import Payment
from .mappers import PaymentMapper as Mapper


class AbstractPaymentServices:
    @abstractmethod
    def create_payment(self, payment: Dict) -> Dict | None:
        raise NotImplementedError

    @abstractmethod
    def get_page(self, page: int, per_page: int, search_query: Dict, order_by: list):
        raise NotImplementedError

    @abstractmethod
    def get_payment(self, payment_id: int) -> Dict | None:
        raise NotImplementedError

    @abstractmethod
    def update_payment(self, payment_id: int, data: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_payment(self, payment_id: int) -> bool:
        raise NotImplementedError


class PaymentServices(AbstractPaymentServices):
    def __init__(self, payment_repository: AbstractPaymentRepository):
        self.payment_repository = payment_repository

    def create_payment(self, payment: Dict) -> Dict | None:
        created_payment = self.payment_repository.add(Mapper.to_entity(payment))

        return Mapper.from_entity(created_payment)

    def get_page(self, page: int, per_page: int, search_query: Dict, order_by: list):
        max_per_page = 100
        per_page = 20
        return self.payment_repository.get_page(
            page, per_page, max_per_page, search_query, order_by
        )

    def get_payment(self, payment_id: int) -> Dict | None:
        payment = self.payment_repository.get_by_id(payment_id)
        if not payment:
            return None
        return Mapper.from_entity(payment)

    def update_payment(self, payment_id: int, data: Dict) -> None:
        data["id"] = payment_id
        return self.payment_repository.update(payment_id, data)

    def delete_payment(self, payment_id: int) -> bool:
        return self.payment_repository.delete(payment_id)