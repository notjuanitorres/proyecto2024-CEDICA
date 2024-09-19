from dependency_injector import containers, providers
from .module.accounts import AccountsServices, AccountsRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.core.module.accounts"])
    config = providers.Configuration()

    # Repositories
    accounts_repository = providers.Factory(AccountsRepository)

    # Services
    accounts_services = providers.Factory(AccountsServices,
                                          accounts_repository=accounts_repository)
