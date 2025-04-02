# compare_db

此脚本可用于MySQL家族系列数据库迁移之后进行新旧数据库的表数量比对。

# 使用方式

- source.sh

```sh

#!/bin/bash

MYSQL_HOST="xx.xx.xx.xx"   #源数据库主机地址
MYSQL_PORT="20307"   #源数据库主机端口
MYSQL_USER="root"    #源数据库用户
MYSQL_PASS="xxx"     #源数据库登录用户的密码
DIR="source"    #存放获取的源数据量目录

MYSQL_DBS="test-su"    #需要获取的比对的数据库，有多个数据库时用","分隔
......

bash source.sh
```

- target.sh

```sh
#!/bin/bash
MYSQL_HOST="xx.xx.xx.xx"    #目标数据库主机地址 
MYSQL_PORT="20308"      #目标数据库主机端口
MYSQL_USER="root"       #目标数据库用户
MYSQL_PASS="xxx"       #目标数据库登录用户的密码
DIR="target"           #存放获取的目标数据量目录   

MYSQL_DBS="test-su"      #需要获取的比对的数据库，有多个数据库时用","分隔
......

bash target.sh
```

- compare.py

```python
import os
import csv
file_map = {
    'test-su': 'test-su',
    'xxx':'xxx'
}                     #填写需要比对的数据库名称，有多组比对时用","分隔

source_dir = 'source'
target_dir = 'target'
output_dir = 'compare'

......

python compare.py
```

运行完毕后查看compare目录下的"*.csv"文件以查看表数量对比差异
