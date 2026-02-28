import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trabajos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asignatura TEXT NOT NULL,
    descripcion TEXT,
    fecha_entrega_final DATE NOT NULL,
    tiene_entrega_parcial INTEGER NOT NULL,
    fecha_entrega_parcial DATE,
    estado_trabajo TEXT NOT NULL,
    valor_total REAL NOT NULL,
    adelanto REAL NOT NULL,
    observaciones TEXT,
    creado_en DATE DEFAULT CURRENT_DATE
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente")
