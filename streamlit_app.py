import streamlit as st
import pandas as pd 
import plotly.express as px

fil = "data/budget_fil.xlsx"


def main_st(fil):

    df = pd.read_excel(fil, index_col=0)

    kolonner = df.columns[1:-1]

    df["Total"] = df[kolonner].sum(axis=1)

    st.subheader("Udgifter", divider="red")

    with st.expander("Budget tabel"):
        st.session_state.poster = st.data_editor(df, num_rows="dynamic")

    total_måneder = df.columns[1:]

    df_totaler = df[total_måneder].sum(axis=0)

    df_totaler = pd.DataFrame([df_totaler], index=["Total pr. måned"])

    #st.subheader("Total pr. måned", divider="red")
    st.dataframe(df_totaler)

    st.subheader("Indtægter", divider="red")
    indtægter = pd.read_excel("data/indtægter_fil.xlsx", index_col=0)
    indtægter["Total"] = indtægter[indtægter.columns[0:-1]].sum(axis=1)
    
    st.session_state.indtægter = st.data_editor(indtægter)

    st.subheader("Difference", divider="red")
    
    
    out_values = indtægter.to_numpy() - df_totaler.to_numpy()
    diff = pd.DataFrame(out_values, index=["Difference"], columns=df_totaler.columns)
    

    st.dataframe(diff)

    if st.button("Gem ændringer"):
        st.session_state.poster.to_excel("data/budget_fil.xlsx")
        st.session_state.indtægter.to_excel("data/indtægter_fil.xlsx")
        st.rerun()
    
    
    col1, col2 = st.columns([1,1])

    df_totaler["Indtægt"] = indtægter["Total"]

    

    plot_df = (
        df_totaler.T
        .reset_index()
        .rename(columns={"index": "Måned", 0: "Total", 0:"Indtægt"})
    )
    
    plot_df.loc[13] = {
        "Måned":"Indtægt",
        "Total pr. måned":indtægter["Total"]
    }


    myplot = px.bar(plot_df, x="Måned", y="Total pr. måned", color="Måned", text_auto="True", title="Udgifter")

    plot_df_diff = (
        diff.T
        .reset_index()
        .rename(columns={"index": "Måned", 0: "Total"})
    )


    myplot_diff = px.bar(plot_df_diff, x="Måned", y="Difference", color="Måned", text_auto="True", title="Difference")

    col1.plotly_chart(myplot)
    col2.plotly_chart(myplot_diff)



def login_gate():
    st.set_page_config(layout="wide")
    st.title("Budget app")

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
