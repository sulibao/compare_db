## shell+python

提供了shell+Python的方式，修改配置信息

- source.sh
```sh
MYSQL_HOST="192.168.2.193"
MYSQL_PORT="20307"
MYSQL_USER="root"
MYSQL_PASS="SLBmysql2025"
DIR="source"

MYSQL_DBS="sulibao"
```
- target.sh
```sh
MYSQL_HOST="xx.xx.xx.xx"
MYSQL_PORT="20308"
MYSQL_USER="root"
MYSQL_PASS="xxx"
DIR="target"

MYSQL_DBS="test-su"
```
- compare.py
```python
file_map = {
    "test-su": "test-su",
}
```

```
cd /shell+python
bash source.sh
bash target.sh
python compare.py

cat compare/*.csv

```