import hephaestus.util.logging as logging
import hephaestus.testing.swte as swte


class TestLogging:

    def test_basic_logger(self):
        """Verifies that base logger name functionality is unchanged"""

        # Loggers with the same name should be the same object.
        assert logging.get_logger(
            name=swte.Constants.MAGIC_STRING_ONE
        ) is logging.get_logger(name=swte.Constants.MAGIC_STRING_ONE)

        # Loggers with different names should be different objects.
        assert logging.get_logger(
            name=swte.Constants.MAGIC_STRING_ONE
        ) is not logging.get_logger(name=swte.Constants.MAGIC_STRING_TWO)
