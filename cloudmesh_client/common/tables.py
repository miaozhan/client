"""Convenient methods and classes to print tables"""
from __future__ import print_function

from pytimeparse.timeparse import timeparse
from prettytable import PrettyTable
from datetime import datetime
from datetime import timedelta
import json
import yaml
import cloudmesh_base.hostlist

from cloudmesh_base.util import convert_from_unicode


def dict_printer(d, order=None, header=None, output="table",
                 sort_keys=True,
                 show_none=""):
    """
    TODO
    :param d: A a dict with dicts of the same type.
    :type d: dict
    :param order:The order in which the columns are printed.
                The order is specified by the key names of the dict.
    :type order:
    :param header: The Header of each of the columns
    :type header: list or tuple of field names
    :param output: type of output (table, csv, json, yaml or dict)
    :type output: string
    :param sort_keys:
    :type sort_keys: bool
    :return:
    """
    if output == "table":
        return dict_table_printer(d, order=order, header=header, sort_keys=sort_keys)
    elif output == "csv":
        return dict_csv_printer(d, order=order, header=header, sort_keys=sort_keys)
    elif output == "json":
        return json.dumps(d, sort_keys=sort_keys, indent=4)
    elif output == "yaml":
        return yaml.dump(convert_from_unicode(d), default_flow_style=False)
    elif output == "dict":
        return d
    else:
        return "UNKOWN FORMAT"


def dict_csv_printer(d, order=None, header=None, output="table", sort_keys=True):
    first_element = d.keys()[0]

    def _keys():
        return d[first_element].keys()

    def _get(element, key):
        try:
            tmp = str(d[element][key])
        except:
            tmp = ' '
        return tmp

    if d is None or d == {}:
        return None

    if order is None:
        order = _keys()

    if header is None and order is not None:
        header = order
    elif header is None:
        header = _keys()

    table = ""
    content = []
    for attribute in order:
        content.append(attribute)
    table = table + ",".join([str(e) for e in content]) + "\n"

    for job in d:
        content = []
        for attribute in order:
            try:
                content.append(d[job][attribute])
            except:
                content.append("None")
        table = table + ",".join([str(e) for e in content]) + "\n"
    return table


def dict_table_printer(d, order=None, header=None, sort_keys=True, show_none=""):
    """prints a pretty table from an dict of dicts
    :param d: A a dict with dicts of the same type.
                  Each key will be a column
    :param order: The order in which the columns are printed.
                  The order is specified by the key names of the dict.
    :param header: The Header of each of the columns
    
    """
    first_element = d.keys()[0]

    def _keys():
        return d[first_element].keys()

    def _get(item, key):
        try:
            tmp = str(d[item][key])
            if tmp == "None":
                tmp = show_none
        except:
            tmp = ' '
        return tmp

    if d is None or d == {}:
        return None

    if order is None:
        order = _keys()

    if header is None and order is not None:
        header = order
    elif header is None:
        header = _keys()

    x = PrettyTable(header)

    if sort_keys:
        sorted_list = sorted(d, key=d.get)
    else:
        sorted_list = d

    for element in sorted_list:
        values = []
        for key in order:
            values.append(_get(element, key))
        x.add_row(values)
    x.align = "l"
    return x
