import inspect

def try_convert(value, expected_type):
    try:
        if expected_type == float:
            return float(value)
        elif expected_type == int:
            return int(value)
        elif expected_type == bool:
            return value.lower() in ('1', 'true', 'yes', 'on', 'y')
        elif expected_type == str:
            return value
        else:
            return value  # fallback for untyped or unsupported types
    except (ValueError, TypeError):
        return None  # conversion failed

def call_method_by_name(obj, method_name, *args, **kwargs):
    method = getattr(obj, method_name, None)
    if not callable(method):
        raise AttributeError(f"'{type(obj).__name__}' object has no method '{method_name}'")

    sig = inspect.signature(method)
    params = list(sig.parameters.values())

    converted_args = []
    for arg_str, param in zip(args, params):
        expected_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        converted = try_convert(arg_str, expected_type)
        if converted is None and expected_type != str:
            print(f"Skipping call: failed to convert '{arg_str}' to {expected_type.__name__}")
            return None  # skip the call entirely
        converted_args.append(converted)

    try:
        return method(*converted_args, **kwargs)
    except TypeError:
        print(f"Skipping call, arg count problem.")

        return None  # conversion failed

