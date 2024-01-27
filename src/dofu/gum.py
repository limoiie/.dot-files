import contextlib
import subprocess
import typing as t

__all__ = [
    "choose",
    "confirm",
    "file_",
    "filter_",
    "format_",
    "input_",
    "write",
    "log",
    "pager",
    "spin",
    "style",
    "table",
]


def choose(
    *items,
    header: str = None,
    selected: t.List[str] = None,
    select_if_one: bool = None,
    limit: int = None,
    no_limit: bool = None,
    height: int = None,
    timeout: int = None,
):
    return subprocess.check_output(
        ["gum", "choose"]
        + [f"--header='{header}'" for header in opt(header)]
        + [f"--selected={','.join(slct)}" for slct in opt(selected) if slct]
        + [f"--select-if-one" for _ in opt(select_if_one)]
        + [f"--limit={limit}" for limit in opt(limit)]
        + [f"--no-limit" for _ in opt(no_limit)]
        + [f"--height={height}" for height in opt(height)]
        + [f"--timeout={timeout}" for timeout in opt(timeout)]
        + list(items),
        encoding="utf-8",
    )


def confirm(
    body,
    *,
    affirmative: str = None,
    default: int = None,
    negative: str = None,
    timeout: int = None,
):
    try:
        subprocess.check_output(
            ["gum", "confirm"]
            + [f"--affirmative='{affirmative}'" for affirmative in opt(affirmative)]
            + [f"--default={default}" for default in opt(default)]
            + [f"--negative='{negative}'" for negative in opt(negative)]
            + [f"--timeout={timeout}" for timeout in opt(timeout)]
            + [f"'{body}'"],
            encoding="utf-8",
        )
        return True

    except subprocess.CalledProcessError:
        return False


def file_(
    init_dir: str = None,
    *,
    show_all: bool = None,
    allow_directory: bool = None,
    allow_file: bool = None,
    height: int = None,
    timeout: int = None,
):
    return subprocess.check_output(
        ["gum", "file"]
        + [f"--all" for _ in opt(show_all)]
        + [f"--directory" for _ in opt(allow_directory)]
        + [f"--file" for _ in opt(allow_file)]
        + [f"--height={height}" for height in opt(height)]
        + [f"--timeout={timeout}" for timeout in opt(timeout)]
        + [f"'{init_dir}'" for init_dir in opt(init_dir)],
        encoding="utf-8",
    )


def filter_(
    *items,
    fuzzy: bool = None,
    header: str = None,
    indicator: int = None,
    limit: int = None,
    no_limit: bool = None,
    placeholder: str = None,
    prompt: str = None,
    reverse: bool = None,
    select_if_one: bool = None,
    sort: bool = None,
    strict: bool = None,
):
    return subprocess.check_output(
        ["gum", "filter"]
        + [f"--fuzzy" for _ in opt(fuzzy)]
        + [f"--header='{header}'" for header in opt(header)]
        + [f"--indicator={indicator}" for indicator in opt(indicator)]
        + [f"--limit={limit}" for limit in opt(limit)]
        + [f"--no-limit" for _ in opt(no_limit)]
        + [f"--placeholder='{placeholder}'" for placeholder in opt(placeholder)]
        + [f"--prompt='{prompt}'" for prompt in opt(prompt)]
        + [f"--reverse" for _ in opt(reverse)]
        + [f"--select-if-one" for _ in opt(select_if_one)]
        + [f"--sort" for _ in opt(sort)]
        + [f"--strict" for _ in opt(strict)]
        + list(items),
        encoding="utf-8",
    )


def format_(
    body: str = None,
    *,
    language: str = None,
    theme: str = None,
    type_: t.Literal["code", "emoji", "markdown", "template"] = None,
):
    return subprocess.check_output(
        ["gum", "format"]
        + [f"--language='{language}'" for language in opt(language)]
        + [f"--theme='{theme}'" for theme in opt(theme)]
        + [f"--type='{type_}'" for type_ in opt(type_)]
        + [f"'{body}'"],
        encoding="utf-8",
    )


def input_(
    *,
    header: str = None,
    init_body: str = None,
    char_limit: int = None,
    password: bool = None,
    placeholder: str = None,
    prompt: str = None,
    width: int = None,
    timeout: int = None,
):
    return subprocess.check_output(
        ["gum", "input"]
        + [f"--header='{header}'" for header in opt(header)]
        + [f"--value='{init_body}'" for init_body in opt(init_body)]
        + [f"--char-limit={char_limit}" for char_limit in opt(char_limit)]
        + [f"--password" for _ in opt(password)]
        + [f"--placeholder='{placeholder}'" for placeholder in opt(placeholder)]
        + [f"--prompt='{prompt}'" for prompt in opt(prompt)]
        + [f"--width={width}" for width in opt(width)]
        + [f"--timeout={timeout}" for timeout in opt(timeout)],
        encoding="utf-8",
    )


def write(
    *,
    header: str = None,
    init_body: str,
    char_limit: int = None,
    placeholder: str = None,
    prompt: str = None,
    show_line_numbers: bool = None,
    show_cursor_line: bool = None,
    width: int = None,
    height: int = None,
):
    return subprocess.check_output(
        ["gum", "write"]
        + [f"--header='{header}'" for header in opt(header)]
        + [f"--value='{init_body}'" for init_body in opt(init_body)]
        + [f"--char-limit={char_limit}" for char_limit in opt(char_limit)]
        + [f"--placeholder='{placeholder}'" for placeholder in opt(placeholder)]
        + [f"--prompt='{prompt}'" for prompt in opt(prompt)]
        + [f"--show-line-numbers" for _ in opt(show_line_numbers)]
        + [f"--show-cursor-line" for _ in opt(show_cursor_line)]
        + [f"--width={width}" for width in opt(width)]
        + [f"--height={height}" for height in opt(height)],
        encoding="utf-8",
    )


def log(
    text,
    *,
    format__: str,
    formatter: str,
    level: t.Literal["debug", "info", "warn", "error", "fatal"] = None,
    prefix: str = None,
    structured: bool = None,
    time: str = None,
):
    return subprocess.check_output(
        ["gum", "log"]
        + [f"--format='{format__}'" for format__ in opt(format__)]
        + [f"--formatter='{formatter}'" for formatter in opt(formatter)]
        + [f"--level='{level}'" for level in opt(level)]
        + [f"--prefix='{prefix}'" for prefix in opt(prefix)]
        + [f"--structured" for _ in opt(structured)]
        + [f"--time='{time}'" for time in opt(time)]
        + [f"'{text}'"],
    )


def pager(
    content: str = None,
    *,
    file: str = None,
    show_line_numbers: bool = None,
    soft_wrap: bool = None,
    timeout: int = None,
):
    if content is not None:
        stdin = contextlib.nullcontext(content)
    else:
        assert file is not None
        stdin = open(file, "r")

    with stdin as stdin:
        return subprocess.check_output(
            ["gum", "pager"]
            + [f"--show-line-numbers" for _ in opt(show_line_numbers)]
            + [f"--soft-wrap" for _ in opt(soft_wrap)]
            + [f"--timeout={timeout}" for timeout in opt(timeout)],
            stdin=stdin,
            encoding="utf-8",
        )


def spin(
    *,
    title: str = None,
    align: t.Literal["left", "right"] = None,
    show_output: bool = None,
    spinner: t.Literal[
        "line",
        "dot",
        "minidot",
        "jump",
        "pulse",
        "points",
        "globe",
        "moon",
        "monkey",
        "meter",
        "hamburger",
    ] = None,
    timeout: int = None,
):
    return subprocess.check_output(
        ["gum", "spin"]
        + [f"--align='{align}'" for align in opt(align)]
        + [f"--show-output" for _ in opt(show_output)]
        + [f"--spinner" for _ in opt(spinner)]
        + [f"--timeout={timeout}" for timeout in opt(timeout)]
        + [f"--title='{title}'" for title in opt(title)],
        encoding="utf-8",
    )


def style(
    body: str,
    *,
    align: t.Literal["bottom", "center", "left", "middle", "right", "top"] = None,
    background: str = None,
    bold: bool = None,
    border: bool = None,
    faint: bool = None,
    foreground: str = None,
    italic: bool = None,
    reverse: bool = None,
    strikethrough: bool = None,
    underline: bool = None,
    width: int = None,
    height: int = None,
    timeout: int = None,
):
    return subprocess.check_output(
        ["gum", "style"]
        + [f"--align='{align}'" for align in opt(align)]
        + [f"--background='{background}'" for background in opt(background)]
        + [f"--bold" for _ in opt(bold)]
        + [f"--border" for _ in opt(border)]
        + [f"--faint" for _ in opt(faint)]
        + [f"--foreground='{foreground}'" for foreground in opt(foreground)]
        + [f"--italic" for _ in opt(italic)]
        + [f"--reverse" for _ in opt(reverse)]
        + [f"--strikethrough" for _ in opt(strikethrough)]
        + [f"--underline" for _ in opt(underline)]
        + [f"--width={width}" for width in opt(width)]
        + [f"--height={height}" for height in opt(height)]
        + [f"--timeout={timeout}" for timeout in opt(timeout)]
        + [f"'{body}'"],
        encoding="utf-8",
    )


def table(
    *,
    file: str = None,
    border: bool = None,
    widths: str = None,
    columns: str = None,
    print_: bool = None,
    separator: str = None,
    height: int = None,
    timeout: int = None,
):
    return subprocess.check_output(
        ["gum", "table"]
        + [f"--file='{file}'" for file in opt(file)]
        + [f"--border" for _ in opt(border)]
        + [f"--widths='{widths}'" for widths in opt(widths)]
        + [f"--columns='{columns}'" for columns in opt(columns)]
        + [f"--print" for _ in opt(print_)]
        + [f"--separator='{separator}'" for separator in opt(separator)]
        + [f"--height={height}" for height in opt(height)]
        + [f"--timeout={timeout}" for timeout in opt(timeout)],
        encoding="utf-8",
    )


def opt(value, *, empty=None):
    if value != empty:
        yield value
