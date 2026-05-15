# Alejandro Rodríguez Duque - Front End
# Santiago Rodríguez Duque - Back End
# 28 Febrero 2026
# Licencia de uso, leer el LICENSE
# Quindío, Colombia

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, date

app = Flask(__name__, template_folder="pages")

# ---------- Data Base ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Estado del pago (sin pagar, adelanto, pagado) ----------
def estado_pago(valor, adelanto):
    if adelanto == 0:
        return "Sin pagar"
    elif adelanto < valor:
        return "Adelanto"
    return "Pagado"

print(estado_pago(2,1))

# ---------- Días Restantes ----------

def dias_restantes(fecha):
    return (datetime.strptime(fecha, "%Y-%m-%d").date() - date.today()).days

# ---------- RUTAS ----------
@app.route("/")
def dashboard():
    db = get_db()
    trabajos = db.execute("""
        SELECT * FROM trabajos
        WHERE estado_trabajo != 'entregado'
        ORDER BY
            CASE
                WHEN tiene_entrega_parcial = 1 AND fecha_entrega_parcial IS NOT NULL
                THEN fecha_entrega_parcial
                ELSE fecha_entrega_final
            END
    """).fetchall()

    # Registro de facturación con cantidad de trabajos procesados a nivel mensual y semanal.
    trabajos_procesados = []
    hoy = date.today()
    mes_actual = hoy.strftime("%Y-%m")
    anio_actual = hoy.strftime("%Y")

    ingreso_mensual = 0
    ingreso_anual = 0

    for t in trabajos_procesados:

        # Saldo De Cuenta De Pagos Adelantados
        if t["adelanto"] > 0:
            creado = t["creado_en"]
            if creado.startswith(mes_actual):
                ingreso_mensual += t["adelanto"]
            if creado.startswith(anio_actual):
                ingreso_anual += t["adelanto"]

        # Saldo cuenta cuando se cierra el trabajo
        if t["estado_trabajo"] == "entregado" and t["fin_trabajo"]:
            fin = t["fin_trabajo"][:10]  # YYYY-MM-DD
            saldo_cobrado = t["saldo"]

            if fin.startswith(mes_actual):
                ingreso_mensual += saldo_cobrado
            if fin.startswith(anio_actual):
                ingreso_anual += saldo_cobrado

    for t in trabajos:
        # Fechas de parciales
        fecha_ref = (
            t["fecha_entrega_parcial"]
            if t["tiene_entrega_parcial"] and t["fecha_entrega_parcial"]
            else t["fecha_entrega_final"]
        )

        # Total a pagar
        saldo = t["valor_total"] - t["adelanto"]

        # Proceso front del estado de cada trabajo
        trabajos_procesados.append({
            **dict(t),
            "estado_pago": estado_pago(t["valor_total"], t["adelanto"]),
            "saldo": saldo,
            "dias": dias_restantes(fecha_ref)
        })

    # Métricas para las casillas
    total_activos = len(trabajos_procesados)
    urgentes = len([t for t in trabajos_procesados if t["dias"] <= 1])
    sin_adelanto = len([t for t in trabajos_procesados if t["adelanto"] == 0])
    saldo_total = sum(t["saldo"] for t in trabajos_procesados)
    fecha_actual = date.today().strftime("%B %Y")

    # Renderizado
    return render_template(
    "dashboard.html",
    trabajos=trabajos_procesados,
    total=total_activos,
    urgentes=urgentes,
    sin_adelanto=sin_adelanto,
    saldo_total=saldo_total,
    ingreso_mensual=ingreso_mensual,
    ingreso_anual=ingreso_anual,
    fecha_actual=fecha_actual
    )

# Configuraciones de renderizado
@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        db = get_db()
        db.execute("""
        INSERT INTO trabajos (
            asignatura, descripcion, fecha_entrega_final,
            tiene_entrega_parcial, fecha_entrega_parcial,
            estado_trabajo, valor_total, adelanto,
            observaciones, inicio_trabajo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["asignatura"],
            request.form["descripcion"],
            request.form["fecha_final"],
            1 if request.form.get("parcial") else 0,
            request.form.get("fecha_parcial"),
            "Pendiente",
            float(request.form["valor"]),
            float(request.form["adelanto"]),
            request.form["observaciones"],
            inicio
        ))
        db.commit()
        return redirect(url_for("dashboard"))

    return render_template("nuevo_trabajo.html")

@app.route("/entregar/<int:id>")
def entregar(id):
    fin = datetime.now()
    db = get_db()

    trabajo = db.execute(
        "SELECT inicio_trabajo FROM trabajos WHERE id=?",
        (id,)
    ).fetchone()

    inicio = datetime.strptime(trabajo["inicio_trabajo"], "%Y-%m-%d %H:%M:%S")
    minutos = int((fin - inicio).total_seconds() / 60)

    db.execute("""
        UPDATE trabajos
        SET estado_trabajo='entregado',
            fin_trabajo=?,
            tiempo_total=?
        WHERE id=?
    """, (fin.strftime("%Y-%m-%d %H:%M:%S"), minutos, id))

    db.commit()
    return redirect("/")

app.run(debug=True)