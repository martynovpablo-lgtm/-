import streamlit as st

from app.common import money
from core.memo import benchmark_forecast


def render(accounts, categories, transactions, budgets, lab):
    st.header("Есептер")
    st.subheader("Forecast (cached) — кэштелген болжам")
    options = {c.id: c.name for c in categories if c.type == "expense"}
    cid = st.selectbox("Болжам категориясы", list(options), format_func=options.get)
    period = st.number_input(
        "Соңғы неше ай?", min_value=1, max_value=120, value=3, step=1
    )
    st.caption(
        "Деректегі соңғы күннен бастап N күнтізбелік ай. Бос айлар есепке кіреді. Болжам бір категорияға жасалады."
    )
    if st.button("Болжам және кэш уақытын өлшеу"):
        st.session_state.timing = (
            (cid, period, transactions),
            benchmark_forecast(cid, transactions, period),
        )
    timing = st.session_state.get("timing")
    if timing and timing[0] == (cid, period, transactions):
        result = timing[1]
        st.metric("Келесі айға орташа болжам", money(result["forecast"]))
        st.dataframe(
            [
                {"Есептеу": "Кэшсіз", "Уақыт (ms)": result["uncached_ms"]},
                {"Есептеу": "Кэшке бірінші жазу", "Уақыт (ms)": result["cold_ms"]},
                {
                    "Есептеу": "Кэштен оқу, 30 рет орташа",
                    "Уақыт (ms)": result["warm_ms"],
                },
            ],
            hide_index=True,
            use_container_width=True,
        )
        st.write(
            f"Cache hits: {result['hits']}; misses: {result['misses']}; нәтижелер тең: {result['equal']}"
        )
        st.caption(
            "Өлшем нақты орындалу уақытынан алынады. Шағын деректерде жылдамдық айырмасы аз болуы мүмкін."
        )
    if lab >= 4:
        from core.validation import budget_usage, check_budget

        st.subheader("Бюджет есебі")
        anchor = max(t.ts for t in transactions)
        st.caption(
            f"Тірек күні: {anchor}. Айлық бюджет — сол ай; апталық — дүйсенбі–жексенбі."
        )
        report = []
        for b in budgets:
            result = check_budget(b, transactions)
            spent = budget_usage(b, transactions).get_or_else(0)
            report.append(
                {
                    "ID": b.id,
                    "Категория": options.get(b.cat_id, b.cat_id),
                    "Кезең": "Ай" if b.period == "month" else "Апта",
                    "Шығын": spent,
                    "Лимит": b.limit,
                    "Күй": (
                        "Лимит ішінде" if result.is_right else result.value["message"]
                    ),
                }
            )
        st.dataframe(report, hide_index=True, use_container_width=True)
