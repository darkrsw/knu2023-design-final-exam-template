from types import FrameType, TracebackType
from typing import Any, Optional, Callable
import sys
import pytest
from utils import StackInspector

from typing import TextIO, Type
import os
from glob import glob
import ast
from ast import NodeVisitor

def collect_variable_types(path: str, target_class: str):
    return dict()
