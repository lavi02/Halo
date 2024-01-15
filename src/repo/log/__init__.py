from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
import logging


class Log:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler('Halo.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message) -> None:
        self.logger.error(message)

    def fatal(self, message):
        self.logger.fatal(message)


class Container(containers.DeclarativeContainer):
    log = providers.Singleton(Log, name="Halo")


class Handler:
    @inject
    def __init__(self, log: Log = Provide[Container.log]):
        self.log = log
        self.log.info('Handler initialized')


container = Container()
container.wire(modules=[__name__])

handler = Handler()
