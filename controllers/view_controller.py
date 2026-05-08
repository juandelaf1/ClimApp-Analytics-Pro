from flask import Blueprint, render_template, request

view_bp = Blueprint("view", __name__, template_folder="../templates")

@view_bp.route("/")
def index():
    return render_template("index.html")

@view_bp.route("/registro")
def registro():
    return render_template("registro.html")

@view_bp.route("/api")
def api_view():
    """
    CORRECCIÓN: El botón API del menú ahora carga el Dashboard real.
    """
    return render_template("index.html")

@view_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    municipio = None
    fecha = None

    if request.method == "POST":
        municipio = request.form.get("municipio", "").strip().upper()
        fecha = request.form.get("fecha", "").strip()

    respuesta = filter_records(municipio=municipio if municipio else None, fecha=fecha if fecha else None)
    
    if isinstance(respuesta, dict):
        registros = respuesta.get("data", [])
    elif isinstance(respuesta, list):
        registros = respuesta
    else:
        registros = []

    return render_template("consulta.html", registros=registros)

@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    municipio = request.form.get("municipio", "").strip().upper()
    if not municipio:
        return render_template("comparar.html", resultado={"success": False, "message": "Debes introducir un municipio."})

    resultado = compare_latest_records(municipio)
    return render_template("comparar.html", resultado=resultado)