import csv
import os
import json
from pathlib import Path
from .constants import FiledTypes as FT

class CSVModel:
    """CSV file storage"""

    fields = {
        "Date": {'req': True, 'type': FT.iso_date_string},
        "Time": {'req': True, 'type': FT.string_list,
                 'values': ['8:00', '12:00', '16:00', '20:00']},
        "Technician": {'req': True, 'type': FT.string},
        "Lab": {'req': True, 'type': FT.string_list,
                'values': ['A', 'B', 'C', 'D', 'E']},
        "Plot": {'req': True, 'type': FT.string_list,
                 'values': [str(x) for x in range(1, 21)]},
        "Seed sample":  {'req': True, 'type': FT.string},
        "Humidity": {'req': True, 'type': FT.decimal,
                     'min': 0.5, 'max': 52.0, 'inc': .01},
        "Light": {'req': True, 'type': FT.decimal,
                  'min': 0, 'max': 100.0, 'inc': .01},
        "Temperature": {'req': True, 'type': FT.decimal,
                        'min': 4, 'max': 40, 'inc': .01},
        "Equipment Fault": {'req': False, 'type': FT.boolean},
        "Plants": {'req': True, 'type': FT.integer,
                   'min': 0, 'max': 20},
        "Blossoms": {'req': True, 'type': FT.integer,
                     'min': 0, 'max': 1000},
        "Fruit": {'req': True, 'type': FT.integer,
                  'min': 0, 'max': 1000},
        "Min Height": {'req': True, 'type': FT.decimal,
                       'min': 0, 'max': 1000, 'inc': .01},
        "Max Height": {'req': True, 'type': FT.decimal,
                       'min': 0, 'max': 1000, 'inc': .01},
        "Median Height": {'req': True, 'type': FT.decimal,
                          'min': 0, 'max': 1000, 'inc': .01},
        "Notes": {'req': False, 'type': FT.long_string}
    }

    def __init__(self, filename):
        self.file = Path(filename)

    def save_record(self, data, rownum=None):
        """Save a dict of data to the CSV file"""
        if rownum is None:
            newfile = not self.file.exists()
            with open(self.file, 'a', encoding='utf-8', newline='') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                if newfile:
                    csvwriter.writeheader()
                csvwriter.writerow(data)
        else:
            records = self.get_all_records()
            records[rownum] = data
            with open(self.file, 'w', encoding='utf-8', newline='') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                csvwriter.writeheader()
                csvwriter.writerows(records)

    def get_all_records(self):

        if not self.file.exists():
            return []
        with open(self.file, 'r', encoding='utf-8') as fh:
            csvreader = csv.DictReader(fh)
            missing_fields = (
                set(self.fields.keys()) - set(csvreader.fieldnames)
            )
            if len(missing_fields) > 0:
                fields_string = ", ".join(missing_fields)
                raise Exception(
                    f"File is missing fields: {fields_string}"
                )
            records = list(csvreader)
            trues = ('true', 'yes', '1')
            bool_fields = [
                key for key, meta
                in self.fields.items()
                if meta['type'] == FT.boolean
            ]
            for record in records:
                for key in bool_fields:
                    record[key] = record[key].lower() in trues
        return records

    def get_record(self, rownum):
        return self.get_all_records()[rownum]


class SettingsModel:
    """A model for saving settings"""

    variables = {
        'autofill date': {'type': 'bool', 'value': True},
        'autofill sheet data': {'type': 'bool', 'value': True}
    }

    def __init__(self, filename='saba_settings.json', path='~'):
        self.filepath = os.path.join(os.path.expanduser(path), filename)
        self.load()

    def set(self, key, value):
        if (
            key in self.variables and
            type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

    def save(self, settings=None):
        """Save the current settings to the file"""
        json_string = json.dumps(self.variables)
        with open(self.filepath, 'w') as fh:
            fh.write(json_string)

    def load(self):
        """Load the settings from the file"""

        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, 'r') as fh:
            raw_values = json.loads(fh.read())

        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value
