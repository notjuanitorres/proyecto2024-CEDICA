from dependency_injector import containers, providers
from .database import db
from .module.accounts import AccountsServices, AccountsRepository
from .module.equestrian import EquestrianServices, EquestrianRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    # TODO: Initialize the db in the container so it can be injected into the repository
    accounts_repository = providers.Factory(AccountsRepository)
    equestrian_repository = providers.Factory(EquestrianRepository)

    # Services
    accounts_services = providers.Factory(
        AccountsServices, accounts_repository=accounts_repository
    )
    equestrian_services = providers.Factory(
        EquestrianServices, equestrian_repository=equestrian_repository
    )
