from dependency_injector import containers, providers
from .module.accounts import AccountsServices, AccountsRepository
from .module.employee import EmployeeServices, EmployeeRepository
from .database import db


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    # TODO: Initialize the db in the container so it can be injected into the repository
    accounts_repository = providers.Factory(AccountsRepository)
    employee_repository = providers.Factory(EmployeeRepository)

    # Services
    accounts_services = providers.Factory(
        AccountsServices, accounts_repository=accounts_repository
    )

    employee_services = providers.Factory(
        EmployeeServices, employee_repository=employee_repository
    )
