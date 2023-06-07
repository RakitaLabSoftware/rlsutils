import inspect
from typing import Type

import hydra_zen as hz
from omegaconf import OmegaConf


def get_nested_params(obj, mode: str = "class"):
    params = {}
    match mode:
        case "class":
            sig = inspect.signature(obj.__init__)
        case "func":
            sig = inspect.signature(obj)
        case _:
            raise NotImplementedError()
    for param_name, param in sig.parameters.items():
        # FIXME rewrite
        if (
            param.default != inspect.Parameter.empty
            and inspect.isclass(param.default.__class__)
            and not isinstance(param.default, (int, float, str, bool))
        ):
            inner_params = {}
            print(sig)
            inner_sig = inspect.signature(param.default.__init__).parameters.keys()
            for inner_param_name in list(inner_sig):
                inner_params[inner_param_name] = getattr(
                    param.default, inner_param_name
                )
            params[param_name] = OmegaConf.structured(
                hz.builds(
                    param.default.__class__,
                    **inner_params,
                    populate_full_signature=True,
                )
            )
    return params


def make_component_config(component, mode: str = "class"):
    params = get_nested_params(component, mode)
    print(params)
    try:
        print("in func")
        obj_cfg = hz.builds(
            component,
            **params,
            populate_full_signature=True,
            zen_partial=True,
        )
    except:
        print("in class")
        obj_cfg = hz.builds(component.__class__, **params, populate_full_signature=True)
    cfg = OmegaConf.structured(obj_cfg)
    return cfg
