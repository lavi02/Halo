from src.repo.log import Container

__version__ = '0.1.0'

if __name__ == "__main__":
    container = Container()
    container.config.log_name.override('Halo')

    logger = container.log()
    handler = container.handler()

    # Handler 사용
    response = handler.handle("Successfully initialized")
