# Қаржы менеджері — lab-03

Бұл кезең тек 1–3 зертханаларды қамтиды. Болашақ модульдер әлі қосылмаған; мәзірде түсіндірме көрсетіледі.

## Іске қосу (Windows)

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app/main.py
```

Орта белсендірілгенде: `pytest -q`, `black --check .`, `ruff check .`.

Барлық сомалар бүтін теңгемен; кіріс +, шығыс −. Деректер tuple/frozen модельдер.
Өзгерістер браузер сессиясында, Data → JSON жүктеу арқылы көшірме сақталады.

## Навигация

- Overview: 3 шот, 15 категория, 180 транзакция, баланс.
- Data: кестелер, бюджет лимитін жаңарту, JSON.
- Functional Core: reduce және immutable қосу үлгісі.
- Pipelines: үш closure сүзгісі және екі рекурсивті функция.
- Reports: соңғы N күнтізбелік айдың орташа шығыны, lru_cache/ms. Бос айлар есепке кіреді.
- Tests: тексеру командалары; About: сипаттама.
- Async/FRP: кейінгі зертхана туралы түсіндірме.

Құрылым: app/ — UI; core/ — ядро; data/ — seed; tests/ — әр зертхана тесттері.
Үш студенттің нақты файлдары: [TEAM_PLAN](docs/TEAM_PLAN.md).
PR және бейне: [SUBMISSION](docs/SUBMISSION.md). Бұл құжаттар толық төрт кезеңнің жалпы жоспарын сипаттайды.
