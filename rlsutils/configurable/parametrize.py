import inspect
from omegaconf import OmegaConf
import hydra_zen as hz


def get_nested_params(obj, mode: str = "class"):
    """
    Retrieve nested parameters of an object.

    Args:
        obj: The object to retrieve parameters from.
        mode (str): The mode for parameter retrieval. Defaults to "class".

    Returns:
        dict: A dictionary containing the nested parameters.

    Raises:
        NotImplementedError: If the mode is not "class" or "func".
    """
    params = {}
    # Determine the signature based on the mode
    match mode:
        case "class":
            sig = inspect.signature(obj.__init__)
        case "func":
            sig = inspect.signature(obj)
        case _:
            raise NotImplementedError()

    # Iterate over the parameters in the signature
    for param_name, param in sig.parameters.items():
        # Check if the parameter has a non-empty default value, is a class, and not a basic type
        if (
            param.default != inspect.Parameter.empty
            and inspect.isclass(param.default.__class__)
            and not isinstance(param.default, (int, float, str, bool))
        ):
            inner_params = {}
            # Get the signature of the default value class's __init__ method
            inner_sig = inspect.signature(param.default.__init__).parameters.keys()
            # Iterate over the inner parameters
            for inner_param_name in list(inner_sig):
                # Get the value of the inner parameter from the default value instance
                inner_params[inner_param_name] = getattr(
                    param.default, inner_param_name
                )
            # Build the nested parameter configuration using hz.builds and OmegaConf.structured
            params[param_name] = OmegaConf.structured(
                hz.builds(
                    param.default.__class__,
                    **inner_params,
                    populate_full_signature=True,
                )
            )
    return params


def make_component_config(component, mode: str = "class"):
    """
    Generate a component configuration.

    Args:
        component: The component object.
        mode (str): The mode for parameter retrieval. Defaults to "class".

    Returns:
        OmegaConf: The configuration object for the component.
    """
    # Retrieve the nested parameters of the component
    params = get_nested_params(component, mode)
    try:
        # Try building the component configuration using hz.builds with the retrieved parameters
        obj_cfg = hz.builds(
            component,
            **params,
            populate_full_signature=True,
            zen_partial=True,
        )
    except:
        # If an exception occurs, assume the component is a class and build the configuration with its class
        obj_cfg = hz.builds(component.__class__, **params, populate_full_signature=True)
    # Convert the built configuration object to an OmegaConf structured object
    cfg = OmegaConf.structured(obj_cfg)
    return cfg
