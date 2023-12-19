from types import FrameType, TracebackType
from typing import Any, Optional, Callable
import sys
import pytest

def traceit(frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
    # print(frame.f_code.co_qualname)
    # print(frame.f_code.co_filename)
    # print("self" in frame.f_locals and hasattr(frame.f_locals["self"], "a"))
    # print(type(getattr(frame.f_locals["self"], "a")).__name__)
    return traceit

def collect_variable_types(path: str, target_class: str):
    sys.settrace(traceit)
    pytest.main(["-s", "./src/"])
    sys.settrace(None)
    return dict()
