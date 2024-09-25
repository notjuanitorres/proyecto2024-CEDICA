from dependency_injector import containers, providers
from .database import db
from .module.accounts import AccountsServices, AccountsRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    # TODO: Initialize the db in the container so it can be injected into the repository
    accounts_repository = providers.Factory(AccountsRepository)

    # Services
    accounts_services = providers.Factory(
        AccountsServices, accounts_repository=accounts_repository
    )
