import os
import pg8000
import pg8000.exceptions
import argparse
import csv

def fetch_table_row_counts(config, databases, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print("{} directory created successfully".format(output_directory))
    else:
        print("The directory {} already exists".format(output_directory))

    for db_name in databases:
        current_config = config.copy()
        current_config['database'] = db_name

        table_file = os.path.join(output_directory, "{}.table".format(db_name))
        output_file = os.path.join(output_directory, "{}.txt".format(db_name))

        connection = None
        cursor = None
        try:
            connection = pg8000.connect(**current_config)
            cursor = connection.cursor()

            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
            tables = [row[0] for row in cursor.fetchall()]

            with open(table_file, 'w') as f:
                for table in tables:
                    f.write("{}\n".format(table))

            with open(output_file, 'w') as f:
                pass

            for table in tables:
                query = "SELECT %s, COUNT(1) FROM \"{}\"".format(table)
                cursor.execute(query, (table,))
                result = cursor.fetchone()

                if result:
                    with open(output_file, 'a') as f:
                        f.write("{}\t{}\n".format(result[0], result[1]))

            print("Query results for database {} have been saved to: {}".format(db_name, output_file))

        except (pg8000.exceptions.InterfaceError, pg8000.exceptions.ProgrammingError) as e:
            print("Error accessing database {}: {}".format(db_name, e))
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

def read_file(file_path):
    table_rows = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    table_name, row_count = parts
                    table_rows[table_name] = int(row_count)
    except FileNotFoundError:
        print("Error: File not found at {}".format(file_path))
    return table_rows

def compare_files(source_dir, target_dir, file_map):
    results_all = []
    for source_db_name, target_db_name in file_map.items():
        source_file = os.path.join(source_dir, "{}.txt".format(source_db_name))
        target_file = os.path.join(target_dir, "{}.txt".format(target_db_name))

        if not os.path.exists(source_file):
            print("Source file does not exist: {}".format(source_file))
            continue
        if not os.path.exists(target_file):
            print("Target file does not exist: {}".format(target_file))
            continue

        source_data = read_file(source_file)
        target_data = read_file(target_file)

        comparison_results = []
        all_tables_set = set(source_data.keys()).union(set(target_data.keys()))
        all_tables = sorted(list(all_tables_set))

        for table in all_tables:
            source_rows = source_data.get(table, "Not found")
            target_rows = target_data.get(table, "Not found")
            if source_rows != target_rows:
                comparison_results.append(
                    {
                        "table name": table,
                        "source rows": source_rows,
                        "target rows": target_rows,
                    }
                )
        results_all.extend(comparison_results)
    return results_all

def write_csv(results, output_file):
    if not results:
        print("No differences found, skipping CSV creation for {}".format(output_file))
        return
    with open(output_file, "w", newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=["table name", "source rows", "target rows"]
        )
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print("Comparison results saved to {}".format(output_file))

def main():
    parser = argparse.ArgumentParser(description="Compare database table row counts.")
    parser.add_argument('--source_host', type=str, default='192.168.2.193', help='Source database host.')
    parser.add_argument('--source_port', type=int, default=25432, help='Source database port.')
    parser.add_argument('--source_user', type=str, default='postgres', help='Source database user.')
    parser.add_argument('--source_password', type=str, default='postgres', help='Source database password.')
    parser.add_argument('--source_databases', type=str, default='slb', help='Comma-separated list of source databases.')
    parser.add_argument('--target_host', type=str, default='192.168.2.193', help='Target database host.')
    parser.add_argument('--target_port', type=int, default=25433, help='Target database port.')
    parser.add_argument('--target_user', type=str, default='postgres', help='Target database user.')
    parser.add_argument('--target_password', type=str, default='postgres', help='Target database password.')
    parser.add_argument('--target_databases', type=str, default='sulibao', help='Comma-separated list of target databases.')
    parser.add_argument('--output_dir', type=str, default='compare_results', help='Directory to save comparison results.')
    parser.add_argument('--source_output_dir', type=str, default='source_data', help='Directory to save source database data.')
    parser.add_argument('--target_output_dir', type=str, default='target_data', help='Directory to save target database data.')
    parser.add_argument('--file_map', type=str, default='slb:sulibao', help='Comma-separated key-value pairs for file mapping (e.g., source_db1:target_db1,source_db2:target_db2).')

    args = parser.parse_args()

    source_config = {
        'host': args.source_host,
        'port': args.source_port,
        'user': args.source_user,
        'password': args.source_password,
        'database': args.source_databases.split(',')[0]
    }
    target_config = {
        'host': args.target_host,
        'port': args.target_port,
        'user': args.target_user,
        'password': args.target_password,
        'database': args.target_databases.split(',')[0]
    }

    source_databases = args.source_databases.split(',')
    target_databases = args.target_databases.split(',')

    # Parse file_map argument
    file_map_parsed = {}
    for item in args.file_map.split(','):
        if ':' in item:
            k, v = item.split(':', 1)
            file_map_parsed[k.strip()] = v.strip()

    print("Fetching source database data...")
    fetch_table_row_counts(source_config, source_databases, args.source_output_dir)

    print("Fetching target database data...")
    fetch_table_row_counts(target_config, target_databases, args.target_output_dir)

    print("Comparing data...")
    comparison_results = compare_files(args.source_output_dir, args.target_output_dir, file_map_parsed)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    output_csv_path = os.path.join(args.output_dir, 'comparison_summary.csv')
    write_csv(comparison_results, output_csv_path)

    print("Comparison process completed.")

if __name__ == "__main__":
    main()