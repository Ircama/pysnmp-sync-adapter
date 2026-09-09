import sys
import pysnmp

try:
    # Python 3.8+
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # For Python <3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    pysnmp_version = version("pysnmplib")
    raise ImportError(
        f"pysnmp-sync-adapter requires pysnmp>=7.0.0. "
        f"Detected version: pysnmplib {pysnmp_version}. "
        f"Please uninstall pysnmplib with `pip uninstall pysnmplib`. "
        f"Then install the latest pysnmp version with `pip install pysnmp`."
    )
except PackageNotFoundError:
    pass

try:
    pysnmp_version = version("pysnmp")
    if pysnmp_version.startswith("4.") or pysnmp_version.startswith("5."):
        raise ImportError(
            f"pysnmp-sync-adapter requires pysnmp>=7.0.0. "
            f"Detected version: {pysnmp_version}. "
            f"Please uninstall pysnmp with `pip uninstall pysnmp`. "
            f"Then install the latest pysnmp version with `pip install pysnmp`."
        )
except PackageNotFoundError:
    print("pysnmp not found. Please install pysnmp>=7.0.0.", file=sys.stderr)
    raise

from .sync_adapters import (
    get_cmd_sync,
    next_cmd_sync,
    set_cmd_sync,
    bulk_cmd_sync,
    walk_cmd_sync,
    bulk_walk_cmd_sync,
    create_transport,
    parallel_get_sync,
    cluster_varbinds,
    ensure_loop
)


def create_dispatcher(dispatcher_cls=None):
    """
    Safely create a pysnmp dispatcher (SnmpDispatcher for v1arch) or engine
    (SnmpEngine for v3arch), ensuring an event loop exists first.

    Required on Python >= 3.12, where asyncio.get_event_loop() no longer
    creates an event loop implicitly and pysnmp's dispatcher/engine
    constructors fail without one.

    Example:
        from pysnmp.hlapi.v1arch.asyncio import SnmpDispatcher
        dispatcher = create_dispatcher(SnmpDispatcher)

        from pysnmp.hlapi.v3arch.asyncio import SnmpEngine
        engine = create_dispatcher(SnmpEngine)

    If dispatcher_cls is omitted, it is auto-detected from the selected
    architecture (SnmpEngine for v3arch, SnmpDispatcher otherwise).
    """
    if dispatcher_cls is None:
        from pysnmp.hlapi.v1arch.asyncio import SnmpDispatcher
        from pysnmp.hlapi.v3arch.asyncio import SnmpEngine
        from .sync_adapters import arch
        dispatcher_cls = SnmpEngine if arch == "v3arch" else SnmpDispatcher
    ensure_loop()
    return dispatcher_cls()
