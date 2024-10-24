from enum import Enum


class PaymentTypeEnum(Enum):
    """
    Enum for the different types of payments.
    """
    HONORARIOS = 'HONORARIOS'
    PROOVEDOR = 'PROOVEDOR'
    GASTOS = 'GASTOS'
