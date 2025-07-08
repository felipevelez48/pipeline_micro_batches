import os
import sqlite3
import pandas as pd
from datetime import datetime

#Creamos la función para procesar info en batch, en esta caso archivos CSV.

def procesamiento_batch(csv_path, conn, cur):
    #creamos el dataframe para manipular la información
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        #Convertimos cada una de las fecha en día-mes-año; en lugar de mes-día-año
        fecha = datetime.strptime(row['timestamp'], '%m/%d/%Y').date().isoformat()
        #Para no luchar con los nulos, le ponemos la condición si está nulo, lo pongamos en 0.0
        price = float(row['price']) if pd.notna(row['price']) else 0.0
        #convertimos a entero los user_id
        user_id = int(row['user_id'])

        #Insertamos los eventos de los CSV
        cur.execute("INSERT INTO eventos (timestamp, price, user_id) VALUES (?,?,?);",
            (fecha, price, user_id)
        )

        #Actualizamos las estadísticas
        cur.execute(
            """
            UPDATE estadisticas
                SET total_count = total_count + 1,
                    sum_price = sum_price + ?,
                    min_price = MIN(min_price, ?),
                    max_price = MAX(max_price, ?)
            """, (price,price,price)
        )

    conn.commit()
    #Ahora acá obtenemos las métricas actuales que se están ejecutando
    total, sum_p, min_p, max_p = cur.execute(
        "SELECT total_count, sum_price, min_price, max_price FROM estadisticas;"
    ).fetchone()
    avg_price = sum_p/total if total else 0.0
    return total, avg_price, min_p, max_p

"""
Para validar que todo este correcto, hagamos una función para consultar directamente desde la BD eventos
"""
def consulta_tabla(cur, label=""):
    row = cur.execute(
        "SELECT COUNT(*), AVG(price), MIN(price), MAX(price) FROM eventos;"
    ).fetchone()
    cnt,avg,mn,mx = row
    print(f"{label} (direct query): count = {cnt}  | avg = {avg:.2f}  | min = {mn:.2f}  | max= {mx:.2f} \n \n \n")

"""
También solo para temas visuales en la terminal, creamos una pequeña función para el print.
"""
def caja_texto(texto):
    largo= len(texto) + 4
    print ('*' * largo)
    print(f"* {texto} *")
    print ('*' * largo)


"""
Ahora creemos la conexión a la BD 'ppragma_text.db' y le damos la ruta a los archivos para cargar
"""
def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'pragma_test.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    #Ahora buscamos la ruta de los archivos, excluyendo validation.csv
    data_dir = os.path.join(base_dir, 'data')
    batches = sorted(f for f in os.listdir(data_dir)
                     if f.endswith('.csv') and f != 'validation.csv'
                     )
    
    #Procesamos cada batch y mostramos las métricas mientras se van calculando
    for i in batches:
        full_path = os.path.join(data_dir, i)
        total, avg_file, min_file, max_file = procesamiento_batch(full_path, conn, cur)
        print(f"{i}: (estadisticas)  count = {total} | promedio = {avg_file:.2f}  | mínimo = {min_file:.2f}   | máximo = {max_file:.2f}")

    """Una vez validamos que estamos leyendo correctamente la información, imprimomos las
        estadísticas antes de proceder con la evaluación del archivo validation.csv
    """
    print(" \n --------Antes del validation.csv -------- \n")
    total_cero, sum_cero, min_cero, max_cero = cur.execute(
        "SELECT total_count, sum_price, min_price, max_price FROM estadisticas;"
    ).fetchone()
    prom_cero= sum_cero/total_cero if total_cero else 0.0
    print(f" (estadisticas) count = {total_cero} | promedio = {prom_cero:.2f}  | mínimo = {min_cero:.2f}   | máximo = {max_cero:.2f} ")
    print("\n ---------------------------------------------- \n")
    consulta_tabla(cur, label="Antes")


    """
    Ahora vamos a procesar el archivo validation.csv, dando su ubicación y mostrando
    los resultados después de su ejecución, utilizando la misma función
    procesamiento_batch
    """
    validation_path = os.path.join(data_dir, 'validation.csv')
    procesamiento_batch(validation_path, conn, cur)
    print ("\n ----------- Después del validation.csv ------- \n")
    total_uno, sum_uno, min_uno, max_uno = cur.execute(
        "SELECT total_count, sum_price, min_price, max_price FROM estadisticas;"
    ).fetchone()
    prom_uno= sum_uno/total_uno if total_cero else 0.0
    print(f" (estadisticas) count = {total_uno} | promedio = {prom_uno:.2f}  | mínimo = {min_uno:.2f}   | máximo = {max_uno:.2f} ")
    consulta_tabla(cur, label="Después")
    caja_texto("Así validamos que tanto la información que nos arroja la función, como la que consultamos directamente a la BD es la misma. Check")
    conn.close()

if __name__ == '__main__':
    main()