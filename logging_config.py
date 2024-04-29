import logging

def setup_logging(log_filename):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

# Create and configure the root logger
setup_logging('app.log')
logger = logging.getLogger('my_application') 