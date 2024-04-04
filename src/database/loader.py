import traceback
from loguru import logger

class DatabaseLoader:
    """
    Class responsible for loading the database and setting it up.
    """

    def __init__(self) -> None:
        raise NotImplementedError("No classes instantiated for DatabaseLoader.")

    async def setup(self) -> None:
        """
        Sets up the database by creating the necessary table.
        """
        try:
            # Create database table(s)
            raise NotImplementedError("No database table setup implemented.")
        except Exception as e:
            logger.critical(f"Error setting up database: {e}")
            traceback.print_exc()