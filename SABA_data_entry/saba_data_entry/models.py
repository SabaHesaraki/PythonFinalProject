from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import psycopg2 as pg
from psycopg2.extras import RealDictCursor

RowKey = Tuple[str, str, str, str]


class SettingsModel:
    fields = {
        "theme": {"type": "str", "default": "clam"},
        "font size": {"type": "int", "default": 10},
        "font family": {"type": "str", "default": "Segoe UI"},
        "autofill sheet data": {"type": "bool", "default": True},
    }

    def __init__(self, filename: str = "settings.json"):
        self.path = Path(filename)
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def _save(self) -> None:
        try:
            self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
        except Exception:
            pass

    def get(self, key: str) -> Any:
        if key in self._data:
            return self._data[key]
        info = self.fields.get(key, {"default": ""})
        return info.get("default", "")

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()


class SQLModel:
    table_name = "plot_checks"

    fields = {
        "Date": {"req": True, "type": "str"},
        "Time": {
            "req": True,
            "type": "str",
            "values": ["08:00:00", "12:00:00", "16:00:00", "20:00:00"],
        },
        "Lab": {
            "req": True,
            "type": "str",
            "values": ["A", "B", "C", "D", "E"],
        },
        "Plot": {
            "req": True,
            "type": "str",
            "values": [str(i) for i in range(1, 21)],
        },
        "Seed Sample": {"req": True, "type": "str"},
        "Humidity": {
            "req": True,
            "type": "decimal",
            "range": (0.0, 100.0),
            "inc": 0.1,
        },
        "Light": {
            "req": True,
            "type": "decimal",
            "range": (0.0, 100.0),
            "inc": 0.1,
        },
        "Temperature": {
            "req": True,
            "type": "decimal",
            "range": (4.0, 40.0),
            "inc": 0.1,
        },
        "Equipment Fault": {
            "req": False,
            "type": "bool",
            "values": ["False", "True"],
        },
        "Blossoms": {"req": False, "type": "int", "range": (0, 1000)},
        "Plants": {"req": False, "type": "int", "range": (0, 1000)},
        "Fruit": {"req": False, "type": "int", "range": (0, 1000)},
        "Min Height": {
            "req": False,
            "type": "decimal",
            "range": (0.0, 1000.0),
            "inc": 0.01,
        },
        "Max Height": {
            "req": False,
            "type": "decimal",
            "range": (0.0, 1000.0),
            "inc": 0.01,
        },
        "Median Height": {
            "req": False,
            "type": "decimal",
            "range": (0.0, 1000.0),
            "inc": 0.01,
        },
        "Notes": {"req": False, "type": "str"},
    }

    db_map = {
        "Date": "date",
        "Time": "time",
        "Lab": "lab_id",
        "Plot": "plot",
        "Seed Sample": "seed_sample",
        "Humidity": "humidity",
        "Light": "light",
        "Temperature": "temperature",
        "Equipment Fault": "equipment_fault",
        "Blossoms": "blossoms",
        "Plants": "plants",
        "Fruit": "fruit",
        "Min Height": "min_height",
        "Max Height": "max_height",
        "Median Height": "median_height",
        "Notes": "notes",
    }

    def __init__(
        self,
        host: str = "localhost",
        database: str = "saba_data_entry",
        user: str = "postgres",
        password: str = "",
        port: int = 5432,
    ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn: Optional[pg.extensions.connection] = None

    def connect(
        self,
        host: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        port: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        if host is not None:
            self.host = host
        if database is not None:
            self.database = database
        if user is not None:
            self.user = user
        if password is not None:
            self.password = password
        if port is not None:
            self.port = int(port)

        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass

        self.conn = pg.connect(
            host=self.host,
            dbname=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
            cursor_factory=RealDictCursor,
        )
        self.conn.autocommit = True

    def close(self) -> None:
        try:
            if self.conn is not None:
                self.conn.close()
        finally:
            self.conn = None

    def _cursor(self):
        if self.conn is None or self.conn.closed:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.conn.cursor()

    def _row_to_record(self, row: dict[str, Any]) -> dict[str, Any]:
        rev_map = {v: k for k, v in self.db_map.items()}
        record = {}
        for db_col, val in row.items():
            ui_key = rev_map.get(db_col, db_col)
            record[ui_key] = "" if val is None else str(val)
        return record

    def get_all_records(self) -> list[dict[str, Any]]:
        sql = f"SELECT * FROM {self.table_name} ORDER BY date DESC, time DESC;"
        with self._cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return [self._row_to_record(dict(r)) for r in rows]

    def get_record(self, rowkey: RowKey) -> dict[str, Any]:
        d, t, lab, plot = rowkey
        sql = f"SELECT * FROM {self.table_name} WHERE date=%s AND time=%s AND lab_id=%s AND plot=%s;"
        with self._cursor() as cur:
            cur.execute(sql, (d, t, lab, int(plot)))
            row = cur.fetchone()
        if not row:
            raise KeyError(f"Record not found: {rowkey}")
        return self._row_to_record(dict(row))

    def _ensure_technician_and_lab_check(self, cur, lab_id: str, date_val: str, time_val: str) -> None:
        cur.execute("SELECT id FROM lab_techs ORDER BY id LIMIT 1;")
        tech_row = cur.fetchone()
        if tech_row:
            tech_id = tech_row["id"]
        else:
            cur.execute("INSERT INTO lab_techs (name) VALUES ('Default Tech') RETURNING id;")
            created = cur.fetchone()
            tech_id = created["id"] if created else 1

        cur.execute(
            """
            INSERT INTO lab_checks (lab_id, date, time, lab_tech_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (lab_id, date, time) DO NOTHING;
            """,
            (lab_id, date_val, time_val, tech_id),
        )

    def save_record(
        self,
        record: dict[str, Any],
        rowkey: Optional[RowKey] = None,
    ) -> None:
        db_record: dict[str, Any] = {}
        for ui_k, v in record.items():
            mapped_key = "Median Height" if ui_k == "Med Height" else ui_k
            db_k = self.db_map.get(mapped_key)
            if db_k:
                if v == "" or v is None:
                    db_record[db_k] = None
                else:
                    field_type = self.fields.get(mapped_key, {}).get("type", "str")
                    if field_type in ("decimal", "float"):
                        try:
                            db_record[db_k] = float(v)
                        except (ValueError, TypeError):
                            db_record[db_k] = None
                    elif field_type == "int":
                        try:
                            db_record[db_k] = int(v)
                        except (ValueError, TypeError):
                            db_record[db_k] = None
                    elif field_type == "bool":
                        db_record[db_k] = str(v).strip().lower() in ("true", "1", "t", "yes")
                    else:
                        db_record[db_k] = str(v).strip()

        with self._cursor() as cur:
            lab = db_record.get("lab_id")
            date_val = db_record.get("date")
            time_val = db_record.get("time")
            if lab and date_val and time_val:
                self._ensure_technician_and_lab_check(cur, str(lab), str(date_val), str(time_val))

            if rowkey is None:
                cols = [k for k, v in db_record.items() if v is not None]
                if not cols:
                    raise ValueError("Cannot insert an empty record.")
                col_sql = ", ".join(cols)
                val_sql = ", ".join(f"%({c})s" for c in cols)
                sql = f"INSERT INTO {self.table_name} ({col_sql}) VALUES ({val_sql});"
                cur.execute(sql, db_record)
            else:
                set_cols = ", ".join(f"{k}=%({k})s" for k in db_record.keys() if k not in ("date", "time", "lab_id", "plot"))
                d, t, lab, plot = rowkey
                sql = (
                    f"UPDATE {self.table_name} SET {set_cols} "
                    f"WHERE date=%(old_date)s AND time=%(old_time)s AND lab_id=%(old_lab)s AND plot=%(old_plot)s;"
                )
                payload = {**db_record, "old_date": d, "old_time": t, "old_lab": lab, "old_plot": int(plot)}
                cur.execute(sql, payload)

    def delete_record(self, rowkey: RowKey) -> None:
        d, t, lab, plot = rowkey
        sql = f"DELETE FROM {self.table_name} WHERE date=%s AND time=%s AND lab_id=%s AND plot=%s;"
        with self._cursor() as cur:
            cur.execute(sql, (d, t, lab, int(plot)))
