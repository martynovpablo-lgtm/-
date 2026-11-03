from datetime import date

import streamlit as st

from app.common import money, table
from core.recursion import flatten_categories, sum_expenses_recursive
from core.transforms import (
    by_amount_range,
    by_category,
    by_date_range,
    filter_transactions,
)


def render(accounts, categories, transactions, budgets, lab):
    st.header("Сүзгілер мен рекурсия")
    options = {c.id: c.name for c in categories}
    category = st.selectbox(
        "Категория сүзгісі",
        ["all"] + list(options),
        format_func=lambda cid: "Барлығы" if cid == "all" else options[cid],
    )
    first = min(date.fromisoformat(t.ts) for t in transactions)
    last = max(date.fromisoformat(t.ts) for t in transactions)
    col1, col2 = st.columns(2)
    start = col1.date_input("Басталу күні", first)
    end = col2.date_input("Аяқталу күні", last)
    col1, col2 = st.columns(2)
    lower = col1.number_input("Ең аз сома (таңбамен)", value=-1000000, step=1000)
    upper = col2.number_input("Ең көп сома (таңбамен)", value=1000000, step=1000)
    if start > end or lower > upper:
        st.error("Күндер немесе сомалар аралығының шектері ауысып кеткен.")
        return
    predicates = [
        by_date_range(start.isoformat(), end.isoformat()),
        by_amount_range(lower, upper),
    ]
    if category != "all":
        predicates.append(by_category(category))
    filtered = filter_transactions(transactions, *predicates)
    st.metric("Табылған транзакциялар", len(filtered))
    table(filtered)
    st.subheader("Иерархия бойынша шығын")
    root = st.selectbox("Иерархия түбірі", list(options), format_func=options.get)
    tree = flatten_categories(categories, root)
    st.write(" → ".join(c.name for c in tree))
    st.metric(
        "Таңдалған аралықтағы ағаш шығыны",
        money(sum_expenses_recursive(categories, filtered, root)),
    )
    st.caption(
        "Категория сүзгісі бір ID-ді таңдайды; ағаш есебі түбірді және барлық ұрпақты қамтиды."
    )
    if lab >= 3:
        st.info("Кэшті және айлық болжамды «Есептер / Reports» бөлімінен тексеріңіз.")
