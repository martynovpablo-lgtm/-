"""Бетке ортақ ұсақ көрсету функциялары."""

import json
from dataclasses import asdict

import streamlit as st


def rows(items):
    return [asdict(item) for item in items]


def table(items):
    data = rows(items)
    if data:
        st.dataframe(data, hide_index=True, use_container_width=True)
    else:
        st.info("Дерек жоқ")


def money(value):
    return f"{value:,} ₸".replace(",", " ")


def export_data(accounts, categories, transactions, budgets):
    return json.dumps(
        {
            "accounts": rows(accounts),
            "categories": rows(categories),
            "transactions": rows(transactions),
            "budgets": rows(budgets),
        },
        ensure_ascii=False,
        indent=2,
    )
