import os
import mysql.connector
from mysql.connector import Error

# 配置信息
config = {
    'host': '192.168.2.193',
    'port': 20308,
    'user': 'root',
    'password': 'SLBmysql2025',
    'database': '',
    'raise_on_warnings': True
}

# 数据库列表
databases = ['slb']

# 创建保存结果的目录
directory = 'target'
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"{directory} directory created successfully")
else:
    print(f"The directory {directory} already exists")

# 遍历每个数据库
for db_name in databases:
    config['database'] = db_name
    
    # 获取所有表名
    table_file = os.path.join(directory, f"{db_name}.table")
    output_file = os.path.join(directory, f"{db_name}.txt")
    
    try:
        # 连接数据库获取表名
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema=%s ORDER BY table_name", (db_name,))
        tables = [row[0] for row in cursor.fetchall()]
        
        # 保存表名到文件
        with open(table_file, 'w') as f:
            for table in tables:
                f.write(f"{table}\n")
        
        # 清空或创建结果文件
        with open(output_file, 'w') as f:
            pass
            
        # 查询每个表的行数
        for table in tables:
            # 防止SQL注入，使用参数化查询
            query = f"SELECT %s, COUNT(1) FROM `{table}`"
            cursor.execute(query, (table,))
            result = cursor.fetchone()
            
            if result:
                with open(output_file, 'a') as f:
                    f.write(f"{result[0]}\t{result[1]}\n")
        
        print(f"Query results for database {db_name} have been saved to: {output_file}")
        
    except Error as e:
        print(f"Error accessing database {db_name}: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()