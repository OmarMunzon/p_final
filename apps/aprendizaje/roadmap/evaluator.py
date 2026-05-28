from .judge0 import run_code


def evaluate_code(exercise, user_code):
    print("Evaluando código del ejercicio:", exercise.title)
    print("Código del usuario:\n", user_code)
    results = []
    for tc in exercise.test_cases.all():
        full = f'{user_code}\n\nprint({tc.input_data})'
        r    = run_code(full, language='python')
        out  = r['stdout'].strip()
        ok   = r['accepted'] and out == tc.expected.strip()
        results.append({
            'description': tc.description,
            'expected':    tc.expected,
            'output':      out if r['accepted'] else r['stderr'].strip(),
            'passed':      ok,
            'is_hidden':   tc.is_hidden,
            'exec_time':   r.get('time'),
            'status':      r['status'],
        })
    return results


def evaluate_fill(exercise, user_answers):
    correct_answers = exercise.get_fill_answers_list()
    answers_ok = all(
        u.strip() == c
        for u, c in zip(user_answers, correct_answers)
    )

    # Reconstruir código y ejecutar contra test cases
    code = exercise.fill_template
    for ans in user_answers:
        code = code.replace('___', ans, 1)

    results = []
    for tc in exercise.test_cases.all():
        full = f'{code}\nprint({tc.input_data})'
        r    = run_code(full, language='python')
        out  = r['stdout'].strip()
        ok   = r['accepted'] and out == tc.expected.strip()
        results.append({
            'description': tc.description,
            'expected':    tc.expected,
            'output':      out,
            'passed':      ok,
            'is_hidden':   tc.is_hidden,
        })

    # Si no hay test cases, usar solo comparación de respuestas
    if not results:
        results = [{'passed': answers_ok, 'description': 'Respuestas', 'is_hidden': False}]

    return results, answers_ok


def evaluate_quiz(exercise, user_answer):
    results = []
    for q in exercise.quiz_questions.all():
        # user_ans = user_answers_dict.get(str(q.id))
        user_ans = user_answer
        correct  = user_ans is not None and int(user_ans) == q.correct_idx
        results.append({
            'question_id': q.id,
            'passed':      correct,
            'correct_idx': q.correct_idx,
            'is_hidden':   False,
        })
    return results


def calculate_score(exercise, attempts, time_spent, passed):
    if not passed:
        return 0
    base         = exercise.xp_reward
    attempt_mult = max(0.4, 1.0 - (attempts - 1) * 0.2)
    time_ratio   = time_spent / max(exercise.time_limit_secs, 1)
    time_mult    = 1.2 if time_ratio < 0.4 else (1.0 if time_ratio < 0.8 else 0.8)
    return round(base * attempt_mult * time_mult)