import os
import csv

file_map = {
    "sulibao": "slb",
}

source_dir = "source"
target_dir = "target"
output_dir = "compare"


def read_file(file_path):
    table_rows = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                table_name, row_count = parts
                table_rows[table_name] = int(row_count)
    return table_rows


def compare_files(source_file, target_file):
    source_path = os.path.join(source_dir, source_file)
    target_path = os.path.join(target_dir, target_file)

    source_data = read_file(source_path)
    target_data = read_file(target_path)

    results = []

    all_tables_set = set(source_data.keys()).union(set(target_data.keys()))
    all_tables = sorted(all_tables_set)
    for table in all_tables:
        source_rows = source_data.get(table, "Not found")
        target_rows = target_data.get(table, "Not found")
    if source_rows != target_rows:
        results.append(
            {
                "table name": table,
                "source rows": source_rows,
                "target rows": target_rows,
            }
        )
    return results


def write_csv(results, output_file):
    with open(output_file, "w") as file:
        writer = csv.DictWriter(
            file, fieldnames=["table name", "source rows", "target rows"]
        )
        writer.writeheader()
        for result in results:
            writer.writerow(result)


def main():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for source_file, target_file in file_map.items():
        # Add file extension
        source_file = source_file + ".txt"
        target_file = target_file + ".txt"

        source_path = os.path.join(source_dir, source_file)
        target_path = os.path.join(target_dir, target_file)

        if not os.path.exists(source_path):
            print("Source file does not exist: {}".format(source_file))
            continue
        if not os.path.exists(target_path):
            print("Target file does not exist: {}".format(target_file))
            continue

        results = compare_files(source_file, target_file)

        # Generate CSV file name
        output_file = os.path.join(
            output_dir, "{}_comparison.csv".format(source_file[:-4])
        )
        write_csv(results, output_file)
        print(
            "Comparison complete for {}. Results saved to {}".format(
                source_file, output_file
            )
        )


if __name__ == "__main__":
    main()
