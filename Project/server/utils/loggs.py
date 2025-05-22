

import os
import logging
import traceback
import json
from typing import Optional


class StackFrame:
    def __init__(self, func: str, source: str, line: int):
        self.func = func
        self.source = source
        self.line = line


def replace_attr(attr):
    if isinstance(attr, Exception):
        return fmt_err(attr)
    return attr


def marshal_stack(err: Exception) -> Optional[list[StackFrame]]:
    tb = traceback.extract_tb(err.__traceback__)

    if not tb:
        return None

    frames = []
    for frame in tb:
        source = os.path.basename(os.path.dirname(frame.filename))
        source_file = os.path.basename(frame.filename)
        func_name = frame.name
        line_number = frame.lineno
        frames.append(StackFrame(func_name, f"{source}/{source_file}", line_number))

    return frames


def fmt_err(err: Exception) -> dict:
    group_values = {
        "msg": str(err)
    }

    frames = marshal_stack(err)

    if frames:
        group_values["trace"] = [
            {"func": frame.func, "source": frame.source, "line": frame.line}
            for frame in frames
        ]
    
    return group_values


def get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
