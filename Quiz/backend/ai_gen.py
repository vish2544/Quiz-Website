# backend/ai_gen.py
import os
import random
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def _fallback_generate(language, level, n=10):
    """Simple fallback generator when no external AI available."""
    base_q = [
        ("What is the output of the following {} code snippet that prints numbers 0 to 2?",
         ["0 1 2", "1 2 3", "0 1 2 3", "error"]),
        ("Which keyword is used to define a function in {}?",
         ["func", "def", "function", "declare"]),
        ("Which data type is immutable in {}?",
         ["list", "tuple", "dict", "set"]),
        ("What is the correct file extension for {} source files?",
         [".{}src", ".{}code", ".{}", ".{}file"]),
    ]
    qlist = []
    for i in range(n):
        tmpl, opts = random.choice(base_q)
        question = tmpl.format(language)
        # produce four options, randomly pick correct one
        if "{}" in opts[0]:
            # replace when placeholders used
            opts = [o.replace("{}", language.lower()) for o in opts]
        # choose a correct index randomly
        correct_index = random.randrange(4)
        # ensure options are distinct by shuffling and filling with filler if needed
        while len(set(opts)) < 4:
            opts = opts + ["Unknown"]
        opts_shuffled = random.sample(opts, 4)
        correct_option = opts_shuffled[0]  # for fallback we'll declare first as correct
        qlist.append({
            "question_text": question + f" (level: {level})",
            "options": opts_shuffled,
            "correct_option": correct_option,
            "explanation": f"Fallback explanation for {language}."
        })
    return qlist

def generate_questions_via_openai(language, level, n=10):
    import openai
    openai.api_key = OPENAI_KEY
    prompt = f"""Generate {n} multiple choice programming questions for language: {language}, difficulty: {level}.
Return JSON array with fields: question_text, options (array of 4), correct_option (the correct text), explanation.
Do not include anything else."""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o" if "gpt-4o" in openai.Model.list() else "gpt-4o-mini",
            messages=[{"role":"system","content":"You are a helpful quiz generator."},
                      {"role":"user","content":prompt}],
            max_tokens=1500,
            temperature=0.7,
        )
        text = resp.choices[0].message.content
        # Expecting JSON — attempt to parse
        import json
        data = json.loads(text)
        # normalize to our structure
        qlist = []
        for item in data:
            qlist.append({
                "question_text": item.get("question_text"),
                "options": item.get("options"),
                "correct_option": item.get("correct_option"),
                "explanation": item.get("explanation", "")
            })
        return qlist
    except Exception as e:
        print("OpenAI generation failed:", e)
        return _fallback_generate(language, level, n)

def generate_questions(language, level, n=10):
    if OPENAI_KEY:
        return generate_questions_via_openai(language, level, n)
    else:
        return _fallback_generate(language, level, n)
