import streamlit as st

from app.common import money
from core.transforms import account_balance


def render(accounts, categories, transactions, budgets):
    st.header("Жалпы шолу")
    columns = st.columns(4)
    columns[0].metric("Шоттар", len(accounts))
    columns[1].metric("Категориялар", len(categories))
    columns[2].metric("Транзакциялар", len(transactions))
    total = sum(a.balance + account_balance(transactions, a.id) for a in accounts)
    columns[3].metric("Жалпы баланс", money(total))
    st.write(f"Бюджеттер саны: {len(budgets)}")
    st.dataframe(
        [
            {
                "Шот": a.name,
                "Бастапқы баланс": a.balance,
                "Транзакциялар қосындысы": account_balance(transactions, a.id),
                "Қазіргі баланс": a.balance + account_balance(transactions, a.id),
                "Валюта": a.currency,
            }
            for a in accounts
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.caption("Барлық сомалар бүтін теңгемен. Шығыс теріс, кіріс оң.")
