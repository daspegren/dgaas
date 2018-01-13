#!/usr/bin/python

from ConfigParser import SafeConfigParser
from collections import defaultdict
import mysql.connector
from impala.dbapi import connect

CONFIG_FILE_PATH = '/home/maria_dev/ingestion/conf/ingestion_config.ini'
config_parser = SafeConfigParser()
config_parser.read(CONFIG_FILE_PATH)


def default_config_path():
    """
    Returns the default configuration file path
    :return: CONFIG_FILE_PATH
    :rtype: string
    """
    return CONFIG_FILE_PATH

def get_config_dict(ini_file_path=None):
    """
    Read the configuration file and return its contents as a dictionary
    :param ini_file_path: Optional path to an alternative configuration file
    :type ini_file_path: string
    :return: A dictionary that contains all the information in the configuration file
    :rtype: dict
    """
    if ini_file_path is not None:
        config_parser.read(ini_file_path)
    dict_config = defaultdict(dict)
    for section in config_parser.sections():
        for option, value in config_parser.items(section):
            dict_config[section][option] = value
    return dict(dict_config)

def connect_to_mysql(config=None, section=None):
    """
    Establish a connection to MySQL server
    :param config: Optional configuration dictionary
    :type config: dict
    :param section: Optional name of the MySQL section in the config dictionary
    :type section: string
    :return: A mysql.connector connection that connects to MySQL
    :rtype: mysql.connector connection
    """
    if config is None:
        config = get_config_dict()
    if section is None:
        section = "MySQL"
    MySQL = config[section]
    return mysql.connector.connect(user=MySQL["user"], password=MySQL["password"], database=MySQL["database"], host=MySQL["host"])

def connect_to_hive(config=None, section=None):
    """
    Establish a connection to Hive server
    :param config: Optional configuration dictionary
    :type config: dict
    :param section: Optional name of the Hive section in the config dictionary
    :type section: string
    :return: A Impala connection that connects to hive
    :rtype: Impala connection
    """
    if config is None:
        config = get_config_dict()
    if section is None:
        section = "Hive"
    HIVE = config[section]
    return connect(host=HIVE["host"], port=HIVE["port"], auth_mechanism=HIVE["auth"], user=HIVE["user"], password=HIVE["password"])
