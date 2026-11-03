from uuid import uuid4

import streamlit as st

from app.common import money
from core.domain import Transaction
from core.transforms import account_balance, add_transaction


def render(accounts, categories, transactions, budgets, lab):
    st.header("Функционалды ядро")
    st.subheader("№1 — өзгермейтін модельдер және таза функциялар")
    aid = st.selectbox(
        "Баланс есептелетін шот",
        [a.id for a in accounts],
        format_func=lambda x: next(a.name for a in accounts if a.id == x),
    )
    st.metric(
        "account_balance: транзакциялар қосындысы",
        money(account_balance(transactions, aid)),
    )
    st.code(
        "new_trans = add_transaction(old_trans, t)\nnew_budgets = update_budget(old_budgets, bid, new_limit)\n# old_trans және old_budgets өзгермейді",
        language="python",
    )
    if st.button("Immutable қосу үлгісі"):
        demo = Transaction(
            "demo-" + uuid4().hex,
            aid,
            "salary",
            1000,
            max(t.ts for t in transactions),
            "Тек мысал",
        )
        updated = add_transaction(transactions, demo)
        st.success(
            f"Ескі tuple: {len(transactions)}, жаңа tuple: {len(updated)}. Үлгі сессияға сақталмайды."
        )
    if lab >= 2:
        st.subheader("№2 — lambda және тұйықтаулар")
        st.code(
            "pred = by_category('groceries')\nresult = tuple(filter(pred, transactions))",
            language="python",
        )
        st.write(
            "Күн/сома сүзгілері мен екі рекурсивті функция «Конвейерлер / Pipelines» бөлімінде."
        )
    if lab < 4:
        return
    from core.validation import safe_category, validate_pipeline

    st.subheader("№4 — Maybe және Either")
    query = st.text_input("Maybe арқылы категория іздеу (ID)", "groceries")
    name = (
        safe_category(categories, query)
        .map(lambda c: c.name)
        .get_or_else("Категория жоқ: Nothing")
    )
    st.write(name)
    st.write(
        "Сынақ үшін жоқ шот/категория ID-ін немесе қате күнді енгізіңіз. Үлкен теріс сома бюджеттен асуды көрсетеді."
    )
    st.caption("ID анықтамасы: " + "; ".join(f"{c.id} — {c.name}" for c in categories))
    with st.form("transaction_form"):
        account_id = st.text_input("Шот ID", accounts[0].id)
        cat_id = st.text_input("Категория ID", "groceries")
        amount = st.number_input("Сома (кіріс +, шығыс −)", value=-1000, step=100)
        ts = st.text_input("Күн (YYYY-MM-DD)", max(t.ts for t in transactions))
        note = st.text_input("Ескерту", "Жаңа транзакция")
        save = st.checkbox("Тексеруден өтсе, сессияға сақтау", value=False)
        submitted = st.form_submit_button("Транзакцияны тексеру")
    if submitted:
        t = Transaction(uuid4().hex, account_id, cat_id, amount, ts, note)
        result = validate_pipeline(t, accounts, categories, budgets, transactions)
        if result.is_right:
            if save:
                st.session_state.transactions = add_transaction(
                    transactions, result.value
                )
                st.session_state.notice = "Тексерулер өтті: транзакция сақталды."
                st.rerun()
            st.success("Right: шот, категория, сома, күн және бюджет тексерулері өтті.")
        else:
            st.error("Left: " + result.value["message"])
            st.json(result.value)
