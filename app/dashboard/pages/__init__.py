from app.dashboard.pages.resumen_ejecutivo import render as resumen_ejecutivo_render
from app.dashboard.pages.analisis_cientifico import render as analisis_cientifico_render
from app.dashboard.pages.auditoria_datos import render as auditoria_datos_render
from app.dashboard.pages.mapa_estaciones import render as mapa_estaciones_render
from app.dashboard.pages.configuracion import render as configuracion_render

resumen_ejecutivo = type("Module", (), {"render": resumen_ejecutivo_render})()
analisis_cientifico = type("Module", (), {"render": analisis_cientifico_render})()
auditoria_datos = type("Module", (), {"render": auditoria_datos_render})()
mapa_estaciones = type("Module", (), {"render": mapa_estaciones_render})()
configuracion = type("Module", (), {"render": configuracion_render})()