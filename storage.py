#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: storage.py
Author: HungWei Kao
Email: hungwei.kao@gmail.com
Github: https://github.com/ricky155030
Description: wrapper class for PyMySQL
"""
import pymysql.cursors
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Storage(object):

    # Singleton
    def __new__(cls, host, user, password, db):
        if not Storage._instance: 
            Storage._instance = object.__new__(cls)
        return Storage._instance

    _instance = None

    def __init__(self, host, user, password, db):
        # Establish connection
        try:
            self._conn = pymysql.connect(host=host,
                                         user=user, 
                                         password=password,
                                         db=db,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            logger.error("Cannot establish connection to database")
            logger.exception(e)
            return 

    def insert_update(self, table, data=None):
        if type(data) is not dict:
            logger.error("data should be dict type")
            return 
        
        # Generate SQL
        keys = ', '.join(data.keys())
        variable = ', '.join(['%s'] * len(data))

        update_data = list()
        update_value = list()
        for key in data:
            update_data.append(key + " = %s")
            update_value.append(data[key]) 
        update = ', '.join(update_data)

        values = list(data.values()) + update_value
        
        # Execute SQL
        with self._conn.cursor() as cursor:
            sql = "INSERT INTO " + table + " (" + keys + ") VALUES (" + variable + ") ON DUPLICATE KEY UPDATE " + update
            cursor.execute(sql, values)

        logger.debug("Execute sql: " + sql)
        logger.debug("Value: " + str(values))

        self._conn.commit();

    def select(self, table, data=None):
        if data is None: 
            sql = "SELECT * FROM " + table
        elif type(data) is not dict:
            logger.error("data should be dict type")
            return 
        else:
            condition = list()
            for key in data:
                condition.append(key + " = '%s'" % (data[key]))
            where = ', '.join(condition)
            sql = "SELECT * FROM " + table + " WHERE " + where

        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        logger.debug("Execute sql: " + sql)

        return result
