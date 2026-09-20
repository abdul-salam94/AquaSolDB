# -*- coding: utf-8 -*-
"""Write a selection back out.

CSV is the release format (UTF-8, LF, one header row) and is always available.  Parquet
is offered only when `pyarrow` is importable, and the ImportError names the missing
dependency and how to install it rather than letting pandas raise from three frames down.
"""
PARQUET_DEPENDENCY = "pyarrow"


def save_csv(df, path, **kwargs):
    """Write `df` as UTF-8 CSV with LF endings and no index column. Returns `path`.

    The defaults are the release's own conventions, so a file written here reads back
    with `open_table`-like settings on any platform.  Any of them can be overridden.
    """
    options = {"index": False, "encoding": "utf-8", "lineterminator": "\n"}
    options.update(kwargs)
    df.to_csv(path, **options)
    return path


def parquet_available():
    """True when the optional parquet dependency can be imported."""
    try:
        __import__(PARQUET_DEPENDENCY)
    except ImportError:
        return False
    return True


def save_parquet(df, path, **kwargs):
    """Write `df` as Parquet. Returns `path`.

    Parquet is optional: it needs `pyarrow`, which is not a dependency of this package
    (the release is CSV only, R-DB3-9).  Without it this raises ImportError naming the
    package to install -- it never silently writes a CSV instead.
    """
    if not parquet_available():
        raise ImportError(
            "writing Parquet needs the optional dependency %r, which is not installed. "
            "Install it with `pip install %s` (or `pip install aquasoldb[parquet]`), or "
            "use save_csv, which needs nothing beyond pandas."
            % (PARQUET_DEPENDENCY, PARQUET_DEPENDENCY))
    options = {"index": False, "engine": PARQUET_DEPENDENCY}
    options.update(kwargs)
    df.to_parquet(path, **options)
    return path


__all__ = ["PARQUET_DEPENDENCY", "parquet_available", "save_csv", "save_parquet"]