import pytest
from hephaestus.decorators.reference import (
    reference,
    reference_getter,
    reference_ignore,
    ReferenceError,
)


# Define's a simple, valid reference.
@reference
class ValidReferenceClass(str):

    def __init__(self, value: str):
        self.update(value)

    @reference_getter
    def get(self) -> str:
        return self._value

    @reference_ignore
    def update(self, value: str):
        self._value = value


class TestReference:

    def test_verify_getter_defined(self, logger):
        """Verifies reference decorator throws exception when "getter" not specified."""

        logger.debug("Testing something")
        with pytest.raises(ReferenceError) as execution:

            @reference
            class FakeClass:
                pass

            # This error is thrown when __new__ is called so, we need to instantiate an object.
            FakeClass()

        assert "Could not find getter" in str(execution.value)

    def test_verify_class(self):
        """Verifies reference decorator throws exception when used on non-class object."""
        with pytest.raises(ReferenceError) as execution:

            @reference
            def FakeMethod():
                pass

        assert "object is not a class" in str(execution.value)

    def test_ensure_getattr_valid(self):
        """Verifies reference decorator throws exception attempting to access a method
        not defined in reference class or stored object.
        """
        to_find = "method_that_doesn't_exist"
        with pytest.raises(AttributeError) as execution:

            # Should call __getattr__ which is ultimately what's being tested.
            getattr(ValidReferenceClass("testing"), to_find)

        assert f"object has no attribute '{to_find}'" in str(execution.value)

    def test_ensure_none_on_none_stored_object(self):
        """Verifies when the stored object is 'None', None is returned for
        any method call.
        """
        assert ValidReferenceClass(None).upper() is None
