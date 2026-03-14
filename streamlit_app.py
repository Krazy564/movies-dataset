import streamlit as st
import pandas as pd 
import plotly.express as px

fil = "data/budget_fil.xlsx"


def main_st(fil):

    st.header("Budget app", divider="red")


    df = pd.read_excel(fil, index_col=0)

    kolonner = df.columns[1:-1]

    df["Total"] = df[kolonner].sum(axis=1)

    st.session_state.poster = st.data_editor(df, num_rows="dynamic")

    total_måneder = df.columns[1:]

    df_totaler = df[total_måneder].sum(axis=0)

    df_totaler = pd.DataFrame([df_totaler], index=["Total pr. måned"])

    st.subheader("Total pr. måned", divider="red")
    st.dataframe(df_totaler)

    if st.button("Gem ændringer"):
        st.session_state.poster.to_excel("data/budget_fil.xlsx")
        st.rerun()
    
    
    plot_df = (
        df_totaler.T
        .reset_index()
        .rename(columns={"index": "Måned", 0: "Total"})
    )

    myplot = px.bar(plot_df, x="Måned", y="Total pr. måned", color="Måned", text_auto="True")

    st.plotly_chart(myplot)


def login_gate():
    st.set_page_config(layout="wide")
    st.title("Login")

    # Session init
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Adgangskode", type="password")
            submit = st.form_submit_button("Log ind")
        if submit:
            if password == st.secrets.get("LOGIN_PASSWORD", ""):
                st.session_state.authenticated = True
                st.session_state.login_user = "John"  # evt. sæt navn her
                st.success("Login ok")
                st.rerun()
            else:
                st.error("Forkert adgangskode.")
    else:
        # Topbar med logout
        cols = st.columns([1, 6, 1])
        with cols[2]:
            if st.button("Log ud"):
                for key in ("authenticated", "login_user"):
                    st.session_state.pop(key, None)
                st.rerun()
        # Kald dit hovedscript
        fil = "data/budget_fil.xlsx"
        main_st(fil)

if __name__ == "__main__":
    login_gate()
