import hephaestus.testing.swte as swte
from hephaestus.decorators.track import TraceQueue, track


class TestTrack:

    FAKE_FUNCTION_RETURN_VALUE = 5

    def _fake_function(self, *args, **kwargs):
        return self.FAKE_FUNCTION_RETURN_VALUE

    def test_track_function(
        self,
    ):
        """Verifies tracker records a method call"""

        tq = TraceQueue()

        wrapped_fake_function = track(self._fake_function)
        wrapped_fake_function()

        assert tq.get().name == self._fake_function.__name__

    def test_track_arguments(self):
        """Verifies tracker records the arguments passed to a method."""

        args = (swte.IntConsts.BADDCAFE, swte.IntConsts.DEADBEEF)
        kwargs = {
            "DEADBEEF": swte.StrConsts.DEADBEEF,
            "BADDCAFE": swte.StrConsts.BADDCAFE,
        }

        tq = TraceQueue()

        wrapped_fake_function = track(self._fake_function)
        wrapped_fake_function(*args, **kwargs)

        traced = tq.get()
        assert traced.args == args and traced.kwargs == kwargs

    def test_trace_return_value(self):
        """Verifies tracker records the return value of a method"""

        tq = TraceQueue()

        wrapped_fake_function = track(self._fake_function)
        wrapped_fake_function()

        assert tq.get().retval == self.FAKE_FUNCTION_RETURN_VALUE
