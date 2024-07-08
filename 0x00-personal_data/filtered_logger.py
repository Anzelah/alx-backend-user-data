#!/usr/bin/env python3
"""perform log formating"""

import logging
import re
from typing import List
import csv
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Use regex:re.sub to redact the password and dob values"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
                         f'{i}={redaction}{separator}', message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        final_log = self.FORMAT % record.__dict__

        return filter_datum(self.fields, self.REDACTION,
                            final_log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Return a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # create handler
    c_handler = logging.StreamHandler()
    # create formatter and add it to handler
    Redacting = RedactingFormatter(logging.Formatter)
    c_formatter = logging.Formatter(Redacting)
    c_handler.setFormatter(c_formatter)
    # add handler to logger
    logger.addHandler(c_handler)

    return logger


PII_FIELDS: tuple = ('name', 'email', 'phone', 'ssn', 'password')
with open('user_data.csv', newline='') as f, open(
          str(PII_FIELDS), 'w', newline='') as output:
    reader = csv.reader(f)
    writer = csv.writer(output)

    for row in reader:
        writer.writerow(row[:5])


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a secure database and then
    return a connector(object) to the database"""
    # connect to a secure server
    connection = mysql.connector.connect(
            user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
            host=os.getenv('PERSONAL_DATA_DB_HOST'),
            database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return connection
