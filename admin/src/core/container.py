# pylint: disable=I1101
from dependency_injector import containers, providers
from .module.accounts import AccountsServices, AccountsRepository
from .module.employee import EmployeeRepository
from .module.payment import PaymentServices, PaymentRepository
from .database import db

from .module.employee import EmployeeRepository
from .module.equestrian import EquestrianServices, EquestrianRepository
from .module.common import StorageServices

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()


    # TODO: Initialize the db in the container so it can be injected into the repository
    accounts_repository = providers.Factory(AccountsRepository)
    employee_repository = providers.Factory(EmployeeRepository)
    payment_repository = providers.Factory(PaymentRepository)
    equestrian_repository = providers.Factory(EquestrianRepository)

    # Services
    storage_services = providers.Factory(StorageServices)

    accounts_services = providers.Factory(
        AccountsServices, accounts_repository=accounts_repository
    )

    equestrian_services = providers.Factory(
        EquestrianServices, equestrian_repository=equestrian_repository
    )

    payment_services = providers.Factory(
        PaymentServices, payment_repository=payment_repository
    )