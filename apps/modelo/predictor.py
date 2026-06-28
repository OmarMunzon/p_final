from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

modelo = joblib.load(
    BASE_DIR / "adaptive_model2.pkl"
)

def recomendar(
    nivel_diagnostico,
    # tema_actual,
    ejercicios_resueltos,
    porcentaje_aciertos,
    intentos_promedio,
    # tiempo_promedio_seg,
    errores_consecutivos,
    xp_acumulada,
    lecciones_completadas,
    # dias_inactividad,
    # edad,
    # curso
):

    datos = pd.DataFrame([{
        # "edad": edad,
        # "curso": curso,
        "nivel_diagnostico": nivel_diagnostico,
        # "tema_actual": tema_actual,
        "ejercicios_resueltos": ejercicios_resueltos,
        "porcentaje_aciertos": porcentaje_aciertos,
        "intentos_promedio": intentos_promedio,
        # "tiempo_promedio_seg": tiempo_promedio_seg,
        "errores_consecutivos": errores_consecutivos,
        "xp_acumulada": xp_acumulada,
        "lecciones_completadas": lecciones_completadas,
        # "dias_inactividad": dias_inactividad
    }])

    pred = modelo.predict(datos)[0]

    recomendaciones = {
        0: "Reforzar",
        1: "Mantener",
        2: "Avanzar"
    }

    return recomendaciones[pred]
