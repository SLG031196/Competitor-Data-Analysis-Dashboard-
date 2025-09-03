import streamlit as st
from datetime import date
from utils.db import run_query_with_params
from utils import charts

st.set_page_config(page_title="Scrapped Dashboard", layout="wide", page_icon="📊")
st.title("📊 WPS_Dashboard")

# ============================
# 🌐 Global Filters
# ============================
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", date(2025, 7, 1))
with col2:
    end_date = st.date_input("End Date", date(2025, 8, 30))

# Fetch subcategories dynamically (Query 1 without subcategory filtering)
subcat_df = run_query_with_params(
    "queries/query1.sql",
    (start_date, end_date, None, None)  # tuple for MySQL positional params
)

subcategory_options = sorted(subcat_df["Sub_category"].dropna().unique())
subcategory_choice = st.selectbox("Select Subcategory", ["All"] + list(subcategory_options))
subcategory_param = None if subcategory_choice == "All" else subcategory_choice

st.markdown("---")

# ============================
# 📋 Show All Tables on Top
# ============================
st.subheader("📋 Full Data Views")

colA, colB, colC = st.columns(3)

# Report 1 Table
with colA:
    st.markdown("**Report 1: Sent Terms**")
    df1 = run_query_with_params(
        "queries/query1.sql",
        (start_date, end_date, subcategory_param, subcategory_param)
    )
    st.dataframe(df1, use_container_width=True)

# Report 2 Table
with colB:
    st.markdown("**Report 2: Rendered Terms**")
    df2 = run_query_with_params(
        "queries/query2.sql",
        (start_date, end_date, subcategory_param, subcategory_param)
    )
    st.dataframe(df2, use_container_width=True)

# Report 3 Table
with colC:
    st.markdown("**Report 3: Headlines**")
    df3 = run_query_with_params(
        "queries/query3.sql",
        (start_date, end_date, subcategory_param, subcategory_param)
    )
    st.dataframe(df3, use_container_width=True)

st.markdown("---")

# ============================
# 📊 Extra Visuals & Insights
# ============================
# st.subheader("📈 Key Insights")

# # Row 1 — Top term counts from Query 1 and Query 2
# c1, c2 = st.columns(2)
# with c1:
#     if not df1.empty and "sent_term_count" in df1.columns:
#         fig1 = charts.bar_chart(
#             df1.head(15),
#             x="sent_term",
#             y="sent_term_count",
#             title="Top 15 Sentiment Terms"
#         )
#         st.plotly_chart(fig1, use_container_width=True)

# with c2:
#     if not df2.empty and "rendered_term_count" in df2.columns:
#         fig2 = charts.bar_chart(
#             df2.head(15),
#             x="rendered_term",
#             y="rendered_term_count",
#             title="Top 15 Rendered Terms"
#         )
#         st.plotly_chart(fig2, use_container_width=True)

# Row 2 — Headlines summary from Query 3
if not df3.empty:
    st.subheader("📰 Headlines Summary")
    headline_counts = df3.groupby("Sub_category").size().reset_index(name="Headline Count")
    fig3 = charts.bar_chart(
        headline_counts,
        x="Sub_category",
        y="Headline Count",
        title="Headline Count by Subcategory"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.write("**Sample Headlines:**")
    st.table(df3.head(10))
