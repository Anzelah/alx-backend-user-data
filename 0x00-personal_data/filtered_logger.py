#!/usr/bin/env python3
"""perform log formating"""

import logging
import re
from typing import List
import csv
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    c_formatter = RedactingFormatter(fields=list(PII_FIELDS))
    c_handler.setFormatter(c_formatter)
    # add handler to logger
    logger.addHandler(c_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a secure database and then
    return a connector(object) to the database"""
    # connect to a secure server

    connection = mysql.connector.connect(
            user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return connection


def main() -> None:
    """
    Obtain a database connection using get_db and retrieve all rows
    in the users table and display each row under a filtered format

    Returns: Nothing
    """
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute(
            "SELECT * FROM users;")
    rows = cursor.fetchall()
    fields = cursor.column_names
    logger = get_logger()

    for row in rows:
        attach = '; '.join(f'{i}={j}' for i, j in zip(fields, row))
        logger.info(attach)

    cursor.close()
    db_connection.close()


if __name__ == '__main__':
    main()
