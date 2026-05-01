"""
Banco de preguntas para el diagnóstico inicial.
Cada pregunta tiene: enunciado, opciones y respuesta correcta.
"""

PREGUNTAS_DIAGNOSTICO = [
    {
        'id': 1,
        'enunciado': '¿Cuánto es 15 + 28?',
        'opciones': ['41', '43', '42', '44'],
        'respuesta_correcta': '43',
        'puntaje': 10,
        'categoria': 'matematica_basica',
    },
    {
        'id': 2,
        'enunciado': (
            'Si un estudiante tiene 120 puntos de 200 posibles, '
            '¿qué porcentaje obtuvo?'
        ),
        'opciones': ['55%', '60%', '65%', '70%'],
        'respuesta_correcta': '60%',
        'puntaje': 10,
        'categoria': 'matematica_basica',
    },
    {
        'id': 3,
        'enunciado': (
            '¿Cuál es la raíz cuadrada de 144?'
        ),
        'opciones': ['10', '11', '12', '13'],
        'respuesta_correcta': '12',
        'puntaje': 10,
        'categoria': 'matematica_basica',
    },
    {
        'id': 4,
        'enunciado': (
            'En Python, ¿cuál es el resultado de: 10 // 3?'
        ),
        'opciones': ['3.33', '3', '4', '2'],
        'respuesta_correcta': '3',
        'puntaje': 15,
        'categoria': 'programacion',
    },
    {
        'id': 5,
        'enunciado': (
            '¿Qué tipo de dato retorna la función len() en Python?'
        ),
        'opciones': ['float', 'str', 'int', 'bool'],
        'respuesta_correcta': 'int',
        'puntaje': 15,
        'categoria': 'programacion',
    },
    {
        'id': 6,
        'enunciado': (
            'En una lista [1, 2, 3, 4, 5], '
            '¿cuál es el índice del valor 3?'
        ),
        'opciones': ['1', '2', '3', '4'],
        'respuesta_correcta': '2',
        'puntaje': 15,
        'categoria': 'programacion',
    },
    {
        'id': 7,
        'enunciado': (
            '¿Cuál de estas estructuras almacena pares clave-valor?'
        ),
        'opciones': ['lista', 'tupla', 'diccionario', 'conjunto'],
        'respuesta_correcta': 'diccionario',
        'puntaje': 15,
        'categoria': 'programacion',
    },
    {
        'id': 8,
        'enunciado': (
            'Si f(x) = 2x² + 3x − 5, ¿cuánto es f(2)?'
        ),
        'opciones': ['7', '8', '9', '10'],
        'respuesta_correcta': '9',
        'puntaje': 20,
        'categoria': 'matematica_avanzada',
    },
    {
        'id': 9,
        'enunciado': (
            '¿Cuál es la complejidad temporal del algoritmo '
            'de búsqueda binaria?'
        ),
        'opciones': ['O(n)', 'O(n²)', 'O(log n)', 'O(1)'],
        'respuesta_correcta': 'O(log n)',
        'puntaje': 20,
        'categoria': 'algoritmos',
    },
    {
        'id': 10,
        'enunciado': (
            '¿Qué principio de la POO permite que una clase '
            'herede atributos de otra?'
        ),
        'opciones': [
            'Encapsulamiento',
            'Polimorfismo',
            'Herencia',
            'Abstracción',
        ],
        'respuesta_correcta': 'Herencia',
        'puntaje': 20,
        'categoria': 'programacion_avanzada',
    },
]

PUNTAJE_MAXIMO = sum(p['puntaje'] for p in PREGUNTAS_DIAGNOSTICO)
