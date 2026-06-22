def generar_feedback(prediccion):

    if prediccion == "Reforzar":

        return {
            "mensaje":
                "Necesitas reforzar este tema.",
            "accion":
                "Mostrar ejercicios básicos"
        }

    elif prediccion == "Mantener":

        return {
            "mensaje":
                "Continúa practicando.",
            "accion":
                "Mostrar ejercicios intermedios"
        }

    else:

        return {
            "mensaje":
                "Excelente trabajo.",
            "accion":
                "Desbloquear siguiente "
        }