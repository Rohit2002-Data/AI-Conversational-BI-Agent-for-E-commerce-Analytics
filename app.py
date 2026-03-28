import streamlit as st
import pandas as pd
from io import StringIO

from db_setup import load_database
from tools import generate_sql, execute_sql, generate_insights
from visualization import generate_chart

st.set_page_config(page_title="AI BI Agent", layout="wide")

st.title("🚀 AI Conversational BI Agent")

con = load_database()

query = st.text_input("Ask your business question:")

if st.button("Run Query"):

    if query:
        with st.spinner("Processing..."):

            # SQL
            sql_query = generate_sql.invoke(query)

            st.subheader("🧾 Generated SQL")

            if not sql_query:
                st.error("❌ Failed to generate SQL. Try clearer question.")
                st.stop()

            st.code(sql_query, language="sql")

            # Execute
            result = execute_sql.invoke(sql_query)

            st.subheader("📊 Query Result")

            if "ERROR" in result:
                st.error(result)
                st.stop()

            try:
                df = pd.read_csv(StringIO(result))
                st.dataframe(df)

                fig = generate_chart(df)
                if fig:
                    st.subheader("📈 Visualization")
                    st.pyplot(fig)

            except:
                st.write(result)

            # Insights
            st.subheader("💡 Business Insights")
            insights = generate_insights.invoke(result)
            st.write(insights)

    else:
        st.warning("Please enter a query")
