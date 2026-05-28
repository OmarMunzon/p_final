from django.core.management.base import BaseCommand
from apps.aprendizaje.roadmap.models import (
    RoadmapStage,
    RoadmapLesson,
    RoadmapExercise,
    RoadmapTestCase,
    RoadmapQuizQuestion,
)


class Command(BaseCommand):
    help = 'Carga roadmap completo con 10 ejercicios por stage'

    def handle(self, *args, **kwargs):

        RoadmapStage.objects.all().delete()

        self.stdout.write('🧹 Limpiando datos anteriores...')

        # =====================================================
        # FUNCIÓN AUXILIAR
        # =====================================================
        def crear_quiz(
            lesson,
            order,
            title,
            question,
            options,
            correct_idx,
            explanation,
            xp=10,
            difficulty='easy'
        ):
            ex = RoadmapExercise.objects.create(
                lesson=lesson,
                title=title,
                description='Responde correctamente.',
                exercise_type='quiz',
                difficulty=difficulty,
                xp_reward=xp,
                time_limit_secs=120,
                max_attempts=3,
                order=order,
            )

            RoadmapQuizQuestion.objects.create(
                exercise=ex,
                order=1,
                question=question,
                options=options,
                correct_idx=correct_idx,
                explanation=explanation,
            )

        # =====================================================
        # STAGE 1 — PENSAMIENTO LÓGICO
        # =====================================================
        s1 = RoadmapStage.objects.create(
            title='Pensamiento lógico',
            icon='🧠',
            order=1,
            difficulty='easy',
        )

        l1 = RoadmapLesson.objects.create(
            stage=s1,
            title='Patrones y secuencias',
            status='locked',
            xp_reward=100,
            order=1,
            difficulty='easy',
        )

        patrones = [
            ('2,4,6,8,?', '9|10|12|14', 1, 'Incrementa de 2 en 2'),
            ('1,3,5,7,?', '8|9|10|11', 1, 'Números impares'),
            ('5,10,15,20,?', '30|25|35|40', 1, 'Incrementa de 5'),
            ('10,8,6,4,?', '3|2|1|0', 1, 'Disminuye de 2'),
            ('1,2,4,8,?', '10|12|16|18', 2, 'Multiplica por 2'),
            ('3,6,9,12,?', '15|18|21|24', 0, 'Múltiplos de 3'),
            ('7,14,21,28,?', '30|35|40|42', 1, 'Múltiplos de 7'),
            ('9,7,5,3,?', '2|1|0|-1', 1, 'Disminuye de 2'),
            ('1,4,9,16,?', '20|25|36|49', 1, 'Cuadrados perfectos'),
            ('2,3,5,8,13,?', '18|20|21|22', 2, 'Secuencia Fibonacci'),
        ]

        for idx, p in enumerate(patrones, start=1):
            crear_quiz(
                lesson=l1,
                order=idx,
                title=f'Patrón lógico {idx}',
                question=f'¿Qué número continúa? {p[0]}',
                options=p[1],
                correct_idx=p[2],
                explanation=p[3],
            )

        # =====================================================
        # STAGE 2 — VARIABLES Y DATOS
        # =====================================================
        s2 = RoadmapStage.objects.create(
            title='Variables y datos',
            icon='📦',
            order=2,
            difficulty='easy',
        )

        l2 = RoadmapLesson.objects.create(
            stage=s2,
            title='Tipos de datos',
            status='locked',
            xp_reward=120,
            order=1,
            difficulty='easy',
        )

        preguntas_datos = [
            ('¿Cuál es un entero?', '3.14|"hola"|50|True', 2),
            ('¿Cuál es un string?', 'False|"Python"|3|9.5', 1),
            ('¿Cuál es booleano?', '0|1|True|"False"', 2),
            ('¿Cuál es float?', '10|5.5|"hola"|False', 1),
            ('¿Qué tipo es "123"?', 'int|float|string|bool', 2),
            ('¿Qué tipo es True?', 'bool|str|int|float', 0),
            ('¿Qué función devuelve el tipo?', 'print()|type()|input()|len()', 1),
            ('¿Qué símbolo define string?', '{}|""|[]|()', 1),
            ('¿Cuál es lista?', '[]|()|{}|""', 0),
            ('¿Cuál es diccionario?', '{}|[]|()|<>', 0),
        ]

        for idx, q in enumerate(preguntas_datos, start=1):
            crear_quiz(
                lesson=l2,
                order=idx,
                title=f'Tipos de datos {idx}',
                question=q[0],
                options=q[1],
                correct_idx=q[2],
                explanation='Respuesta correcta.',
            )

        # =====================================================
        # STAGE 3 — OPERADORES LÓGICOS
        # =====================================================
        s3 = RoadmapStage.objects.create(
            title='Operadores lógicos',
            icon='⚖️',
            order=3,
            difficulty='easy',
        )

        l3 = RoadmapLesson.objects.create(
            stage=s3,
            title='AND OR NOT',
            status='locked',
            xp_reward=140,
            order=1,
            difficulty='easy',
        )

        operadores = [
            ('True and False', 'True|False', 1),
            ('True or False', 'True|False', 0),
            ('not True', 'True|False', 1),
            ('5 > 3', 'True|False', 0),
            ('2 == 5', 'True|False', 1),
            ('4 != 4', 'True|False', 1),
            ('7 >= 7', 'True|False', 0),
            ('3 < 1', 'True|False', 1),
            ('True and True', 'True|False', 0),
            ('False or False', 'True|False', 1),
        ]

        for idx, o in enumerate(operadores, start=1):
            crear_quiz(
                lesson=l3,
                order=idx,
                title=f'Operadores lógicos {idx}',
                question=f'¿Cuál es el resultado de {o[0]}?',
                options=o[1],
                correct_idx=o[2],
                explanation='Evaluación lógica.',
            )

        # =====================================================
        # STAGE 4 — CONDICIONALES
        # =====================================================
        s4 = RoadmapStage.objects.create(
            title='Condicionales',
            icon='🔀',
            order=4,
            difficulty='medium',
        )

        l4 = RoadmapLesson.objects.create(
            stage=s4,
            title='if / elif / else',
            status='locked',
            xp_reward=160,
            order=1,
            difficulty='easy',
        )

        # Ejercicio 1: Positivo o Negativo
        ex1 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 1: Positivo o Negativo',
            description='Completa el código para detectar si un número es positivo o negativo.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=1,
            fill_template=(
                'def clasificar(n):\n'
                '    ___ n > 0:\n'
                '        return "Positivo"\n'
                '    ___:\n'
                '        return "Negativo"'
            ),
            fill_answers='if|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex1,
            description='clasificar(5)',
            input_data='clasificar(5)',
            expected='Positivo',
            order=1,
        )

        # Ejercicio 2: Categoría de calificación
        ex2 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 2: Calificación',
            description='Completa el código para categorizar una calificación.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=2,
            fill_template=(
                'def nota(calificacion):\n'
                '    ___ calificacion >= 90:\n'
                '        return "A"\n'
                '    ___ calificacion >= 80:\n'
                '        return "B"\n'
                '    ___:\n'
                '        return "C"'
            ),
            fill_answers='if|elif|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex2,
            description='nota(85)',
            input_data='nota(85)',
            expected='B',
            order=1,
        )

        # Ejercicio 3: Mayor de edad
        ex3 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 3: Mayor de edad',
            description='Completa el código para validar mayoría de edad.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=3,
            fill_template=(
                'def mayor_edad(edad):\n'
                '    ___ edad >= 18:\n'
                '        return "Sí"\n'
                '    ___:\n'
                '        return "No"'
            ),
            fill_answers='if|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex3,
            description='mayor_edad(21)',
            input_data='mayor_edad(21)',
            expected='Sí',
            order=1,
        )

        # Ejercicio 4: Número par o impar
        ex4 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 4: Par o Impar',
            description='Completa el código para detectar si un número es par o impar.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=4,
            fill_template=(
                'def paridad(n):\n'
                '    ___ n % 2 == 0:\n'
                '        return "Par"\n'
                '    ___:\n'
                '        return "Impar"'
            ),
            fill_answers='if|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex4,
            description='paridad(7)',
            input_data='paridad(7)',
            expected='Impar',
            order=1,
        )

        # Ejercicio 5: Rango de temperatura
        ex5 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 5: Temperatura',
            description='Completa el código para clasificar la temperatura.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=5,
            fill_template=(
                'def clima(temp):\n'
                '    ___ temp < 15:\n'
                '        return "Frío"\n'
                '    ___ temp <= 25:\n'
                '        return "Templado"\n'
                '    ___:\n'
                '        return "Caluroso"'
            ),
            fill_answers='if|elif|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex5,
            description='clima(20)',
            input_data='clima(20)',
            expected='Templado',
            order=1,
        )

        # Ejercicio 6: Descuento por compra
        ex6 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 6: Descuento',
            description='Completa el código para calcular descuento según monto.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=6,
            fill_template=(
                'def descuento(monto):\n'
                '    ___ monto >= 100:\n'
                '        return monto * 0.9\n'
                '    ___ monto >= 50:\n'
                '        return monto * 0.95\n'
                '    ___:\n'
                '        return monto'
            ),
            fill_answers='if|elif|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex6,
            description='descuento(100)',
            input_data='descuento(100)',
            expected='90',
            order=1,
        )

        # Ejercicio 7: Estación del año
        ex7 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 7: Estación',
            description='Completa el código para identificar la estación según el mes.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=7,
            fill_template=(
                'def estacion(mes):\n'
                '    ___ mes in [12, 1, 2]:\n'
                '        return "Invierno"\n'
                '    ___ mes in [3, 4, 5]:\n'
                '        return "Primavera"\n'
                '    ___:\n'
                '        return "Verano"'
            ),
            fill_answers='if|elif|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex7,
            description='estacion(6)',
            input_data='estacion(6)',
            expected='Verano',
            order=1,
        )

        # Ejercicio 8: Acceso a sistema
        ex8 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 8: Acceso',
            description='Completa el código para validar acceso según permisos.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=8,
            fill_template=(
                'def acceso(rol):\n'
                '    ___ rol == "admin" ___ rol == "supervisor":\n'
                '        return "Permitido"\n'
                '    ___:\n'
                '        return "Denegado"'
            ),
            fill_answers='if|or|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex8,
            description='acceso("admin")',
            input_data='acceso("admin")',
            expected='Permitido',
            order=1,
        )

        # Ejercicio 9: Valida intervalo
        ex9 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 9: Intervalo válido',
            description='Completa el código para validar si está en rango 10-100.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=9,
            fill_template=(
                'def en_rango(x):\n'
                '    ___ x >= 10 ___ x <= 100:\n'
                '        return "Válido"\n'
                '    ___:\n'
                '        return "Fuera de rango"'
            ),
            fill_answers='if|and|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex9,
            description='en_rango(50)',
            input_data='en_rango(50)',
            expected='Válido',
            order=1,
        )

        # Ejercicio 10: Categoría de película
        ex10 = RoadmapExercise.objects.create(
            lesson=l4,
            title='Condicional 10: Clasificación película',
            description='Completa el código para clasificar película por edad.',
            exercise_type='fill',
            difficulty='easy',
            xp_reward=15,
            time_limit_secs=180,
            max_attempts=3,
            order=10,
            fill_template=(
                'def pelicula(edad):\n'
                '    ___ edad < 13:\n'
                '        return "G"\n'
                '    ___ edad < 17:\n'
                '        return "PG-13"\n'
                '    ___:\n'
                '        return "R"'
            ),
            fill_answers='if|elif|else',
        )
        RoadmapTestCase.objects.create(
            exercise=ex10,
            description='pelicula(14)',
            input_data='pelicula(14)',
            expected='PG-13',
            order=1,
        )

        # =====================================================
        # STAGE 5 — BUCLES
        # =====================================================
        s5 = RoadmapStage.objects.create(
            title='Bucles',
            icon='🔁',
            order=5,
            difficulty='medium',
        )

        l5 = RoadmapLesson.objects.create(
            stage=s5,
            title='Bucles for',
            status='locked',
            xp_reward=180,
            order=1,
            difficulty='medium',
        )

        # Ejercicio 1: Sumar números del 1 al n
        ex1 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 1: Suma de números',
            description='Suma todos los números desde 1 hasta n.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=1,
            starter_code=(
                'def sumar(n):\n'
                '    total = 0\n'
                '    # Tu código aquí\n'
                '    return total'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex1,
            description='sumar(5)',
            input_data='sumar(5)',
            expected='15',
            order=1,
        )

        # Ejercicio 2: Contar números pares
        ex2 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 2: Números pares',
            description='Cuenta cuántos números pares hay del 1 al n.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=2,
            starter_code=(
                'def contar_pares(n):\n'
                '    conteo = 0\n'
                '    # Tu código aquí\n'
                '    return conteo'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex2,
            description='contar_pares(10)',
            input_data='contar_pares(10)',
            expected='5',
            order=1,
        )

        # Ejercicio 3: Tabla de multiplicación
        ex3 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 3: Tabla de multiplicación',
            description='Genera la tabla de multiplicación de un número.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=3,
            starter_code=(
                'def tabla(n):\n'
                '    resultado = []\n'
                '    # Tu código aquí\n'
                '    return resultado'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex3,
            description='tabla(3)',
            input_data='tabla(3)',
            expected='[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]',
            order=1,
        )

        # Ejercicio 4: Fibonacci
        ex4 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 4: Secuencia Fibonacci',
            description='Genera los primeros n números de Fibonacci.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=4,
            starter_code=(
                'def fibonacci(n):\n'
                '    secuencia = []\n'
                '    # Tu código aquí\n'
                '    return secuencia'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex4,
            description='fibonacci(6)',
            input_data='fibonacci(6)',
            expected='[0, 1, 1, 2, 3, 5]',
            order=1,
        )

        # Ejercicio 5: Invertir una cadena
        ex5 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 5: Invertir texto',
            description='Invierte el orden de los caracteres en una cadena.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=5,
            starter_code=(
                'def invertir(texto):\n'
                '    resultado = ""\n'
                '    # Tu código aquí\n'
                '    return resultado'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex5,
            description='invertir("hola")',
            input_data='invertir("hola")',
            expected='aloh',
            order=1,
        )

        # Ejercicio 6: Factorial
        ex6 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 6: Factorial',
            description='Calcula el factorial de un número.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=6,
            starter_code=(
                'def factorial(n):\n'
                '    resultado = 1\n'
                '    # Tu código aquí\n'
                '    return resultado'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex6,
            description='factorial(5)',
            input_data='factorial(5)',
            expected='120',
            order=1,
        )

        # Ejercicio 7: Buscar máximo
        ex7 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 7: Número máximo',
            description='Encuentra el número mayor en una lista.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=7,
            starter_code=(
                'def maximo(lista):\n'
                '    max_num = lista[0]\n'
                '    # Tu código aquí\n'
                '    return max_num'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex7,
            description='maximo([3, 7, 2, 9, 1])',
            input_data='maximo([3, 7, 2, 9, 1])',
            expected='9',
            order=1,
        )

        # Ejercicio 8: Contar coincidencias
        ex8 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 8: Contar coincidencias',
            description='Cuenta cuántas veces aparece un elemento en una lista.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=8,
            starter_code=(
                'def contar(lista, elemento):\n'
                '    cantidad = 0\n'
                '    # Tu código aquí\n'
                '    return cantidad'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex8,
            description='contar([1, 2, 2, 3, 2], 2)',
            input_data='contar([1, 2, 2, 3, 2], 2)',
            expected='3',
            order=1,
        )

        # Ejercicio 9: Filtrar números
        ex9 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 9: Filtrar números',
            description='Crea una lista solo con números mayores a n.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=9,
            starter_code=(
                'def filtrar(lista, minimo):\n'
                '    resultado = []\n'
                '    # Tu código aquí\n'
                '    return resultado'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex9,
            description='filtrar([1, 5, 3, 8, 2], 3)',
            input_data='filtrar([1, 5, 3, 8, 2], 3)',
            expected='[5, 8]',
            order=1,
        )

        # Ejercicio 10: Histograma
        ex10 = RoadmapExercise.objects.create(
            lesson=l5,
            title='Bucle 10: Histograma',
            description='Crea un histograma visual usando asteriscos.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=20,
            time_limit_secs=300,
            max_attempts=3,
            order=10,
            starter_code=(
                'def histograma(lista):\n'
                '    resultado = ""\n'
                '    # Tu código aquí\n'
                '    return resultado'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex10,
            description='histograma([2, 3, 1])',
            input_data='histograma([2, 3, 1])',
            expected='**\n***\n*',
            order=1,
        )

        # =====================================================
        # STAGE 6 — ALGORITMOS
        # =====================================================
        s6 = RoadmapStage.objects.create(
            title='Algoritmos',
            icon='📋',
            order=6,
            difficulty='medium',
        )

        l6 = RoadmapLesson.objects.create(
            stage=s6,
            title='Secuencia lógica',
            status='locked',
            xp_reward=200,
            order=1,
            difficulty='medium',
        )

        # Ejercicio 1: Definición de algoritmo
        crear_quiz(
            lesson=l6,
            order=1,
            title='Algoritmo 1: Definición',
            question='¿Cuál es la mejor definición de un algoritmo?',
            options='Un diagrama de flujo|Una serie de pasos ordenados para resolver un problema|Un programa de computadora|Una función matemática',
            correct_idx=1,
            explanation='Un algoritmo es una secuencia ordenada de pasos para resolver un problema.',
        )

        # Ejercicio 2: Características de un algoritmo
        crear_quiz(
            lesson=l6,
            order=2,
            title='Algoritmo 2: Características',
            question='¿Cuál NO es una característica de un buen algoritmo?',
            options='Claridad|Ambigüedad|Eficiencia|Finitud',
            correct_idx=1,
            explanation='Un algoritmo debe ser claro, NO ambiguo, eficiente y con fin definido.',
        )

        # Ejercicio 3: Símbolo de inicio
        crear_quiz(
            lesson=l6,
            order=3,
            title='Algoritmo 3: Símbolo de inicio',
            question='¿Qué símbolo representa el INICIO en un diagrama de flujo?',
            options='Rectángulo|Óvalo|Rombo|Paralelogramo',
            correct_idx=1,
            explanation='El óvalo representa inicio/fin en un diagrama de flujo.',
        )

        # Ejercicio 4: Símbolo de proceso
        crear_quiz(
            lesson=l6,
            order=4,
            title='Algoritmo 4: Símbolo de proceso',
            question='¿Qué símbolo representa un PROCESO en un diagrama de flujo?',
            options='Óvalo|Rectángulo|Rombo|Triángulo',
            correct_idx=1,
            explanation='El rectángulo representa un proceso o instrucción.',
        )

        # Ejercicio 5: Símbolo de decisión
        crear_quiz(
            lesson=l6,
            order=5,
            title='Algoritmo 5: Símbolo de decisión',
            question='¿Qué símbolo representa una DECISIÓN (condicional) en un diagrama?',
            options='Rectángulo|Óvalo|Rombo|Paralelogramo',
            correct_idx=2,
            explanation='El rombo representa una decisión o condición en un diagrama de flujo.',
        )

        # Ejercicio 6: Símbolo de entrada/salida
        crear_quiz(
            lesson=l6,
            order=6,
            title='Algoritmo 6: Símbolo entrada/salida',
            question='¿Qué símbolo representa entrada o salida de datos?',
            options='Rectángulo|Paralelogramo|Rombo|Óvalo',
            correct_idx=1,
            explanation='El paralelogramo representa entrada (input) o salida (output) de datos.',
        )

        # Ejercicio 7: Orden en un algoritmo
        crear_quiz(
            lesson=l6,
            order=7,
            title='Algoritmo 7: Orden de pasos',
            question='¿Es importante el orden de los pasos en un algoritmo?',
            options='No, el orden no importa|Sí, el orden es crítico|Depende del algoritmo|Sólo en algunos casos',
            correct_idx=1,
            explanation='El orden de los pasos es fundamental para que el algoritmo funcione correctamente.',
        )

        # Ejercicio 8: Prueba de un algoritmo
        crear_quiz(
            lesson=l6,
            order=8,
            title='Algoritmo 8: Verificación',
            question='¿Cuál es el método para verificar que un algoritmo es correcto?',
            options='Confiar en la intuición|Hacer seguimiento (tracing) con datos de prueba|Ejecutarlo una vez|Preguntarle a otro',
            correct_idx=1,
            explanation='El tracing o seguimiento manual con datos de prueba verifica la correctitud.',
        )

        # Ejercicio 9: Ejemplo de algoritmo
        crear_quiz(
            lesson=l6,
            order=9,
            title='Algoritmo 9: Problema cotidiano',
            question='¿Cuál es un algoritmo que usas en la vida diaria?',
            options='Pensar en la escuela|Seguir una receta de cocina|Soñar|Mirar televisión',
            correct_idx=1,
            explanation='Seguir una receta es un algoritmo: pasos ordenados para lograr un resultado.',
        )

        # Ejercicio 10: Pseudocódigo
        crear_quiz(
            lesson=l6,
            order=10,
            title='Algoritmo 10: Pseudocódigo',
            question='¿Qué es el pseudocódigo?',
            options='Código que no funciona|Descripción en lenguaje natural que simula código|Un lenguaje de programación real|Un tipo de diagrama',
            correct_idx=1,
            explanation='El pseudocódigo es una forma de escribir algoritmos usando lenguaje natural y símbolos, sin sintaxis de programación.',
        )

        # =====================================================
        # STAGE 7 — FUNCIONES
        # =====================================================
        s7 = RoadmapStage.objects.create(
            title='Funciones',
            icon='⚙️',
            order=7,
            difficulty='medium',
        )

        l7 = RoadmapLesson.objects.create(
            stage=s7,
            title='Funciones básicas',
            status='locked',
            xp_reward=220,
            order=1,
            difficulty='medium',
        )

        # Ejercicio 1: Calcular área de rectángulo
        ex1 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 1: Área de rectángulo',
            description='Crea una función que calcule el área de un rectángulo.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=1,
            starter_code=(
                'def area_rectangulo(base, altura):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex1,
            description='area_rectangulo(5,2)',
            input_data='area_rectangulo(5,2)',
            expected='10',
            order=1,
        )

        # Ejercicio 2: Calcular perímetro
        ex2 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 2: Perímetro de cuadrado',
            description='Crea una función que calcule el perímetro de un cuadrado.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=2,
            starter_code=(
                'def perimetro(lado):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex2,
            description='perimetro(5)',
            input_data='perimetro(5)',
            expected='20',
            order=1,
        )

        # Ejercicio 3: Convertir Celsius a Fahrenheit
        ex3 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 3: Conversión de temperatura',
            description='Crea una función que convierta Celsius a Fahrenheit.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=3,
            starter_code=(
                'def celsius_a_fahrenheit(c):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex3,
            description='celsius_a_fahrenheit(0)',
            input_data='celsius_a_fahrenheit(0)',
            expected='32',
            order=1,
        )

        # Ejercicio 4: Calcular descuento
        ex4 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 4: Aplicar descuento',
            description='Crea una función que calcule el precio con descuento.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=4,
            starter_code=(
                'def aplicar_descuento(precio, porcentaje):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex4,
            description='aplicar_descuento(100, 10)',
            input_data='aplicar_descuento(100, 10)',
            expected='90',
            order=1,
        )

        # Ejercicio 5: Validar contraseña
        ex5 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 5: Validar contraseña',
            description='Crea una función que valide si una contraseña es fuerte (al menos 8 caracteres).',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=5,
            starter_code=(
                'def es_fuerte(password):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex5,
            description='es_fuerte("miPassword123")',
            input_data='es_fuerte("miPassword123")',
            expected='True',
            order=1,
        )

        # Ejercicio 6: Concatenar strings
        ex6 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 6: Saludar con nombre',
            description='Crea una función que concatene un saludo con un nombre.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=6,
            starter_code=(
                'def saludar(nombre):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex6,
            description='saludar("Juan")',
            input_data='saludar("Juan")',
            expected='Hola, Juan',
            order=1,
        )

        # Ejercicio 7: Calcular potencia
        ex7 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 7: Potencia',
            description='Crea una función que calcule la potencia de un número.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=7,
            starter_code=(
                'def potencia(base, exponente):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex7,
            description='potencia(2, 3)',
            input_data='potencia(2, 3)',
            expected='8',
            order=1,
        )

        # Ejercicio 8: Calcular promedio
        ex8 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 8: Promedio de notas',
            description='Crea una función que calcule el promedio de una lista de notas.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=8,
            starter_code=(
                'def promedio(notas):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex8,
            description='promedio([80, 90, 100])',
            input_data='promedio([80, 90, 100])',
            expected='90',
            order=1,
        )

        # Ejercicio 9: Mayor de dos números
        ex9 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 9: Mayor de dos números',
            description='Crea una función que retorne el mayor de dos números.',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=9,
            starter_code=(
                'def mayor(a, b):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex9,
            description='mayor(15, 23)',
            input_data='mayor(15, 23)',
            expected='23',
            order=1,
        )

        # Ejercicio 10: Calcular IMC
        ex10 = RoadmapExercise.objects.create(
            lesson=l7,
            title='Función 10: Índice de Masa Corporal',
            description='Crea una función que calcule el IMC (peso / altura²).',
            exercise_type='code',
            difficulty='medium',
            xp_reward=25,
            time_limit_secs=300,
            max_attempts=3,
            order=10,
            starter_code=(
                'def calcular_imc(peso, altura):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex10,
            description='calcular_imc(70, 1.75)',
            input_data='calcular_imc(70, 1.75)',
            expected='22.86',
            order=1,
        )

        # =====================================================
        # STAGE 8 — RESOLUCIÓN DE PROBLEMAS
        # =====================================================
        s8 = RoadmapStage.objects.create(
            title='Resolución de problemas',
            icon='🧩',
            order=8,
            difficulty='hard',
        )

        l8 = RoadmapLesson.objects.create(
            stage=s8,
            title='Problemas clásicos',
            status='locked',
            xp_reward=250,
            order=1,
            difficulty='hard',
        )

        # Ejercicio 1: FizzBuzz
        ex1 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 1: FizzBuzz',
            description='Retorna "Fizz" si es múltiplo de 3, "Buzz" si es múltiplo de 5, "FizzBuzz" si es ambos, sino el número.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=1,
            starter_code=(
                'def fizzbuzz(n):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex1,
            description='fizzbuzz(15)',
            input_data='fizzbuzz(15)',
            expected='FizzBuzz',
            order=1,
        )

        # Ejercicio 2: Verificar palíndromo
        ex2 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 2: Palíndromo',
            description='Verifica si una palabra es palíndromo (se lee igual de adelante y atrás).',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=2,
            starter_code=(
                'def es_palindromo(texto):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex2,
            description='es_palindromo("radar")',
            input_data='es_palindromo("radar")',
            expected='True',
            order=1,
        )

        # Ejercicio 3: Número primo
        ex3 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 3: Número primo',
            description='Verifica si un número es primo.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=3,
            starter_code=(
                'def es_primo(n):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex3,
            description='es_primo(17)',
            input_data='es_primo(17)',
            expected='True',
            order=1,
        )

        # Ejercicio 4: Invertir número
        ex4 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 4: Invertir número',
            description='Invierte los dígitos de un número.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=4,
            starter_code=(
                'def invertir_numero(n):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex4,
            description='invertir_numero(12345)',
            input_data='invertir_numero(12345)',
            expected='54321',
            order=1,
        )

        # Ejercicio 5: Suma de dígitos
        ex5 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 5: Suma de dígitos',
            description='Suma todos los dígitos de un número.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=5,
            starter_code=(
                'def suma_digitos(n):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex5,
            description='suma_digitos(123)',
            input_data='suma_digitos(123)',
            expected='6',
            order=1,
        )

        # Ejercicio 6: Búsqueda binaria
        ex6 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 6: Búsqueda binaria',
            description='Busca un elemento en lista ordenada usando búsqueda binaria.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=6,
            starter_code=(
                'def busqueda_binaria(lista, objetivo):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex6,
            description='busqueda_binaria([1, 3, 5, 7, 9], 5)',
            input_data='busqueda_binaria([1, 3, 5, 7, 9], 5)',
            expected='2',
            order=1,
        )

        # Ejercicio 7: Máximo común divisor
        ex7 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 7: MCD (Máximo Común Divisor)',
            description='Calcula el máximo común divisor de dos números (algoritmo de Euclides).',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=7,
            starter_code=(
                'def mcd(a, b):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex7,
            description='mcd(48, 18)',
            input_data='mcd(48, 18)',
            expected='6',
            order=1,
        )

        # Ejercicio 8: Ordenamiento por burbuja
        ex8 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 8: Ordenamiento de burbuja',
            description='Ordena una lista usando el algoritmo de ordenamiento de burbuja.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=8,
            starter_code=(
                'def burbuja(lista):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex8,
            description='burbuja([5, 2, 8, 1])',
            input_data='burbuja([5, 2, 8, 1])',
            expected='[1, 2, 5, 8]',
            order=1,
        )

        # Ejercicio 9: Números de Fibonacci hasta n
        ex9 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 9: Fibonacci - suma hasta n',
            description='Suma todos los números Fibonacci menores o iguales a n.',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=9,
            starter_code=(
                'def suma_fibonacci(n):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex9,
            description='suma_fibonacci(10)',
            input_data='suma_fibonacci(10)',
            expected='20',
            order=1,
        )

        # Ejercicio 10: Anagrama
        ex10 = RoadmapExercise.objects.create(
            lesson=l8,
            title='Problema 10: Anagrama',
            description='Verifica si dos palabras son anagramas (contienen las mismas letras).',
            exercise_type='code',
            difficulty='hard',
            xp_reward=30,
            time_limit_secs=420,
            max_attempts=3,
            order=10,
            starter_code=(
                'def es_anagrama(palabra1, palabra2):\n'
                '    # Tu código aquí\n'
                '    pass'
            ),
        )
        RoadmapTestCase.objects.create(
            exercise=ex10,
            description='es_anagrama("listen", "silent")',
            input_data='es_anagrama("listen", "silent")',
            expected='True',
            order=1,
        )

        self.stdout.write(
            self.style.SUCCESS(
                '✅ Roadmap cargado con 10 ejercicios por stage.'
            )
        )