# Database comparison tool for PostgreSQL

This tool is used to compare the number of rows in the tables of two databases (the source database and the target database, in this branch for PostgreSQL database), and report any differences. It is configured through command-line parameters.

## Function

- Retrieve the number of rows from the target database.
- Compare the obtained data and identify the differences.
- Save the comparison results to a CSV file.
- All configurations (database connection, output directory, database mapping) can be configured through command-line parameters. Configure through command-line parameters.

## Suggested operating environment

- Python 3.7.0 and above
- Pip/Pip3
- pg8000 1.29.4 lib

## Install

1. Clone this repository and grant execution permissions:
   ```bash
   git clone <repository_url> -b postgresql_python
   chmod +x -R compare_db
   cd compare_db
   ```
2. Installing the required Python packages:

   ```bash
   pip3 install -r requirements.txt
   ```
   Note: When executing the above Python/pip commands on relatively new versions of Ubuntu, you may encounter the "PEP 668 Python Management Limitation". In such cases, it is recommended to create a virtual environment for operation as follows.

   ```bash
   python3 -m venv myenv
   source /myenv/bin/activate
   pip3 install -r requirements.txt
   deactivate
   ```

## Method of application

Run the `main.py` script and pass in the required command-line parameters. If no parameters are provided, the default values will be used.

```bash
python3 main.py [OPTIONS]
```

### Command Options

`You can invoke the help information by running "python3 main.py --help/-h".`
- `--source_host` (str): Source database host.default: `192.168.2.193`
- `--source_port` (int): Source database port.default: `25432`
- `--source_user` (str): Source database user.default: `postgres`
- `--source_password` (str): Source database password.default: `postgres`
- `--source_databases` (str): The list of source databases to be compared, separated by commas in English format.default: `slb`

- `--target_host` (str): Target database host.default: `192.168.2.193`
- `--target_port` (int): Target database port.default: `25433`
- `--target_user` (str): Target database user.default: `postgres`
- `--target_password` (str): Target database password.default: `postgres`
- `--target_databases` (str): The list of target databases to be compared, separated by commas in English format.default: `sulibao`

- `--output_dir` (str): Directory for saving the final comparison CSV report.default: `compare_results`
- `--source_output_dir` (str): The directory for storing the data of the intermediate source database.default: `source_data`
- `--target_output_dir` (str): The directory for storing the data of the intermediate target database.default: `target_data`

- `--file_map` (str): Comma-separated key-value pairs used to map the source database to the target database.format: `source_db1:target_db1,source_db2:target_db2`。default: `slb:sulibao`

### Example

```bash
python main.py --source_host 192.168.2.193 --source_port 25432 --source_user postgres --source_password SLBpg2025 --source_databases slb --target_host 192.168.2.193 --target_port 25433 --target_user postgres --target_password SLBmysql2025 --target_databases sulibao --file_map slb:sulibao --output_dir compare_results
```

## Binary executable files can be constructed (optional operation)

To create a single executable file, you need to use `PyInstaller`

1. Install PyInstaller：
   ```bash
   pip3 install pyinstaller
   ```
2. Build executable file:
   ```bash
   pyinstaller --onefile main.py
   ```
   The executable file can be found in the `./dist/` directory

## Run the binary file (optional operation)

1. Linux(./dist/main)，The execution results are as follows:
```bash
(myenv) root@sulibao-None:~/compare_db/dist# ./main --source_host 192.168.2.193 --source_port 25432 --source_user postgres --source_password SLBpg2025 --source_databases slb --target_host 192.168.2.193 --target_port 25433 --target_user postgres --target_password SLBpg2025 --target_databases sulibao --file_map slb:sulibao --output_dir compare_results
Fetching source database data...
source_data directory created successfully
Query results for database slb have been saved to: source_data/slb.txt
Fetching target database data...
target_data directory created successfully
Query results for database sulibao have been saved to: target_data/sulibao.txt
Comparing data...
Comparison results saved to compare_results/comparison_summary.csv
Comparison process completed.

(myenv) root@sulibao-None:~/compare_db/dist# cat compare_results/comparison_summary.csv 
table name,source rows,target rows     
# At this moment, only this plugin table has a slight quantity difference. All other tables without quantity differences will not be displayed.
pg_stat_statements,106,96
```

2. Windows(.\dist\main.exe)，The execution results are as follows:

```bash
E:\> .\dist\main.exe --source_host 192.168.2.193 --source_port 25432 --source_user postgres --source_password SLBpg2025 --source_databases slb --target_host 192.168.2.193 --target_port 25433 --target_user postgres --target_password SLBpg2025 --target_databases sulibao --file_map slb:sulibao --output_dir compare_results
Fetching source database data...
source_data directory created successfully
Query results for database slb have been saved to: source_data\slb.txt
Fetching target database data...
target_data directory created successfully
Query results for database sulibao have been saved to: target_data\sulibao.txt
Comparing data...
Comparison results saved to compare_results\comparison_summary.csv
Comparison process completed.

E:\> notepad.exe compare_results/comparison_summary.csv
table name,source rows,target rows          
# At this moment, only this plugin table has a slight quantity difference. All other tables without quantity differences will not be displayed.
pg_stat_statements,106,96
```

3. Example binary file

```bash
./dist/windows/main.exe--Built based on Windows 11 Professional Edition (amd_X64)
./dist/Linux/main---Built based on Ubuntu 24.04.2 LTS (x86_64)
```