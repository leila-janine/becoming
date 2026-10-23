SOURCES = [
    {'title':'Starting before the deadline', 'publisher':'Centre for Clinical Interventions, Government of Western Australia', 'url':'https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Procrastination', 'basis':'Clinical self-help resource', 'use':'Notice avoidance, define a concrete next action, and experiment with a short start. The app’s five-minute start is an adjustable design choice, not a guaranteed treatment.'},
    {'title':'Clear, kind boundaries', 'publisher':'Centre for Clinical Interventions', 'url':'https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Assertiveness', 'basis':'Clinical self-help resource', 'use':'Practice expressing your needs directly while respecting the other person. Try a low-stakes situation before a difficult conversation.'},
    {'title':'When intention needs a plan', 'publisher':'US National Cancer Institute, DCCPS', 'url':'https://cancercontrol.cancer.gov/brp/research/constructs/implementation-intentions', 'basis':'Research construct summary', 'use':'Attach an action to a specific cue: “If I finish dinner, then I will open the graduation checklist.” This can help translate an intention into action; it does not remove practical barriers.'},
    {'title':'Remember more of what you learn', 'publisher':'Dunlosky et al., Psychological Science in the Public Interest (2013)', 'url':'https://doi.org/10.1177/1529100612453266', 'basis':'Research review', 'use':'Practice retrieving ideas without notes and revisit them across days. The app’s 1, 2, 4 day review intervals are a simple adjustable heuristic, not an individually validated schedule.'},
    {'title':'Stuttering and communication', 'publisher':'ASHA / Communication Health and Speech Alliance', 'url':'https://www.asha.org/public/speech/disorders/stuttering/', 'basis':'Professional patient information', 'use':'Stuttering varies and has multiple contributing factors. A speech-language pathologist can assess your needs and support communication goals. This app tracks participation and message clarity, not “perfect” fluency, and does not diagnose or treat stuttering.'},
    {'title':'A spending plan that fits real life', 'publisher':'US Consumer Financial Protection Bureau', 'url':'https://www.consumerfinance.gov/consumer-tools/educator-tool/your-money-your-goals/toolkit/', 'basis':'Financial education toolkit', 'use':'Track actual income, spending, bills, and payment timing. The app uses Philippine pesos and lets you reserve money for enjoyment. Its categories are a planning adaptation, not a prescribed allocation.'},
    {'title':'A cushion for the unexpected', 'publisher':'US Consumer Financial Protection Bureau', 'url':'https://www.consumerfinance.gov/an-essential-guide-to-building-an-emergency-fund/', 'basis':'Financial education guidance', 'use':'An emergency reserve helps absorb unplanned costs. Set the amount around your own expenses and start with a manageable contribution. Calculations here assume no investment returns and are not product recommendations.'},
    {'title':'AI apps and agents certification', 'publisher':'Microsoft Learn', 'url':'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103', 'basis':'Official current exam study guide', 'use':'Use the official skills outline to identify gaps and build hands-on evidence. Track your own exam status; no certification is assumed to be earned. Recheck the official page before paying or scheduling.'},
    {'title':'Python data structures', 'publisher':'Python Software Foundation', 'url':'https://docs.python.org/3/tutorial/datastructures.html', 'basis':'Official language tutorial', 'use':'Use lists, sets, and dictionaries intentionally. The Coding practice exercises ask you to preserve order, handle edge cases, and explain complexity. Exercises are original examples, not copied exam questions.'},
    {'title':'Dart collections and maintainable code', 'publisher':'Dart team', 'url':'https://dart.dev/effective-dart', 'basis':'Official language guidance', 'use':'Read the language and design guidance while practicing deterministic collection operations. Move a pure rule out of a widget so it is easier to explain and test.'},
    {'title':'Testing Flutter applications', 'publisher':'Flutter team', 'url':'https://docs.flutter.dev/testing/overview', 'basis':'Official testing documentation', 'use':'Distinguish unit tests for individual rules, widget tests for UI behavior, and integration tests for broader app flows. Choose a test that catches a real failure in your own project.'},
    {'title':'SQL joins', 'publisher':'PostgreSQL Global Development Group', 'url':'https://www.postgresql.org/docs/current/tutorial-join.html', 'basis':'Official database tutorial', 'use':'Practice which rows a join includes and excludes. Use a disposable practice database and verify both matched and unmatched rows.'},
    {'title':'HTTP idempotency', 'publisher':'MDN Web Docs', 'url':'https://developer.mozilla.org/en-US/docs/Glossary/Idempotent', 'basis':'Maintainer documentation', 'use':'Understand the intended effects of repeated requests. The systems exercise asks you to reason about retries, duplicate operations, and database constraints; it is not a production payment implementation.'},
]

CAREER_PRIORITIES = ['AI Engineer', 'Data Engineer', 'Data Analytics', 'Software Engineering']

RESUME_FOUNDATIONS = [
    ('AI Engineer', 'Your RAG, computer vision, PyTorch/TensorFlow, and traffic-forecasting projects provide starting material.', 'Strengthen evaluation, data leakage checks, retrieval quality, model serving, and monitoring. Build one small AI service with documented failure cases.'),
    ('Data Engineer', 'Your database skills, traffic-data pipeline, API scraping, and automation work provide starting material.', 'Practice SQL, reproducible ingestion, schema validation, idempotent loads, data modelling, and pipeline observability.'),
    ('Data Analytics', 'Your Python, data-analysis projects, QA/UAT, and stakeholder work provide starting material.', 'Define a decision question, clean the data, choose defensible measures, and explain the finding with uncertainty and a useful chart.'),
    ('Software Engineering', 'Your Flutter/Dart, API integration, state management, debugging, and testing experience provide starting material.', 'Keep improving algorithms, modular design, API contracts, tests, code review, CI, and technical explanations as shared foundations.'),
]

TRACKS = {
    'AI Engineer': [
        ('Evaluate first', 'Choose one existing AI project. Define a baseline, held-out evaluation set, leakage checks, and failure cases before changing the model.', 'https://scikit-learn.org/stable/common_pitfalls.html'),
        ('Improve a RAG or ML component', 'For your local-manual RAG, test retrieval relevance, answer grounding, and unanswerable questions. Keep an experiment log without inventing accuracy claims.', 'https://learn.microsoft.com/en-us/azure/ai-foundry/'),
        ('Serve and test the feature', 'Expose one narrow AI feature through FastAPI; validate inputs, test failure paths, and record latency and resource use in your own environment.', 'https://fastapi.tiangolo.com/tutorial/testing/'),
        ('Credential as a supporting goal', 'Your resume lists OCI AI Certified Associate (2025). Record its verification link and renewal details. Use the official AI-103 outline to choose a next lab if it serves your target role.', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103'),
    ],
    'Data Engineer': [
        ('Model and query', 'Use a small public or synthetic dataset. Define keys, constraints, joins, and a documented schema. Explain one query plan.', 'https://www.postgresql.org/docs/current/tutorial.html'),
        ('Build repeatable ingestion', 'Turn a traffic-data or public-API sample into a repeatable load. Validate records, quarantine bad rows, and show that rerunning the same batch does not duplicate data.', 'https://docs.python.org/3/library/json.html'),
        ('Orchestrate and observe', 'Add clear pipeline stages, a retry policy, logs, and quality checks. Learn orchestration with a small practice workflow rather than adding every tool at once.', 'https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html'),
        ('Keep evidence', 'Document data lineage, a failed-load recovery, and the result of a repeat-run test. Share a sanitized example, never employer data.', 'https://docs.github.com/en/actions'),
    ],
    'Data Analytics': [
        ('Start with a decision', 'Ask one concrete question about a public or synthetic dataset. Specify the audience, unit of analysis, and metric definition.', 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html'),
        ('Check the data', 'Inspect missing values, duplicates, units, outliers, and denominators. Explain which cleaning choices could change the conclusion.', 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html'),
        ('Explain a finding', 'Create one readable chart and a short decision memo. Distinguish correlation from a causal claim and state the limits of the data.', 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html'),
    ],
    'Software Engineering': [
        ('Programming depth', 'Practice Python data structures and edge cases, then explain the cost of your approach. Keep Dart/Flutter skills active through your current work.', 'https://docs.python.org/3/tutorial/'),
        ('Modular systems and tests', 'Extract one pure rule from your app, test it, and review the boundary between UI, state, and data access.', 'https://docs.flutter.dev/app-architecture/guide'),
        ('Reliable delivery', 'Add API tests and CI to one portfolio project. Show what a failing test caught and how you fixed it.', 'https://docs.github.com/en/actions/tutorials/build-and-test-code/python'),
    ],
}

PROMPTS = {
    'Explain a technical idea': ('Point → reason → example → point', 'Explain a recent bug fix to a teammate. What changed, why, and how did you verify it?'),
    'Tell a career story': ('Situation → task → action → result', 'Describe a difficult project decision. Use only results you can support with evidence.'),
    'Set a kind boundary': ('Observation → impact → request', 'A last-minute request conflicts with graduation work. State what you can do and ask which priority should move.'),
    'Ask a clear question': ('Context → what I tried → specific ask', 'You are blocked on a task. Explain the context in two sentences, what you tried, and what help you need.'),
}

WEEKLY_PROMPTS = [
    'What moved forward, even a little?',
    'What got in the way: unclear task, too much work, low energy, or a practical constraint?',
    'What can I remove or make smaller next week?',
    'What is one kind boundary I need?',
    'Which one project will provide the strongest evidence for my target role?',
]
