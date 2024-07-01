#!/usr/bin/env python3
"""perform regex-ing"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Use regex:re.sub to redact the password and dob values"""
    ps = message.split(';')[2].split('=')[1]
    dob = message.split(';')[3].split('=')[1]

    res = re.sub(ps, redaction, re.sub(dob, redaction, message))
    return res
