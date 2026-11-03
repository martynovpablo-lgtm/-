"""Іске қосу: streamlit run app/main.py (репозиторий түбірінен)."""

import sys
from importlib.util import find_spec
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from app import data, functional, overview  # noqa: E402
from core.transforms import load_seed  # noqa: E402

LAB = (
    4
    if find_spec("core.validation")
    else 3 if find_spec("core.memo") else 2 if find_spec("core.recursion") else 1
)
PAGES = {
    "Overview": "Жалпы шолу / Overview",
    "Data": "Деректер / Data",
    "Functional Core": "Функционалды ядро / Functional Core",
    "Pipelines": "Конвейерлер / Pipelines",
    "Async/FRP": "Асинхрондық және оқиғалар / Async/FRP",
    "Reports": "Есептер / Reports",
    "Tests": "Тесттер / Tests",
    "About": "Жоба туралы / About",
}


def main():
    st.set_page_config(
        page_title="Қаржы менеджері",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="auto",
    )
    if "transactions" not in st.session_state:
        values = load_seed(ROOT / "data" / "seed.json")
        for key, value in zip(
            ("accounts", "categories", "transactions", "budgets"), values
        ):
            st.session_state[key] = value
    args = tuple(
        st.session_state[key]
        for key in ("accounts", "categories", "transactions", "budgets")
    )
    st.title("Қаржы менеджері")
    st.sidebar.title("☰ Мәзір")
    page = st.sidebar.radio("Бөлім", list(PAGES), format_func=PAGES.get, key="page")
    st.sidebar.caption(f"Python 3.11+ · 1–{LAB} зертхана · KZT")
    notice = st.session_state.pop("notice", None)
    if notice:
        st.success(notice)
    if page == "Overview":
        overview.render(*args)
    elif page == "Data":
        data.render(*args)
    elif page == "Functional Core":
        functional.render(*args, LAB)
    elif page == "Pipelines" and LAB >= 2:
        from app import pipelines

        pipelines.render(*args, LAB)
    elif page == "Reports" and LAB >= 3:
        from app import reports

        reports.render(*args, LAB)
    elif page == "Tests":
        st.header("Тесттер")
        st.write(
            "Әр зертханаға жеке тест файлы бар. Төмендегі командаларды жоба бумасында орындаңыз."
        )
        st.code(
            "python -m pytest -q\npython -m black --check .\npython -m ruff check .",
            language="bash",
        )
        for number in range(1, LAB + 1):
            st.write(f"№{number}: tests/test_lab{number}.py")
        st.caption(
            "Бұл бет командаларды көрсетеді. Нақты тексеру нәтижелері CHECK_RESULTS.md файлында."
        )
    elif page == "About":
        st.header("Жоба туралы")
        st.write(
            "Функционалды бағдарламалау пәні. Үш студентке арналған 1–4 зертхана жобасы."
        )
        st.write(
            "№1: frozen dataclass, tuple, map/filter/reduce. №2: lambda, тұйықтау, рекурсия. №3: рекурсивті болжам, lru_cache. №4: Maybe/Either және валидация."
        )
        st.caption(
            "README.md — іске қосу; docs/TEAM_PLAN.md — файлдарды бөлу; docs/SUBMISSION.md — төрт PR және бейне қорғау."
        )
    else:
        st.info(
            "Бұл бөлімнің функциялары кейінгі зертханаларға жатады. Осы тапсыруда 1–4 зертхана орындалады."
        )


if __name__ == "__main__":
    main()
