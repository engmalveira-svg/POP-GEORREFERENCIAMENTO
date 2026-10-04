import streamlit as st
import pypdf

st.set_page_config(page_title="Validador de Memorial Descritivo - POP", page_icon="📄", layout="centered")

st.title("📄 Validador de Memorial Descritivo (POP)")
st.write("Eng. Civil Paulo Henrique Malveira Vasconcelos | Sistema de Conferência Automatizada")

uploaded_file = st.file_uploader("📂 Escolha ou arraste o seu Memorial Descritivo em PDF", type=[".pdf"])

if uploaded_file is not None:
    st.info("Analisando o documento, aguarde um instante...")
    
    try:
        leitor = pypdf.PdfReader(uploaded_file)
        texto_total = ""
        for pagina in leitor.pages:
            texto_total += pagina.extract_text() + "\n"
        
        texto_minusculo = texto_total.lower()

        # Regras estruturais exigidas
        passos_padrao = [
            {"termo": "paulo henrique", "nome_amigavel": "1. Cabeçalho (Nome do Profissional)"},
            {"termo": "memorial descritivo", "nome_amigavel": "2. Título Centralizado ('Memorial Descritivo')"},
            {"termo": "matrícula", "nome_amigavel": "3. Dados (Campo 'Matrícula')"},
            {"termo": "proprietário", "nome_amigavel": "3. Dados (Campo 'Proprietário')"},
            {"termo": "perímetro", "nome_amigavel": "3. Dados (Campo 'Perímetro')"},
            {"termo": "azimute", "nome_amigavel": "4. Descrição Técnica (Azimutes/Coordenadas/Confrontantes)"},
            {"termo": "crea", "nome_amigavel": "5. Encerramento (CREA e Assinatura no final)"}
        ]

        ultima_posicao = -1
        ordem_correta = True
        relatorio = []

        for passo in passos_padrao:
            termo = passo["termo"]
            nome = passo["nome_amigavel"]
            
            posicao_atual = texto_minusculo.find(termo)
            
            if posicao_atual == -1:
                relatorio.append(f"❌ ERRO: O item obrigatório **{nome}** não foi encontrado.")
                ordem_correta = False
            else:
                relatorio.append(f"✅ Encontrado: {nome}")
                if posicao_atual < ultima_posicao:
                    relatorio.append(f"⚠️ FORA DE ORDEM: **{nome}** apareceu antes da posição esperada no texto.")
                    ordem_correta = False
                ultima_posicao = posicao_atual

        st.subheader("📊 Relatório de Padronização")
        for r in relatorio:
            st.markdown(r)

        st.markdown("---")
        if ordem_correta:
            st.success("🎉 Perfeito! O memorial está rigorosamente dentro do padrão exigido e na ordem correta.")
        else:
            st.error("⚠️ O memorial apresentou desvios estruturais e precisa de correções.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo PDF: {str(e)}")

# Mais um arquivo necessário para o site funcionar nos bastidores
