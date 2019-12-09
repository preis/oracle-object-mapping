# Oracle Object Mapping

# Requirements
- Python 3.7+

# Install
```
pip install git+https://github.com/domingues/oracle-object-mapping.git
```

## Example

### Types definition
```python
import datetime
from typing import Optional

from oracle_object_mapping import objects, fields


class TABLE_VARCHARS(objects.Collection[str]):
    pass


class TABLE_CLOBS(objects.Collection[str]):
    package = 'LIBRARY'
    database_type = fields.CLOB()


class BOOK(objects.Object):
    package = 'LIBRARY'
    ID: Optional[int]
    TITLE: Optional[str]
    AUTHORS: Optional[TABLE_VARCHARS]
    DEDICATION: Optional[str] = fields.CLOB()
    PAGES: Optional[TABLE_CLOBS]
    PUBLISH_DATE: Optional[datetime.datetime]
```

### Create Objects
```python
data = ["a" * x for x in range(10)]

ta = TABLE_VARCHARS()
for x in data:
    ta.append(x)

tb = TABLE_VARCHARS.from_data(data)

# ta == tb
```

```python
ba = BOOK()
ba.TITLE = 'Hello'
ba.AUTHORS = TABLE_VARCHARS.from_data(['Alberto', 'José'])

# ba.to_data() == {'TITLE': 'HELLO', 'AUTHORS': ['Alberto', 'José']}

data = {'TITLE': 'HELLO', 'AUTHORS': ['Alberto', 'José']}
bb = BOOK.from_data(data)

# ba == bb
```

### Call function
```python
connection: cx_Oracle.connection
name = 'LIBRARY.CREATE_BOOK'
return_type = BOOK
new_book = utils.call_function(connection, name, BOOK, [ba])
print(new_book.ID)
```
