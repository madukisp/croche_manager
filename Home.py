import streamlit as st

st.set_page_config(
    page_title="🧶 Crochê Manager",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🪡 Crochê Manager")
st.subheader("Seu gerenciador pessoal de projetos de crochê")

st.markdown("""
Bem-vinda ao **Crochê Manager**, o aplicativo para acompanhar tudo o que você cria à mão:
- 🧶 Registre seus **projetos de crochê**
- 🪡 Gerencie suas **agulhas**
- 🧵 Organize suas **linhas e materiais**
- 📔 Guarde suas **receitas e inspirações**

Use o menu lateral para navegar entre as seções.
""")

st.divider()

st.info("Dica: você pode começar cadastrando suas linhas ou agulhas antes de criar um projeto 🧶")
