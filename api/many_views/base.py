from django.db import connection


def execute_many_sql(cursor, sql, lst=None):
    """
    :param cursor: 游标
    :param sql: 执行的sql语句
    :param lst: sql的参数列表
    :return: 查询结果
    """
    if lst is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, lst)
    raw_data = cursor.fetchall()
    return raw_data


def dict_fetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def copy_dict_fetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    print(columns)
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_one_and_many_data(sql, lst=None, data_len=None):
    with connection.cursor() as cursor:
        raw_data = execute_many_sql(cursor, sql=sql, lst=lst)
        if data_len is not None:
            diseases_dict = {}
            for raw in raw_data:
                if raw[data_len] not in diseases_dict.keys():
                    diseases_dict[raw[data_len]] = []
                dict_tup = {}
                for i, desc in enumerate(cursor.description):
                    if i < data_len:
                        dict_tup[i] = raw[i]
                        dict_tup[desc[0]] = raw[i]
                diseases_dict[raw[data_len]].append(dict_tup)
            return diseases_dict
        else:
            lst = []
            for raw in raw_data:
                dict_tup = {}
                for i, desc in enumerate(cursor.description):
                    dict_tup[i] = raw[i]
                    dict_tup[desc[0]] = raw[i]
                lst.append(dict_tup)
            return lst


def execute_page_sql(cursor, sql, lst=None):
    if lst is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, lst)
    raw_data = cursor.fetchall()
    lst = []
    for raw in raw_data:
        lst.append(dict([(desc[0], raw[i]) for i, desc in enumerate(cursor.description)]))
    return lst