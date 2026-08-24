# models.py
import csv
from datetime import date
from pathlib import Path


class SettingsModel:
    """Settings model for storing and persisting application configurations."""

    fields = {
        "autofill date": {"type": "bool", "value": True},
        "autofill sheet data": {"type": "bool", "value": True},
        "font size": {"type": "int", "value": 9},
        "font family": {"type": "str", "value": ""},
        "theme": {"type": "str", "value": "clam"},
    }

    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.variables = {}

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                raw_values = eval(file.read())
        except (FileNotFoundError, SyntaxError, NameError):
            raw_values = {}

        for key, info in self.fields.items():
            val = raw_values.get(key, info["value"])
            self.variables[key] = val

        return self

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write("{\n")
            keys = list(self.fields.keys())
            for index, key in enumerate(keys):
                value = self.variables.get(key, self.fields[key]["value"])
                if isinstance(value, str):
                    rendered = f"'{value}'"
                else:
                    rendered = str(value)
                comma = "," if index < len(keys) - 1 else ""
                file.write(f"    '{key}': {rendered}{comma}\n")
            file.write("}\n")

    def get(self, key):
        return self.variables.get(key, self.fields[key]["value"])

    def set(self, key, value):
        self.variables[key] = value


class CSVModel:
    """CSV file model for data entry records."""

    fieldnames = [
        "Date",
        "Time",
        "Technician",
        "Lab",
        "Plot",
        "Seed sample",
        "Humidity",
        "Light",
        "Temperature",
        "Equipment Fault",
        "Plants",
        "Blossoms",
        "Fruit",
        "Min Height",
        "Max Height",
        "Median Height",
        "Notes",
    ]

    def __init__(self, filename):
        self.filename = filename
        self.records = []
        self.load()

    def load(self):
        """Load CSV records."""
        file_path = Path(self.filename)
        self.records = []

        print("Running CSVModel.load from:", __file__)
        print("Reading CSV file:", file_path.resolve())

        if not file_path.is_file():
            raise FileNotFoundError(
                f"CSV file does not exist:\n{file_path.resolve()}"
            )

        with file_path.open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
        ) as csv_file:
            sample = csv_file.read(8192)
            csv_file.seek(0)

            print("CSV sample:", repr(sample[:300]))

            if not sample.strip():
                raise ValueError(
                    f"CSV file is empty:\n{file_path.resolve()}"
                )

            try:
                dialect = csv.Sniffer().sniff(
                    sample,
                    delimiters=",;\t|",
                )
            except csv.Error:
                dialect = csv.excel

            reader = csv.DictReader(
                csv_file,
                dialect=dialect,
            )

            print("Detected delimiter:", repr(dialect.delimiter))
            print("Detected headers:", reader.fieldnames)

            if reader.fieldnames is None:
                raise ValueError(
                    f"CSV file has no header:\n{file_path.resolve()}"
                )

            expected_names = {
                field.strip().casefold(): field
                for field in self.fieldnames
            }

            header_mapping = {}

            for original_name in reader.fieldnames:
                if original_name is None:
                    continue

                cleaned_name = original_name.strip()
                canonical_name = expected_names.get(
                    cleaned_name.casefold()
                )

                if canonical_name:
                    header_mapping[original_name] = canonical_name

            rows_seen = 0

            for raw_row in reader:
                print("Raw CSV row:", raw_row)

                values = [
                    str(value).strip()
                    for key, value in raw_row.items()
                    if key is not None and value is not None
                ]

                extra_values = raw_row.get(None, [])

                if isinstance(extra_values, str):
                    extra_values = [extra_values]

                extra_values = [
                    str(value).strip()
                    for value in extra_values
                    if value is not None and str(value).strip()
                ]

                if not any(values) and not extra_values:
                    continue

                rows_seen += 1

                record = {
                    field: ""
                    for field in self.fieldnames
                }

                for original_name, value in raw_row.items():
                    if original_name is None:
                        continue

                    canonical_name = header_mapping.get(original_name)

                    if canonical_name is not None:
                        record[canonical_name] = (
                            str(value).strip()
                            if value is not None
                            else ""
                        )

                if extra_values:
                    extra_text = " | ".join(extra_values)
                    existing_notes = record["Notes"]

                    record["Notes"] = (
                        f"{existing_notes} | {extra_text}"
                        if existing_notes
                        else extra_text
                    )

                self.records.append(record)

            print(
                f"CSV parser finished: "
                f"rows_seen={rows_seen}, "
                f"records={len(self.records)}"
            )

    def save(self, filename=None):
        if filename is not None:
            self.filename = filename

        if not self.filename:
            raise ValueError("No CSV filename specified.")

        with open(self.filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(self.records)

    def add_record(self, record):
        self.records.append(dict(record))

    def update_record(self, row_number, record):
        self.records[row_number] = dict(record)

    def get_record(self, row_number):
        return dict(self.records[row_number])

    def get_records(self):
        return [dict(record) for record in self.records]

    def __len__(self):
        return len(self.records)

    def get_all_records(self):
        return [record.copy() for record in self.records]
