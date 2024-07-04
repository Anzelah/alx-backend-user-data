#!/usr/bin/env python3
"""perform log formating"""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Use regex:re.sub to redact the password and dob values"""
    parts = message.split(separator)

    ps = parts[2].split('=')[1].strip()
    dob = parts[3].split('=')[1].strip()

    return re.sub(ps, redaction, re.sub(dob, redaction, message))


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        else:
            record.exc_text = ""

        if record.stack_info:
            record.stack_info = self.formatStack(record.stack_info)
        #combine into the final log string using format.__dict is for all the attributes        
        final_log = self.FORMAT % record.__dict__

        filtered = filter_datum(self.fields, self.REDACTION, final_log, self.SEPARATOR)
        return filtered

