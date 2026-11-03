import streamlit as st

from app.common import export_data, table
from core.transforms import update_budget


def render(accounts, categories, transactions, budgets):
    st.header("Деректер")
    for title, items in (
        ("Шоттар", accounts),
        ("Категориялар", categories),
        ("Бюджеттер", budgets),
        ("Транзакциялар", transactions),
    ):
        with st.expander(title, expanded=title == "Транзакциялар"):
            table(items)
    st.subheader("Бюджет лимитін өзгерту")
    with st.form("budget_form"):
        bid = st.selectbox("Бюджет", [b.id for b in budgets])
        new_limit = st.number_input(
            "Жаңа лимит (₸)", min_value=0, value=100000, step=1000
        )
        submitted = st.form_submit_button("Лимитті сақтау")
    if submitted:
        st.session_state.budgets = update_budget(budgets, bid, new_limit)
        st.session_state.notice = "Лимит жаңартылды. Алдыңғы tuple өзгерген жоқ."
        st.rerun()
    st.download_button(
        "JSON жүктеу",
        export_data(accounts, categories, transactions, budgets),
        "financial_data.json",
        "application/json",
    )
    st.info(
        "Өзгерістер осы браузер сессиясында сақталады. JSON жүктеу арқылы көшірме алыңыз."
    )
    if st.button("Бастапқы деректерді қалпына келтіру"):
        for key in ("accounts", "categories", "transactions", "budgets", "timing"):
            st.session_state.pop(key, None)
        st.session_state.notice = "Бастапқы seed қайта жүктелді."
        st.rerun()
