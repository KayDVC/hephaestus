import inspect

from logging import getLogger
from typing import Any, Callable, Type

from hephaestus.common.exceptions import LoggedException

_logger = getLogger(__name__)

# Internal "cache" of defined getters and ignores for each parent.
__cls_maps: dict[str, "__ReferenceMap"] = {}
__getter_id = "__hephaestus_getter_method"
__ignore_id = "__hephaestus_ignore_method"

# Used to check if a modifier has already been set on a method. External
# users should only assign one modifier per method.
__errors = {
    __getter_id: "This method has already been declared a getter.",
    __ignore_id: "This method has already been marked as ignored.",
}


##
# Private
##
class __ReferenceMap:
    def __init__(self, getter: Callable = None, ignores: list[Callable] = []):
        self.getter = getter
        self.ignores = ignores


def __return_none() -> None:
    """Empty function used to always get None on call.

    Returns:
        None
    """
    return None


def __method_wrapper(getter: Callable, if_none: Callable, method_name: str) -> Callable:
    """Wraps methods, ensuring calls go to object stored by reference.

    Args:
        getter: the function to use a "getter" for the stored object.
        if_none: the function to use should the stored object be Null.
        method_name: the name of method to wrap.

    Returns:
        A callable function that acts as a proxy for the method to wrap.

    Note:
        Any args passed to the wrapped method will be passed to the stored object's
        actual method without modification.
    """

    def _wrapper(self, *args, **kwargs) -> Any:
        obj = getter(self)
        if not obj:
            _logger.debug("Referenced object is null.")
            return if_none()
        return getattr(obj, method_name)(*args, **kwargs)

    return _wrapper


##
# Public
##
class ReferenceError(LoggedException):
    pass


def reference_ignore(method: Callable) -> Callable:
    """Specifies to avoid proxying the method call using the store object.

    Args:
        method: the method to avoid wrapping.

    Raises:
        ReferenceError: if another reference modifier has already been specified
        for the method.

    Returns:
        The method, largely unmodified.
    """

    # Ensure only one reference modifier externally set on method at a time.
    for id_ in __errors.keys():
        if hasattr(method, id_):
            raise ReferenceError(__errors[id_])

    # Get fully-qualified name of parent. This is the key
    # used to store the class's reference map.
    parent, method_name = method.__qualname__.rsplit(".", 1)
    cls_map = __cls_maps.get(parent, __ReferenceMap())

    # Set modifier indicator and add to reference map.
    setattr(method, __ignore_id, True)
    cls_map.ignores.append(method_name)

    # Update reference map cache.
    __cls_maps[parent] = cls_map

    return method


def reference_getter(method: Callable) -> Callable:
    """Specifies to use the method to get the stored object.

    Args:
        method: the method that returns the stored object.

    Raises:
        ReferenceError: if another reference modifier has already been specified
        for the method.

    Returns:
        The method, largely unmodified.
    """

    # Ensure only one reference modifier externally set on method at a time.
    for id_ in __errors.keys():
        if hasattr(method, id_):
            raise ReferenceError(__errors[id_])

    # Get fully-qualified name of parent. This is the key
    # used to store the class's reference map.
    parent, method_name = method.__qualname__.rsplit(".", 1)
    cls_map = __cls_maps.get(parent, __ReferenceMap())

    # Set modifier indicators for this method. Here, we want this method to have
    # both the getter and ignore indicator so that our reference logic will skip wrapping the
    # function without adding an extra conditional check.
    setattr(method, __getter_id, True)
    cls_map.getter = method_name
    setattr(method, __ignore_id, True)
    cls_map.ignores.append(method_name)

    # Update reference map cache.
    __cls_maps[parent] = cls_map
    return method


def reference(cls: Type) -> Type:
    """Specifies the class holds a stored object.

    Args:
        cls: the class definition to wrap.

    Raises:
        ReferenceError: should the passed object not be a class definition.

    Returns:
        The class definition with some minor tweaks to instantiation and object creation
        logic.

    Note:
        Generally, any method defined for the class other than the "getter" should
        be annotated with @reference_ignore.
    """

    # All the logic is dependent on the object being a class. Ensure it is so.
    if not inspect.isclass(cls):
        raise ReferenceError(f"{str(cls.__name__)} object is not a class.")

    # Save unmodified methods for later use.
    __unmodified_new = cls.__new__

    # TODO: better docstring.
    def __new__(cls: Type, *args, **kwargs):
        """
        Args:
            cls: the class object.

        Raises:
            ReferenceError: if a "getter" is not defined for the class.
        """

        # Use the fully qualified name of the class to lookup the "getter" and "ignore" methods
        # for the class.
        cls_map = __cls_maps.get(cls.__qualname__, None)

        # At minimum, the class should have a method decorated with "@reference_getter" otherwise,
        # most of the logic won't work.
        if (not cls_map) or (not cls_map.getter) or (not hasattr(cls, cls_map.getter)):
            raise ReferenceError("Could not find getter for class.")

        # Get the function objects to pass to the wrapper methods.
        getter_ = getattr(cls, cls_map.getter)
        if_none_method_ = __return_none  # TODO: make configurable as a param?

        # Save getter method for any other lookups.
        setattr(cls, __getter_id, getter_)

        # Wrap all methods not marked with @reference_ignore. Also ignore dunder methods.
        for item_str in dir(cls):
            if (item_str.startswith("__")) or (item_str in cls_map.ignores):
                continue

            item = getattr(cls, item_str)
            if callable(item):
                setattr(
                    cls,
                    item_str,
                    __method_wrapper(
                        getter=getter_, if_none=if_none_method_, method_name=item_str
                    ),
                )

        # Pass along any extra arguments supplied unless the `__new__` method doesn't take any additional arguments.
        return (
            __unmodified_new(cls)
            if __unmodified_new is object.__new__
            else __unmodified_new(cls, *args, **kwargs)
        )

    def __getattr__(self, name: str) -> Any:
        """
        Args:
            name: the name of the attribute.

        Raises:
            AttributeError: if the attribute isn't defined for the stored object.

        Returns:
            The value of the attribute.

        Note:
            This method is only called when the attribute cannot be found in the instance.
            It's very useful for ensuring the attributes defined during object instantiation are
            still accessible.
        """

        # Get defined "getter" method. We don't need to pass `self` to the method because the method
        # is bound to the object referred to by self.
        getter_ = getattr(self, __getter_id)
        instance = getter_()

        # Handle case where stored object can't be checked. We don't want to crash and burn here, nor
        # nor impose any weird implementation-specific mandates about reference checking.
        if not instance:
            return None

        # Check stored object for attribute.
        if not hasattr(instance, name):
            raise AttributeError(f"'{self.__class__}' object has no attribute '{name}'")

        return getattr(instance, name)

    # Update methods for class
    cls.__new__ = __new__
    cls.__getattr__ = __getattr__

    return cls
