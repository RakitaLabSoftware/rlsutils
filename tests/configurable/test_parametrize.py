from typing import Any
from rlsutils.configurable.parametrize import make_component_config


class MyClass:
    def __init__(self, a=0, b=1, c=1, d=2.0, e="hello"):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


class MyNestedClass:
    def __init__(self, a=0, b=MyClass()):
        self.a = a
        self.b = b

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


def myfunc(a, b="a"):
    pass


def mynestedfunc(a, b=MyClass()):
    pass


def test_get_func_params():
    params = make_component_config(myfunc)
    assert params == {
        "_target_": "test_parametrize.myfunc",
        "_partial_": True,
        "b": "a",
    }


def test_nested_func_params():
    params = make_component_config(mynestedfunc, mode="func")
    print(params)
    assert params == {
        "_target_": "test_parametrize.mynestedfunc",
        "_partial_": True,
        "b": {
            "_target_": "test_parametrize.MyClass",
            "a": 0,
            "b": 1,
            "c": 1,
            "d": 2.0,
            "e": "hello",
        },
    }


def test_class_params():
    obj = MyClass(a=1, b=2)
    params = make_component_config(obj)
    print(params)
    assert params == {
        "_target_": "test_parametrize.MyClass",
        "a": 0,
        "b": 1,
        "c": 1,
        "d": 2.0,
        "e": "hello",
    }


def test_nested_class_params():
    obj = MyNestedClass()
    params = make_component_config(obj)
    print(params)
    assert params == {
        "_target_": "test_parametrize.MyNestedClass",
        "a": 0,
        "b": {
            "_target_": "test_parametrize.MyClass",
            "a": 0,
            "b": 1,
            "c": 1,
            "d": 2.0,
            "e": "hello",
        },
    }
