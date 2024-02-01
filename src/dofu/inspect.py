import enum
from functools import wraps, WRAPPER_ASSIGNMENTS
from types import CodeType

from fire import docstrings
from fire.docstrings import DocstringInfo


class CodeFlags(enum.Enum):
    """
    Code flags that dis understands.

    This is defined according to `dis.COMPILER_FLAG_NAMES`.
    """

    OPTIMIZED = 1
    NEWLOCALS = 2
    VARARGS = 4
    VARKEYWORDS = 8
    NESTED = 16
    GENERATOR = 32
    NOFREE = 64
    COROUTINE = 128
    ITERABLE_COROUTINE = 256
    ASYNC_GENERATOR = 512


def extend_interface(part, pass_result=False, pass_result_key="__result__"):
    """
    An annotation that extend annotated function's signature with `part''s.

    :param part: The function whose signature will be appended after annotated
      function's, and will be called whenever calling the extended function.
    :param pass_result: Whether to pass the result of part to the extended
      function.
    :param pass_result_key: The key to pass the result of part to the extended.
    :return: The annotation function.
    """

    def inner(fn):
        extended = extend(fn, part, pass_result, pass_result_key)
        return extended

    return inner


def extend(
    fn: callable,
    part: callable,
    pass_result: bool = False,
    pass_result_key="__result__",
):
    """
    Extend fn's signature with part's.

    Combine fn and part into one function that first runs part followed by fn.

    :param fn: The main function.
    :param part: The patched function that runs before the main one.
    :param pass_result: Whether to pass the result of part to the extended
      function.
    :param pass_result_key: The key to pass the result of part to the extended.
    :return: The combined function.
    """
    pco = getattr(part, "__code__", None)

    # if part is a normal function
    if pco is not None:
        assert pco.co_argcount == 0, "The part func can only have kwonly-args"

    # if part is a wrapped function
    elif hasattr(part, "__wrapped__") and hasattr(part.__wrapped__, "__code__"):
        part = part.__wrapped__
        pco = part.__code__
        assert pco.co_argcount == 0, "The part func can only have kwonly-args"

    # if part is a callable object
    elif hasattr(part, "__call__") and hasattr(part.__call__, "__code__"):
        part = part.__call__
        pco = part.__code__
        assert pco.co_argcount == 1, "The part func can only have kwonly-args"

    # if part is a class
    elif hasattr(part, "__init__") and hasattr(part.__init__, "__code__"):
        part = part.__init__
        pco = part.__code__
        assert pco.co_argcount == 1, "The part func can only have kwonly-args"

    else:
        raise RuntimeError("Failed to get the code object of the part func")

    # this is a hacking to make sure the signature of the combined function
    fn_sig = mock_sig(fn)
    fn_sig.__annotations__.update(part.__annotations__ or {})

    part_kwonly = pco.co_varnames[
        pco.co_argcount : pco.co_kwonlyargcount + pco.co_argcount
    ]
    extend_kwonly(fn_sig, *part_kwonly, **part.__kwdefaults__ or {})

    @wraps(fn_sig)
    def extended(*args, **kwargs):
        part_kwargs = {k: kwargs.pop(k) for k in part_kwonly if k in kwargs}
        part_result = part(**part_kwargs)
        pass_kwargs = {pass_result_key: part_result} if pass_result else {}
        return fn(*args, **kwargs, **pass_kwargs)

    extended.__doc__ = extend_doc(fn_sig, part.__doc__)
    return extended


def extend_kwonly(fn: callable, *more_kwonly, **kwdefaults):
    """
    Extend the signature of the given fn with additional kwonly-args.

    :param fn: The function going to be extended
    :param more_kwonly: kwonly-args going to be extended
    :param kwdefaults: kwonly-args going to be extended with defaults
    """
    co = fn.__code__

    extended_kwonlyargcount = co.co_kwonlyargcount + len(more_kwonly)

    argcount = co.co_argcount + co.co_kwonlyargcount
    extended_varnames = (
        co.co_varnames[:argcount] + more_kwonly + co.co_varnames[argcount:]
    )

    fn.__code__ = co.replace(
        co_kwonlyargcount=extended_kwonlyargcount,
        co_nlocals=len(extended_varnames),
        co_varnames=extended_varnames,
    )
    if not fn.__kwdefaults__:
        fn.__kwdefaults__ = {}
    fn.__kwdefaults__.update(**kwdefaults)


def mock_sig(_fn_: callable, _behavior_: callable or None = None):
    """
    Create a brand-new function whose signature is the same as fn's.

    By default, the created function is only used as signature, and you should
    never call it. But, you can assign a callback through `behavior' to make the
    created function callable.

    :param _fn_: The original function being imitated
    :param _behavior_: A callback being called when calling the cloned function.
    :return: The created brand-new function.
    """
    # unwrap the function to get the original one if it is wrapped
    _fn_ = getattr(_fn_, "__wrapped__", None) or _fn_

    @wraps(_fn_, assigned=WRAPPER_ASSIGNMENTS + ("__defaults__", "__kwdefaults__"))
    def cp():  # specify no arg for cp since the call sig will be replaced by _fn_'s
        if _behavior_:
            kwargs = dict(locals())
            del kwargs["_behavior_"]
            # Currently, this function cannot have positional-only args since
            #   we pass the call args in the keyword way
            return _behavior_(**kwargs)
        raise RuntimeError(
            "This function is for signature-used only, please do NOT call it!"
        )

    delattr(cp, "__wrapped__")

    cp_co: CodeType = cp.__code__
    fn_co: CodeType = _fn_.__code__

    cp_total_argcount = cp_co.co_argcount + cp_co.co_kwonlyargcount
    fn_total_argcount = fn_co.co_argcount + fn_co.co_kwonlyargcount

    if fn_co.co_flags & CodeFlags.VARARGS.value:
        fn_total_argcount += 1

    if fn_co.co_flags & CodeFlags.VARKEYWORDS.value:
        fn_total_argcount += 1

    assert cp_total_argcount == 0, (
        "Do NOT specify any args for cp! Because it "
        "will be confusing since these args would be "
        "swept finally."
    )

    fn_all_argnames = fn_co.co_varnames[:fn_total_argcount]

    cp.__code__ = cp.__code__.replace(
        co_flags=fn_co.co_flags,
        co_argcount=fn_co.co_argcount,
        co_posonlyargcount=fn_co.co_posonlyargcount,
        co_kwonlyargcount=fn_co.co_kwonlyargcount,
        # locals consists of args and local vars. since the copied function has
        # the func interface of fn, and the func body of cp, the number of
        # locals is just the sum of that two sets of vars
        co_nlocals=fn_total_argcount + cp_co.co_nlocals,
        # co_varnames consists of names of all arg and local vars. since the
        # copied function has the func interface of fn, and the func body of cp,
        # the co_varnames shall be defined like following
        co_varnames=fn_all_argnames + cp_co.co_varnames,
    )
    cp.__annotations__ = {**(_fn_.__annotations__ or {})}
    return cp


def extend_doc(fn: callable, more_doc: str):
    """
    Extend `'fn.__doc__ with `more_doc' section by section.

    :param fn: The function whose __doc__ going to be extended.
    :param more_doc: The additional documentation.
    :return: The extended documentation.
    """
    if not more_doc:
        return

    summary, desc, args, returns, yields, raises = docstrings.parse(fn.__doc__)
    pi = docstrings.parse(more_doc)

    summary = " ".join(filter(None, [summary, pi.summary]))
    desc = "\n".join(filter(None, [desc, pi.description]))
    args = (args or []) + (pi.args or [])
    returns = "\n".join(filter(None, [returns, pi.returns]))
    raises = "\n".join(filter(None, [raises, pi.raises]))
    yields = "\n".join(filter(None, [yields, pi.yields]))

    info = DocstringInfo(
        summary=summary,
        description=desc,
        args=args,
        returns=returns,
        raises=raises,
        yields=yields,
    )
    fn.__doc__ = to_doc(info)
    return fn.__doc__


def to_doc(info: DocstringInfo):
    """Stringify the given docstring obj to a formal document/comment string."""
    summary, desc, args, returns, yields, raises = info
    summary = summary + "\n" if summary else None
    desc = desc if desc else None
    args = "\n".join(f":param {name}: {desc}" for name, _, desc in args)
    returns = f":return: {returns}" if returns else None
    raises = f":raise: {raises}" if raises else None
    yields = f":yield: {yields}" if yields else None

    doc = "\n".join(filter(None, [summary, desc, args, returns, raises, yields]))
    return doc
