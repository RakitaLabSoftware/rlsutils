import inspect

import hydra_zen as hz
from omegaconf import OmegaConf


def get_nested_params(obj):
    params = {}
    for param_name, param in inspect.signature(obj).parameters.items():
        # FIXME rewrite
        if (
            param.default != inspect.Parameter.empty
            and inspect.isclass(param.default.__class__)
            and not isinstance(param.default, (int, float, str, bool))
        ):
            inner_params = {}
            for inner_param_name in list(
                inspect.signature(param.default.__init__).parameters.keys()
            ):
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
