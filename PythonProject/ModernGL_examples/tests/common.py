import ModernGL

_static = {
    'context': None,
}


def get_context() -> ModernGL.Context:
    ctx = _static.get('context')

    if ctx is None:
        ctx = ModernGL.create_standalone_context()
        _static['context'] = ctx

    return ctx
