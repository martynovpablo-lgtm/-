# Талап → іске асыру → тексеру

Негіз: жоба PDF-інің 1–4 беттері (алғашқы төрт зертхана), 7–8 беттері (жалпы чеклист).
Тек 1–4 зертхана орындалады. Кейінгі 5–8 зертхананың lazy/FRP/async/service модульдері бұл көлемге кірмейді.

| Талап | Код | UI | Автотексеру |
|---|---|---|---|
| Python 3.11+, Streamlit | pyproject.toml, requirements.txt | app/main.py | Іске қосу және AppTest |
| 8 бөлім, бүйір мәзір | app/main.py | Барлық бөлім | test_ui.py |
| Account, Category, Transaction, Budget, Event immutable | core/domain.py | Data | test_lab1.py |
| ≥3/10/100/3 seed | data/seed.json | Overview, Data | seed көлемі мен сілтемелері |
| Питание/транспорт/досуг иерархиясы | food/transport/leisure және ұрпақтары | Pipelines | test_lab2.py |
| load_seed → tuple | core/transforms.py | Алғашқы жүктеу | test_lab1.py |
| add_transaction → жаңа tuple | core/transforms.py | Functional Core | test_lab1.py |
| update_budget → жаңа tuple | core/transforms.py | Data | test_lab1.py, test_ui.py |
| account_balance reduce | core/transforms.py | Overview, Functional Core | test_lab1.py |
| map/filter/reduce | transforms.py | Деректер, баланс, сүзгілер | test_lab1.py, test_lab2.py |
| by_category/by_date_range/by_amount_range closures | core/transforms.py | Pipelines | test_lab2.py |
| flatten_categories рекурсия | core/recursion.py | Pipelines | түбір, ұрпақ, жоқ түбір, цикл |
| sum_expenses_recursive рекурсия | core/recursion.py | Pipelines | таңба, ұрпақ, басқа категория |
| forecast_expenses(cat_id, tuple, period) @lru_cache | core/memo.py | Reports | test_lab3.py |
| Кеңейтілген рекурсия | _sum_months бөліп есептеу | Reports | жыл шекарасы, бос ай |
| ms кэшке дейін/кейін | benchmark_forecast | Reports → Forecast (cached) | уақыт ≥0, hits/misses, нәтиже тең |
| Maybe/Either map/bind/get_or_else | core/ftypes.py | Functional Core | test_lab4.py |
| safe_category → Maybe | core/validation.py | Functional Core іздеу | бар/жоқ категория |
| validate_transaction → Either[dict, Transaction] | core/validation.py | Транзакция формасы | дұрыс/қате шот, күн, таңба |
| check_budget → Either[dict, Budget] | core/validation.py | Reports | ай/апта, тең лимит, асу |
| Валидация пайплайны | validate_pipeline | Functional Core | bind қатені тоқтатады, енгізу күні |
| ≥5 pytest әр зертханаға | tests/test_lab1..4.py | Tests | CHECK_RESULTS.md |
| black/ruff | pyproject.toml | Tests командалары | CHECK_RESULTS.md |
| README, үлестер, төрт PR, 2 минут видео | README, TEAM_PLAN, SUBMISSION | About | Қолмен тапсыру |

## Силлабуспен байланыс

Силлабустың 4–5 беттеріндегі 1–8 дәрістер:

| Дәріс тақырыбы | Жобадағы көрсетілім |
|---|---|
| Функционалды бағдарламалауға кіріспе | таза ядро мен UI/I/O шекарасы |
| Python негіздері | типтер, dataclass, tuple |
| Функциялар және өзгермейтіндік | frozen, жаңа жинақтар |
| Жоғары ретті функциялар | map/filter/reduce, predicate функциялар |
| Лямбда және тұйықтаулар | үш тәуелсіз closure сүзгісі |
| Рекурсия және деректер құрылымдары | категория ағашы, preorder, рекурсивті қосынды |
| Кеңейтілген рекурсия және мемоизация | бөліп есептеу, lru_cache, уақыт |
| Функционалды үлгілер және құрылымдар | Maybe/Either, map/bind, error short-circuit |

Силлабус тақырыптарды белгілейді; нақты функциялар мен тапсыру шарттарын жоба PDF-і белгілейді.
Лекция мәтіні берілмеген. Силлабус кестесіндегі жоспарлы апталар нақты күнтізбелік дедлайн ретінде алынбады.
