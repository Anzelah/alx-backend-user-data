#!/usr/bin/env python3
"""perform regex-ing"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Use regex:re.sub to redact the password and dob values"""
    parts = message.split(separator)
    for i in range(5):
        ps = parts[2].split('=')[1].strip()
        dob = parts[3].split('=')[1].strip()
        return re.sub(ps, redaction, re.sub(dob, redaction, message))
