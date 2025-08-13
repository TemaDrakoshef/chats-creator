import logging

import betterlogging as bl


def setup_logging(level=logging.INFO):
    """Sets up logging for the application."""
    bl.basic_colorized_config(level=level)
    logging.getLogger("telethon.network.mtprotosender").setLevel(
        logging.WARNING
    )
    logging.basicConfig(
        level=level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
