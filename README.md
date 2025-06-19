# 数据库对比工具

此工具用于对比两个数据库（源数据库和目标数据库）中表的行数，并报告任何差异。可以通过命令行参数进行配置。

## 功能
- 从源数据库获取表行数。
- 从目标数据库获取表行数。
- 对比获取到的数据并识别差异。
- 将对比结果保存到 CSV 文件。
- 所有配置（数据库连接、输出目录、数据库映射）均可通过命令行参数进行配置。

## 建议条件
- Python 3.12
- MySQL Connector/Python:8.0.28 库

## 安装
1. 克隆此仓库：
   ```bash
   git clone <repository_url>
   cd compare_db
   ```
2. 安装所需的 Python 包：
   ```bash
   pip3 install -r requirements.txt
   ```

## 使用方法
运行 `main.py` 脚本并传入所需的命令行参数。如果未提供任何参数，将使用默认值。

```bash
python main.py [OPTIONS]
```

### 命令行选项
- `--source_host` (str): 源数据库主机。默认值: `192.168.2.193`
- `--source_port` (int): 源数据库端口。默认值: `20307`
- `--source_user` (str): 源数据库用户。默认值: `root`
- `--source_password` (str): 源数据库密码。默认值: `SLBmysql2025`
- `--source_databases` (str): 要对比的源数据库列表，以逗号分隔。默认值: `sulibao`

- `--target_host` (str): 目标数据库主机。默认值: `192.168.2.193`
- `--target_port` (int): 目标数据库端口。默认值: `20308`
- `--target_user` (str): 目标数据库用户。默认值: `root`
- `--target_password` (str): 目标数据库密码。默认值: `SLBmysql2025`
- `--target_databases` (str): 要对比的目标数据库列表，以逗号分隔。默认值: `slb`

- `--output_dir` (str): 保存最终对比 CSV 报告的目录。默认值: `compare_results`
- `--source_output_dir` (str): 保存中间源数据库数据的目录。默认值: `source_data`
- `--target_output_dir` (str): 保存中间目标数据库数据的目录。默认值: `target_data`

- `--file_map` (str): 用于映射源数据库到目标数据库的逗号分隔键值对。格式: `source_db1:target_db1,source_db2:target_db2`。默认值: `sulibao:slb`

### 示例用法
```bash
python main.py --source_host 192.168.2.193 --source_port 20307 --source_user root --source_password SLBmysql2025 --source_databases sulibao --target_host 192.168.2.193 --target_port 20308 --target_user root --target_password SLBmysql2025 --target_databases slb --file_map sulibao:slb --output_dir compare_results
```

## 可以进行构建二进制可执行文件（可选）
要创建单个可执行文件，需要使用 `PyInstaller`。

1. 安装 PyInstaller：
   ```bash
   pip install pyinstaller
   ```
2. 构建可执行文件：
   ```bash
   pyinstaller --onefile main.py
   ```
   可执行文件将在 `dist/` 目录中找到。

### 运行二进制文件
```bash
./dist/main [OPTIONS]，[OPTIONS和上述参数一致]
```
（在 Windows 上，则是 `dist\main.exe [OPTIONS]`)