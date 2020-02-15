import torch as th
import numpy as np

from syft.generic.tensor.util import torch_only
from syft.generic.tensor.util import numpy_only
from syft.generic.tensor.util import BaseTensor
from syft.generic.tensor.util import framework
from syft.generic.tensor.util import execute_default_function_on_child_and_wrap

class RestrictedSyftTensor(BaseTensor(framework)):
    """A tensor class which returns a NotImplementedError for all methods which you do not
    explicitly override."""


    def init(self, *args, **kwargs):
        ""

    @torch_only
    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)

    @numpy_only
    def __new__(cls, input_array, *args, **kwargs):
        print("New AbstractNumpyArray")
        obj = np.asarray(input_array).view(cls)
        obj.init(input_array, *args, **kwargs)
        return obj

    @numpy_only
    def __array_finalize__(self, obj):
        """this is just to propagate attributes - this method is called
        after a method/function is run"""

        if obj is None:
            return
        self.info = getattr(obj, "info", None)

    @torch_only
    def set(self, **kwargs):
        for name, value in kwargs.items():
            try:
                attr = self.__getattribute__(name)
                self.__setattr__(name, value)
            except Exception as e:
                raise AttributeError(
                    f"Attribute '{name}' does not exist for tensor type {type(self)}"
                )
        return self

    @torch_only
    def __syft_function__(self, func, args=(), kwargs=None):
        return execute_default_function_on_child_and_wrap(self, func, args, kwargs)

    @numpy_only
    def __array_function__(self, func, types, args=(), kwargs=None):
        """This is basically the same thing as pytorch's __torch_function__
        but it only works for one of numpy's two types of functions. To override
        all of numpy's functions you also need to use __array_ufunc__"""

        return execute_default_function_on_child_and_wrap(self, func, args, kwargs, types)

    @numpy_only
    def __array_ufunc__(self, ufunc, method, *args, **kwargs):
        """Unlike pytorch which only has one function type, numpy has two,
        func and ufunc. This is basically __array_function__ for ufuncs."""

        if method == "__call__":
            return execute_default_function_on_child_and_wrap(self, ufunc, args, kwargs)
        else:
            return NotImplemented



    # END NUMPY FUNCTIONALITY

# def create_not_implemented_method(method_name):
#     def raise_not_implemented_exception(self, *args, **kwargs):
#         msg = f"You just tried to execute {method_name} on tensor type '{(type(self))}."
#         msg += " However, such a method does not exist within this class."
#
#         raise NotImplementedError(msg)
#
#     return raise_not_implemented_exception
#
# print(set(dir(BaseTensor(framework))))
# print(">>>>" + str(framework))
# print(set(dir(RestrictedSyftTensor)))
#
# for method_name in set(dir(BaseTensor(framework))) - set(dir(RestrictedSyftTensor)):  # TODO: add all relevant methods
#     print(method_name)
    # new_method = create_not_implemented_method(method_name)
    # setattr(RestrictedSyftTensor, method_name, new_method)
