from hephaestus.patterns.singleton import Singleton


class FakeClassOne(metaclass=Singleton):
    pass


class FakeClassTwo(metaclass=Singleton):
    pass


class TestSingleton:

    def test_same_instance(self):
        """Verifies multiple instantiation attempts on a single class only result in one object."""

        obj1 = FakeClassOne()
        obj2 = FakeClassOne()

        assert obj1 is obj2

    def test_has_mutex(self):
        """Verifies each object is created with a mutex."""

        obj1 = FakeClassOne()

        assert hasattr(obj1, "_lock")

    def test_different_mutex_objects(self):
        """Verifies each object has a personal mutex."""

        obj1 = FakeClassOne()
        obj2 = FakeClassTwo()

        assert obj1._lock is not obj2._lock
