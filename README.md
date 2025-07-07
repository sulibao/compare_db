## python_old，建议python版本>=3.6

- source.py

```sh
pip install mysql-connector-python

config = {
    'host': '192.168.2.193',   #原数据库host
    'port': 20307,     #原数据库端口
    'user': 'root',    #原数据库登录用户
    'password': 'SLBmysql2025',   #原数据库登录密码
    'database': '',    #原数据库列表，初始为空，后面会遍历数据库列表的值
    'raise_on_warnings': True
}

# 数据库列表
databases = ['sulibao']

python source.py
```

- target.py

```sh
config = {
    'host': '192.168.2.193',    #目标数据库host
    'port': 20308,       #目标数据库端口
    'user': 'root',    #目标数据库登录用户
    'password': 'SLBmysql2025',   #目标数据库登录密码
    'database': '',           #目标数据库列表，初始为空，后面会遍历数据库列表的值
    'raise_on_warnings': True
}

# 数据库列表
databases = ['slb']

python target.py
```

- compare.py

```python
import os
import csv

file_map = {
    "sulibao": "slb",    #"原数据库": "目标数据库"，如果有多个库需要对比，可以换行继续写 
}

source_dir = "source"    #存放原数据的目录
target_dir = "target"    #存放目标数据的目录
output_dir = "compare"   #存放对比结果的目录

......

python compare.py
```

运行后，查看compare目录中的“*.csv”文件，以查看表数量的差异