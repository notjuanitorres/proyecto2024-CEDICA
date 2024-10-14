# pylint: disable=I1101
from dependency_injector import containers, providers
from .module.accounts import AccountsServices, AccountsRepository
from .module.employee import EmployeeRepository
from .module.equestrian import EquestrianServices, EquestrianRepository
from .module.common import StorageServices
from .module.charges import ChargeRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # TODO: Initialize the db in the container so it can be injected into the repository
    accounts_repository = providers.Factory(AccountsRepository)
    employee_repository = providers.Factory(EmployeeRepository)
    equestrian_repository = providers.Factory(EquestrianRepository)
    charges_repository = providers.Factory(ChargeRepository)

    # Services
    storage_services = providers.Factory(StorageServices)

    accounts_services = providers.Factory(
        AccountsServices, accounts_repository=accounts_repository
    )

    equestrian_services = providers.Factory(
        EquestrianServices, equestrian_repository=equestrian_repository
    )
