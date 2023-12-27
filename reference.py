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

class ClassCollector(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.classmap = {}
        self.path = ""

    def set_path(self, p):
        self.path = p

    def visit_ClassDef(self, node):
        self.classmap[node.name] = {"ast": node, "path": self.path}
        return super().generic_visit(node)

def get_type_names(vars):
    return list([type(x) for x in vars])

class MethodVisitor(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.members = set()

    def visit_Attribute(self, anode):
        if anode.value.id == "self":
            self.members.add(anode.attr)
        return super().generic_visit(anode)


class MemberCollector(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.members = set()

    def iterate_lines(self, cnode):
        for stmt in cnode.body:
            if isinstance(stmt, ast.Assign):
                for namenode in stmt.targets:
                    self.members.add(namenode.id)
            if isinstance(stmt, ast.AnnAssign):
                self.members.add(stmt.target.id)
            # if isinstance(stmt, ast.Expr):
            #     print(type(stmt))
            if isinstance(stmt, ast.FunctionDef) or isinstance(stmt, ast.AsyncFunctionDef):
                mvisitor = MethodVisitor()
                mvisitor.visit(stmt)
                self.members = self.members.union(mvisitor.members)
                # print(get_type_names(stmt.body[0].targets))
                # print(stmt.body[0].targets[0].value.id)
                # print(stmt.body[0].targets[0].attr)

def get_pyfiles(path):
    return glob(path+"/**/*.py", recursive=True)



def getAST(path: str):
    with open(path, "r") as f:
        source = f.read()

    return ast.parse(source)

class MyTracer(StackInspector):
    def __init__(self, *, file: TextIO = sys.stdout) -> None:
        """Trace a block of code, sending logs to `file` (default: stdout)"""
        self.original_trace_function: Optional[Callable] = None
        self.file = file

    def set_target(self, t):
        self.target = t

    def set_members(self, m):
        self.members = dict([(varname, set()) for varname in m])

    def traceit(self, frame: FrameType, event: str, arg: Any) -> None:
        """Tracing function. To be overridden in subclasses."""
        if frame.f_code.co_qualname.startswith(self.target):
            for m in self.members.keys():
                if "self" in frame.f_locals and hasattr(frame.f_locals["self"], m):
                    self.members[m].add(type(getattr(frame.f_locals["self"], m)).__name__)
            # self.log(event, frame.f_lineno, frame.f_code.co_name, type(frame.f_locals["file"]))

    def _traceit(self, frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
        """Internal tracing function."""
        if self.our_frame(frame):
            # Do not trace our own methods
            pass
        else:
            self.traceit(frame, event, arg)
        return self._traceit

    def __enter__(self) -> Any:
        """Called at begin of `with` block. Turn tracing on."""
        self.original_trace_function = sys.gettrace()
        sys.settrace(self._traceit)

        # This extra line also enables tracing for the current block
        # inspect.currentframe().f_back.f_trace = self._traceit
        return self

    def __exit__(self, exc_tp: Type, exc_value: BaseException,
                 exc_traceback: TracebackType) -> Optional[bool]:
        """
        Called at end of `with` block. Turn tracing off.
        Return `None` if ok, not `None` if internal error.
        """
        sys.settrace(self.original_trace_function)

        # Note: we must return a non-True value here,
        # such that we re-raise all exceptions
        if self.is_internal_error(exc_tp, exc_value, exc_traceback):
            return False  # internal error
        else:
            return None  # all ok


# def traceit(frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
    # print(frame.f_code.co_qualname)
    # print(frame.f_code.co_filename)
    # print("self" in frame.f_locals and hasattr(frame.f_locals["self"], "a"))
    # print(type(getattr(frame.f_locals["self"], "a")).__name__)
    # return traceit

def collect_variable_types(path: str, target_class: str):
    pyfiles = get_pyfiles(path)
    classcollector = ClassCollector()

    for pyfile in pyfiles:
        myast = getAST(pyfile)
        classcollector.set_path(pyfile)
        classcollector.visit(myast)

    sline = 0
    eline = 0
    members = {}

    for cname, cmap in classcollector.classmap.items():
        if target_class == cname:
            sline = cmap["ast"].lineno
            eline = cmap["ast"].end_lineno
            linecollector = MemberCollector()
            linecollector.iterate_lines(cmap["ast"])
            # print(sline, eline)
            # print(linecollector.members)
            members = linecollector.members


    tracer = MyTracer()
    tracer.set_target(target_class)
    tracer.set_members(members)

    with tracer:
        pytest.main(["-s", path])

    return tracer.members


if __name__ == '__main__':
    collect_variable_types("./src", "ThisClass")
