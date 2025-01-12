from hephaestus.io.logging import get_logger
from hephaestus.testing.swte import StrConsts


class TestLogging:

    def test_basic_logger(self):
        """Verifies that base logger name functionality is unchanged"""

        # Loggers with the same name should be the same object.
        assert get_logger(name=StrConsts.DEADBEEF) is get_logger(
            name=StrConsts.DEADBEEF
        )

        # Loggers with different names should be different objects.
        assert get_logger(name=StrConsts.DEADBEEF) is not get_logger(
            name=StrConsts.BADDCAFE
        )
