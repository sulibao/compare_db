# compare_db

This script can be used to compare the number of tables of the old and new databases after the migration of the MySQL family of databases.

# How to Use

- source.sh

```sh

#!/bin/bash

MYSQL_HOST="xx.xx.xx.xx"   #source database host
MYSQL_PORT="20307"   #Source database host port
MYSQL_USER="root"    #Source database user
MYSQL_PASS="xxx"     #The password of the source database login user
DIR="source"    #The directory where the source data volume is obtained is stored

MYSQL_DBS="test-su"    #The database of the comparison to be fetched, separated by "," when there are multiple databases
......

bash source.sh
```

- target.sh

```sh
#!/bin/bash
MYSQL_HOST="xx.xx.xx.xx"    #Target database host address
MYSQL_PORT="20308"      #Target database host port
MYSQL_USER="root"       #Target database user
MYSQL_PASS="xxx"       #The password of the target database login user
DIR="target"           #The directory where the target data volume is fetched   

MYSQL_DBS="test-su"      #The database of the comparison to be fetched, separated by "," when there are multiple databases
......

bash target.sh
```

- compare.py

```python
import os
import csv
file_map = {
    'test-su': 'test-su',            #'source': 'target'
    'xxx':'xxx'
}
#Fill in the name of the database to be compared, separated by "," when there are multiple sets of comparisons

source_dir = 'source'
target_dir = 'target'
output_dir = 'compare'

......

python compare.py
```

After running, check out the "*.csv" file in the compare directory to see the difference in the number of tables
