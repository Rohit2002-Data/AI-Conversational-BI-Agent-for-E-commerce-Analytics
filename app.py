import streamlit as st
import pandas as pd
from io import StringIO
from db_setup import load_database
from agent import create_agent
from visualization import generate_chart

st.set_page_config(page_title="AI BI Agent", layout="wide")

st.title("🚀 AI Conversational BI Agent")

load_database()
agent_executor = create_agent()

query = st.text_input("Ask your business question:")

if query:
    with st.spinner("Thinking..."):
        response = agent_executor.invoke({"input": query})

    st.subheader("Raw Output")
    st.write(response["output"])

    try:
        df = pd.read_csv(StringIO(response["output"]))
        st.subheader("Table")
        st.dataframe(df)

        fig = generate_chart(df)
        if fig:
            st.subheader("Visualization")
            st.pyplot(fig)

    except:
        st.warning("Could not generate chart")
