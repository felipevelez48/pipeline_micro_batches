# Data Pipeline Micro-Batches
### Test Data Engineer Pragma
![Logo pragma](images/pragma.jpg)


## Simulador Pipeline Micro-Batches 💻🌐

Solución práctica para demostrar cómo capturar, procesar y validar datos en tiempo real mediante micro‑batches! Este repositorio muestra:

- 🌟 **Ingesta incremental:** cómo cargar datos en fragmentos (micro‑batches) sin sobrecargar la memoria.

- ⚡ **Procesamiento eficiente:** actualiza métricas (conteo, promedio, mínimo, máximo) de forma incremental con una única consulta por fila.

- 🔍 **Validación automatizada:** comprueba que las métricas acumuladas coincidan con consultas directas a la base de datos.

Con solo Python, SQLite y Pandas, este pipeline demuestra los fundamentos de la ingesta near‑real time y la integridad de datos.


## 📂 Estructura del Proyecto

```plaintext

data_pipeline/
├── README.md
├── images/ pragma.jpg #Logo de Pragma
├── data/ # CSVs de entrada (2012-1.csv … 2012-5.csv y validation.csv)
├── src/ # Código fuente
│ ├── init_db.py # Inicializa SQLite (pragma_test.db) y crea tablas (eventos & estadisticas)
│ └── pipeline_dos.py # Procesa batches, actualiza estadísticas y valida resultados
├── pragma_test.db # Archivo de base de datos generado
└── requirements.txt # Dependencias de Python
```

## ⚙️ Requisitos

- Python 3.7+  
- Git  
- Librerías Python (instalar en entorno virtual):
  ```bash
  pip install -r requirements.txt
  ```

## 🛠️ Uso
1. Clonar el repositorio
```bash
  git clone <https://github.com/felipevelez48/pipeline_micro_batches.git>
  cd data_pipeline
```

2. Instalar dependencias (recomendado en venv)
```bash
python -m venv venv
source venv/bin/activate   # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

3. Inicializar base de datos en SQLite
```bash
python src/init_db.py
```
  - Crea pragma_test.db y tablas eventos & estadisticas

4. Procesar micro-batches
```bash
python src/pipeline_dos.py
```
  -Lee los CSV de data/ (excepto validation.csv).

  -Inserta eventos en eventos y actualiza métricas en estadisticas.

  -Muestra métricas por batch.

  -Valida antes y después con validation.csv.
  
  - Compara el resultado del script vs. el direct query a la base de datos.

## 🧩 Detalles técnicos

- **SQLite** para simplicidad; con fácil migración a PostgreSQL cambiando URL de conexión.
        Nota: En caso de necesitar multi-usuario se recomienda migrar a PostgreSQL/MySQL

- **Pandas** para lectura de CSV.
        Nota: Manejo de nulls según estrategia (actual: valor null se convierte en 0.0)

- **Batch incremental:** métricas (count, sum, min, max) se actualizan con un solo UPDATE por fila en memoria mínima.

- **Validación:** comparación entre agregados incrementales y consulta directa a events.


## 📊🤖 Autor: John Felipe Vélez

### Data Engineer 💜


