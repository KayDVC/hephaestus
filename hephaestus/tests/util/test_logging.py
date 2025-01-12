from hephaestus.io.logging import get_logger
from hephaestus.testing.swte import StrConsts


class TestLogging:

    def test_basic_logger(self):
        """Verifies that base logger name functionality is unchanged"""

        # Loggers with the same name should be the same object.
        assert get_logger(name=StrConsts.MAGIC_STRING_ONE) is get_logger(
            name=StrConsts.MAGIC_STRING_ONE
        )

        # Loggers with different names should be different objects.
        assert get_logger(name=StrConsts.MAGIC_STRING_ONE) is not get_logger(
            name=StrConsts.MAGIC_STRING_TWO
        )
