import psycopg2 as pg

cx = pg.connect(
    host='localhost',
    database='saba_data_entry',
    user=input('Username: ')
)

cur = cx.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS test
    (id SERIAL PRIMARY KEY, val TEXT);
""")

cur.execute("""
INSERT INTO test (val)
VALUES ('Banana'), ('Orange'), ('Apple');
""")

cx.commit()

cur.execute("SELECT * FROM test")
num_rows = cur.rowcount
data = cur.fetchall()

print(f'Got {num_rows} rows from database:')
print(data)

cur.close()
cx.close()
