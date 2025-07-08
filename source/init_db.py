import os
import sqlite3

#Realizamos conexión a la BD SQLite. (pipeline.db en root)

db_path = os.path.join(os.path.dirname(__file__), '..', 'pragma_test.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

#Pasamos a la creación de las tablas.

cur.execute(
    """
        CREATE TABLE IF NOT EXISTS eventos (
            id         INTEGER   PRIMARY KEY AUTOINCREMENT,
            timestamp  TEXT      NOT NULL, 
            price      REAL      NOT NULL,
            user_id    INTEGER   NOT NULL
        );
    """
)

cur.execute(
    """
        CREATE TABLE IF NOT EXISTS estadisticas (
            total_count     INTEGER DEFAULT 0,
            sum_price       REAL DEFAULT 0.0,
            min_price       REAL DEFAULT 1e12,
            max_price       REAL DEFAULT 0.0
        );
    """
)

"""
Inicializamos los valores en estadisticas.
Con el objetivo de manejar una sola fila de registros, verificamos la cantidad total de filas en la tabla estadisticas,
si la tabla estadisticas se encuentra vacía, entonces agregamos los valores iniciales que mostramos en VALUES
"""
cur.execute("SELECT COUNT(*) FROM estadisticas;")
if cur.fetchone()[0] == 0:
    cur.execute(
        "INSERT INTO estadisticas (total_count, sum_price, min_price, max_price) VALUES (0,0.0,1e12,0.0);"
    )

conn.commit()
conn.close()

print("Base de Datos y tablas creadas e inicializadas con éxito")