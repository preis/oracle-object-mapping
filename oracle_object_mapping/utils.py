from typing import Any, Dict, List, TypeVar

import cx_Oracle

from . import objects


def oracle_object_to_data(obj: cx_Oracle.Object) -> Any:
    if not isinstance(obj, cx_Oracle.Object):
        return obj
    if obj.type.iscollection:
        return [oracle_object_to_data(o) for o in obj.aslist()]
    data = {}
    for attr in obj.type.attributes:
        data[attr.name] = oracle_object_to_data(obj.__getattribute__(attr.name))
    return data


T = TypeVar('T', bound=objects.Base)


def call_function(connection: cx_Oracle.Connection, name: str, return_type: T, args: List[Any] = None,
                  kwargs: Dict[str, Any] = None) -> T:
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    with connection.cursor() as cursor:
        r_type = connection.gettype(return_type.__type_name__)
        args_ = [v.to_oracle_object(connection) if isinstance(v, objects.Base) else v for v in args]
        kwargs_ = {k: (v.to_oracle_object(connection) if isinstance(v, objects.Base) else v) for k, v in kwargs.items()}
        obj = cursor.callfunc(name, r_type, args_, kwargs_)
        return return_type.from_oracle_object(obj)
