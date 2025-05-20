import streamlit as st
import google.generativeai as genai
import random
import os
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import lxml # Necessário para o parser lxml do BeautifulSoup

# --- Configuração da Página (no início) ---
st.set_page_config(page_title="CHABAD - Torá com IA", layout="wide", initial_sidebar_state="expanded")

# --- CARREGAR A API KEY DOS SEGREDOS DO STREAMLIT ---
GOOGLE_API_KEY = None
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("ERRO: Chave API 'GOOGLE_API_KEY' não encontrada nos Segredos do Streamlit.")
    st.info("Por favor, adicione sua GOOGLE_API_KEY aos Segredos do seu app no Streamlit Cloud (em Settings > Secrets).")
    st.stop()
except FileNotFoundError:
    st.error("ERRO: Arquivo de Segredos do Streamlit (secrets.toml) não encontrado.")
    st.info("Este erro é mais comum em desenvolvimento local. No Streamlit Cloud, configure os segredos na interface.")
    st.stop()

if not GOOGLE_API_KEY:
    st.error("ERRO: A GOOGLE_API_KEY não pôde ser carregada ou está vazia.")
    st.info("Verifique a configuração dos seus Segredos no Streamlit Cloud.")
    st.stop()

# --- CONFIGURAR A BIBLIOTECA GEMINI ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e_config_api:
    st.sidebar.error(f"ERRO ao configurar a API Key do Gemini: {e_config_api}")
    st.stop()

# --- INICIALIZAR O MODELO DE IA PRINCIPAL ---
modelo_ia_geral = None
try:
    modelo_ia_geral = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e_carregar_modelo:
    st.sidebar.error(f"ERRO ao carregar o modelo Gemini: {e_carregar_modelo}")
    st.caption("Verifique se o nome do modelo está correto e se sua API key tem permissão para usá-lo.")
    st.stop()

# --- TÍTULO E SUBTÍTULO DO SEU APP ---
st.title("🌟 CHABAD - Torá com IA 🌟")
st.subheader("Seu Assistente Interativo para Estudo da Torá e Judaísmo")

# --- DEFINIÇÕES DAS FUNÇÕES ---

lista_de_pensamentos_chabad = [
    "A verdadeira sabedoria (Chochmá) é a capacidade de ver a Divindade em tudo. A compreensão (Biná) é desenvolver essa percepção. O conhecimento (Daat) é conectar-se profundamente com ela.",
    "Cada mitzvá que cumprimos é como acender uma vela na escuridão, revelando a presença de D'us e aproximando a redenção.",
    "O estudo do Chassidut nos dá as 'ferramentas intelectuais' para refinar nossas emoções e servir a D'us com alegria e um coração pleno.",
    "A missão da nossa geração, como ensinada pelo Rebe de Lubavitch, é preparar o mundo para a chegada de Mashiach através de atos de bondade e do estudo da Torá em todos os seus níveis.",
    "Não subestime o poder de uma única boa ação, uma única boa palavra ou um único bom pensamento. Cada um tem o potencial de transformar o mundo."
]

nomes_dos_rebes_chabad_lista = [
    "o Alter Rebe (Rabi Shneur Zalman de Liadi)",
    "o Mitteler Rebe (Rabi DovBer de Lubavitch)",
    "o Tzemach Tzedek (Rabi Menachem Mendel Schneersohn, o terceiro Rebe)",
    "o Rebe Maharash (Rabi Shmuel Schneersohn de Lubavitch)",
    "o Rebe Rashab (Rabi Sholom DovBer Schneersohn de Lubavitch)",
    "o Rebe Rayatz (Rabi Yosef Yitzchak Schneersohn de Lubavitch)",
    "o Rebe de Lubavitch (Rabi Menachem Mendel Schneerson)"
]

def responder_como_sabio_st(nome_sabio, pergunta_usuario):
    prompt_completo = f"Por favor, responda à seguinte pergunta como se você fosse o {nome_sabio}, utilizando a sua conhecida lógica, sabedoria e os ensinamentos judaicos que lhe são característicos. A pergunta é: \"{pergunta_usuario}\""
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta = modelo_ia_geral.generate_content(prompt_completo)
        return resposta.text
    except Exception as e:
        return f"Ocorreu um erro ao consultar o {nome_sabio}: {e}"

def explicar_conceito_idade_st(conceito_a_explicar, idade_do_publico_str):
    try:
        idade_num = int(idade_do_publico_str)
        if idade_num <= 0: return "A idade deve ser um número positivo."
    except ValueError:
        return "A idade precisa ser um número."
    prompt_detalhado = f"Por favor, explique o conceito judaico de '{conceito_a_explicar}' de maneira simples e clara, adaptada para alguém com {idade_num} anos de idade. Utilize linguagem, exemplos e analogias apropriadas para essa faixa etária."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta_modelo = modelo_ia_geral.generate_content(prompt_detalhado)
        return resposta_modelo.text
    except Exception as e:
        return f"Desculpe, ocorreu um erro ao tentar explicar '{conceito_a_explicar}' para {idade_num} anos: {e}"

def buscar_salmo_formatado_st(numero_do_salmo_str, lista_de_formatos):
    try:
        num_salmo = int(numero_do_salmo_str)
        if not 1 <= num_salmo <= 150: return "Número do Salmo inválido (1-150)."
    except ValueError:
        return "Por favor, digite um número válido para o Salmo."
    if not lista_de_formatos: return "Escolha pelo menos um formato."
    prompt_para_ia = f"Preciso do Salmo (Tehilim) número {num_salmo}.\nPor favor, apresente-o nos seguintes formatos: {', '.join(lista_de_formatos)}.\n\nPara cada formato, siga estas diretrizes se possível:\n- 'hebraico': Texto em hebraico, com nikud (vogais).\n- 'português': Tradução para o português.\n- 'transliterado': Transliteração do hebraico para caracteres latinos, fácil de ler para quem fala português.\n- 'ídiche': Texto do Salmo em Ídiche (em caracteres hebraicos ou transliterado).\n\nSe algum formato não estiver disponível ou a precisão não puder ser garantida, por favor, mencione.\nOrganize a resposta de forma clara, separando cada formato."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta_modelo = modelo_ia_geral.generate_content(prompt_para_ia)
        return resposta_modelo.text
    except Exception as e:
        return f"Desculpe, ocorreu um erro ao tentar buscar o Salmo {num_salmo}: {e}"

def buscar_informacoes_festa_st(nome_da_festa):
    info_concisa_festa, info_detalhada_festa = None, None
    prompt_conciso_festa = f"Por favor, forneça uma descrição concisa da festa judaica de '{nome_da_festa}'. Inclua seu principal significado e, de forma geral, quando ela é celebrada no calendário judaico."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado.", None
        resposta_concisa_modelo = modelo_ia_geral.generate_content(prompt_conciso_festa)
        info_concisa_festa = resposta_concisa_modelo.text
    except Exception as e:
        info_concisa_festa = f"Não consegui encontrar informações concisas sobre '{nome_da_festa}': {e}"

    if info_concisa_festa and not "Não consegui encontrar" in info_concisa_festa:
        prompt_detalhado_festa = f"Considerando a festa judaica de '{nome_da_festa}', por favor, elabore com mais detalhes.\nDescreva as principais mitzvot e costumes associados.\nQuais são as proibições importantes (halachot sobre trabalho, alimentação etc.)?\nQual é o significado espiritual ou histórico mais profundo?"
        try:
            if not modelo_ia_geral: return info_concisa_festa, "ERRO INTERNO: Modelo de IA não carregado."
            resposta_detalhada_modelo = modelo_ia_geral.generate_content(prompt_detalhado_festa)
            info_detalhada_festa = resposta_detalhada_modelo.text
        except Exception as e:
            info_detalhada_festa = f"Não consegui encontrar informações detalhadas sobre '{nome_da_festa}': {e}"
    elif not info_concisa_festa:
        info_detalhada_festa = "Busca inicial falhou."
    return info_concisa_festa, info_detalhada_festa

def gerar_resposta_inicial_st(pergunta_usuario_original):
    prompt_curto = f"Forneça uma resposta inicial concisa e direta para: \"{pergunta_usuario_original}\""
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta = modelo_ia_geral.generate_content(prompt_curto)
        return resposta.text
    except Exception as e:
        return f"Erro na resposta inicial: {e}"

def gerar_resposta_detalhada_st(pergunta_original, instrucao_detalhe, resposta_curta_opcional=None):
    prompt_detalhado = ""
    if instrucao_detalhe == "aprofundar_resposta_anterior" and resposta_curta_opcional:
        prompt_detalhado = f"Sobre a pergunta \"{pergunta_original}\", e considerando a resposta inicial \"{resposta_curta_opcional}\".\nPor favor, aprofunde essa linha de pensamento com mais detalhes, exemplos ou fontes."
    elif instrucao_detalhe == "detalhar_pergunta_original":
        prompt_detalhado = f"Sobre a pergunta original: \"{pergunta_original}\".\nPor favor, forneça uma resposta completa e detalhada desde o início, explorando diferentes facetas, mencionando fontes ou conceitos relevantes e oferecendo uma compreensão abrangente."
    else:
        return "Instrução de detalhamento não reconhecida."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta = modelo_ia_geral.generate_content(prompt_detalhado)
        return resposta.text
    except Exception as e:
        return f"Erro ao gerar resposta detalhada: {e}"

def encontrar_conexoes_judaicas_st(item1, item2):
    prompt_para_ia = f"Considere os seguintes dois elementos do pensamento ou da vida judaica:\nElemento 1: \"{item1}\"\nElemento 2: \"{item2}\"\n\nPor favor, explore e explique possíveis conexões, paralelos, contrastes significativos ou lições que podemos aprender ao relacionar esses dois elementos.\nBaseie sua resposta em fontes, conceitos e na sabedoria judaica. Seja criativo, mas mantenha a profundidade e a autenticidade."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta_ia = modelo_ia_geral.generate_content(prompt_para_ia)
        return resposta_ia.text
    except Exception as e:
        return f"Desculpe, ocorreu um erro ao tentar encontrar conexões: {e}"

def analisar_versiculo_pardes_st(referencia_versiculo):
    prompt_para_ia_pardes = f"Por favor, analise o seguinte versículo da Torá: \"{referencia_versiculo}\".\nApresente uma explicação concisa para cada um dos quatro níveis de interpretação do Pardes, se aplicável e possível:\n1.  Pshat (פשט): Qual é o significado literal, simples e direto do texto?\n2.  Remez (רמז): Existem alusões, dicas, ou significados implícitos? (Ex: gematria, acrônimos, ou paralelos com outros versículos).\n3.  Drash (דרש): Qual é o significado homilético ou interpretativo? (Baseie-se em ensinamentos do Midrash, Talmud ou dos Sábios).\n4.  Sod (סוד): Qual é o significado secreto, místico ou cabalístico? (Relacione com conceitos do Zohar, Arizal, ou Chassidut).\n\nPara cada nível, seja claro e informativo. Se um nível for muito complexo para uma breve explicação, indique isso."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta_modelo_pardes = modelo_ia_geral.generate_content(prompt_para_ia_pardes)
        return resposta_modelo_pardes.text
    except Exception as e_pardes:
        return f"Desculpe, ocorreu um erro ao tentar a análise Pardes: {e_pardes}"

def buscar_historia_ou_ensinamento_rebe_st(nome_rebe_consulta):
    rebe_para_prompt = nome_rebe_consulta
    if nome_rebe_consulta.lower() == "aleatorio":
        rebe_para_prompt = random.choice(nomes_dos_rebes_chabad_lista)
        st.write(f"(Você pediu um Rebe aleatório. Foi escolhido: {rebe_para_prompt})")
    prompt_detalhado_rebe = f"Por favor, compartilhe um ensinamento central e inspirador OU uma história curta e significativa sobre {rebe_para_prompt}.\nSe possível, inclua uma nota muito breve sobre quem foi este Rebe e o período de sua liderança.\nO objetivo é que a resposta seja edificante e transmita a essência do seu legado e sabedoria dentro do movimento Chabad-Lubavitch.\nApresente o texto de forma clara."
    try:
        if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não carregado."
        resposta_modelo_rebe = modelo_ia_geral.generate_content(prompt_detalhado_rebe)
        return resposta_modelo_rebe.text
    except Exception as e_rebe_consulta:
        return f"Desculpe, ocorreu um erro ao buscar o ensinamento ou história: {e_rebe_consulta}"

def apresentar_dica_judaica_do_dia_st():
    tipo_de_dica = random.choice(["halacha", "mitzva"])
    prompt_para_ia_dica, titulo_dica = "", ""
    if tipo_de_dica == "halacha":
        prompt_para_ia_dica = "Por favor, compartilhe uma Halachá (lei judaica) prática e concisa, relevante para o dia a dia. Inclua uma breve explicação de sua importância ou como aplicá-la. Apresente de forma clara e direta."
        titulo_dica = "💡 Halachá do Dia 💡"
    else:
        prompt_para_ia_dica = "Por favor, sugira uma Mitzvá (mandamento ou boa ação) na qual uma pessoa poderia focar hoje ou nesta semana. Inclua uma breve explicação do significado desta Mitzvá e uma sugestão prática de como realizá-la. Apresente de forma inspiradora."
        titulo_dica = "✨ Mitzvá para Inspirar ✨"
    st.subheader(titulo_dica)
    try:
        if not modelo_ia_geral:
            st.error("ERRO INTERNO: Modelo de IA não carregado.")
            return
        with st.spinner("Buscando uma inspiração para você..."):
            resposta_modelo_dica = modelo_ia_geral.generate_content(prompt_para_ia_dica)
        st.markdown(resposta_modelo_dica.text)
    except Exception as e_dica:
        st.error(f"Desculpe, não foi possível buscar a dica de hoje: {e_dica}")
    st.markdown("---")

def conduzir_estudo_dirigido_st():
    st.subheader("🌟 Modo Estudo Dirigido 🌟")
    if 'tipo_estudo' not in st.session_state: st.session_state.tipo_estudo = None
    if 'nome_parasha_tema' not in st.session_state: st.session_state.nome_parasha_tema = ""
    if 'etapa_estudo' not in st.session_state: st.session_state.etapa_estudo = 0

    if st.session_state.etapa_estudo == 0:
        tipo_estudo_escolha = st.radio("Você gostaria de estudar:", ("Uma Parashá da Semana", "Um Tema Geral do Judaísmo"), key="tipo_estudo_radio")
        if tipo_estudo_escolha == "Uma Parashá da Semana":
            st.session_state.tipo_estudo = "parasha"
            st.session_state.nome_parasha_tema = st.text_input("Qual Parashá você gostaria de estudar?", key="parasha_nome_input")
        elif tipo_estudo_escolha == "Um Tema Geral do Judaísmo":
            st.session_state.tipo_estudo = "tema"
            st.session_state.nome_parasha_tema = st.text_input("Qual tema geral do Judaísmo você gostaria de explorar?", key="tema_nome_input")
        
        if st.button("Iniciar Estudo", key="btn_iniciar_estudo_dirigido"):
            if st.session_state.nome_parasha_tema:
                st.session_state.etapa_estudo = 1
                st.rerun() # Reinicia o script para avançar para a próxima etapa
            else:
                st.warning("Por favor, informe a Parashá ou o Tema.")
    
    elif st.session_state.etapa_estudo == 1:
        prompt, titulo_etapa = "", ""
        if st.session_state.tipo_estudo == "parasha":
            prompt = f"Forneça um resumo conciso dos principais eventos e temas da Parashá '{st.session_state.nome_parasha_tema}'."
            titulo_etapa = f"Resumo da Parashá: {st.session_state.nome_parasha_tema}"
        elif st.session_state.tipo_estudo == "tema":
            prompt = f"Forneça uma introdução clara e concisa sobre o tema '{st.session_state.nome_parasha_tema}' no Judaísmo, explicando sua importância."
            titulo_etapa = f"Introdução ao Tema: {st.session_state.nome_parasha_tema}"
        
        st.markdown(f"### {titulo_etapa}")
        if prompt:
            with st.spinner("Buscando informações..."):
                try:
                    if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                    resposta = modelo_ia_geral.generate_content(prompt)
                    st.markdown(resposta.text)
                    st.session_state.etapa_estudo = 2 # Avança para a próxima etapa
                except Exception as e: st.error(f"Erro: {e}"); st.session_state.etapa_estudo = 0
        if st.button("Próxima Etapa do Estudo", key="btn_etapa2_estudo"): st.rerun()
        if st.button("Encerrar Estudo Dirigido", key="btn_encerrar_estudo1"): st.session_state.etapa_estudo = 0; st.session_state.tipo_estudo=None; st.session_state.nome_parasha_tema=""; st.rerun()

    elif st.session_state.etapa_estudo == 2:
        prompt, titulo_etapa = "", ""
        if st.session_state.tipo_estudo == "parasha":
            prompt = f"Qual é um versículo chave ou muito significativo da Parashá '{st.session_state.nome_parasha_tema}' e por quê? Apresente o versículo e uma breve explicação."
            titulo_etapa = "Versículo Chave e Significado"
        elif st.session_state.tipo_estudo == "tema":
            prompt = f"Quais são alguns conceitos chave, fontes principais (Torá, Talmud, Sábios) ou aspectos importantes relacionados ao tema '{st.session_state.nome_parasha_tema}' no Judaísmo?"
            titulo_etapa = "Conceitos Chave e Fontes"

        st.markdown(f"### {titulo_etapa}")
        if prompt:
            with st.spinner("Buscando mais informações..."):
                try:
                    if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                    resposta = modelo_ia_geral.generate_content(prompt)
                    st.markdown(resposta.text)
                    st.session_state.etapa_estudo = 3
                except Exception as e: st.error(f"Erro: {e}"); st.session_state.etapa_estudo = 0
        if st.button("Próxima Etapa do Estudo", key="btn_etapa3_estudo"): st.rerun()
        if st.button("Encerrar Estudo Dirigido", key="btn_encerrar_estudo2"): st.session_state.etapa_estudo = 0; st.session_state.tipo_estudo=None; st.session_state.nome_parasha_tema=""; st.rerun()

    elif st.session_state.etapa_estudo == 3:
        prompt, titulo_etapa = "", ""
        if st.session_state.tipo_estudo == "parasha":
            sabio_parasha = "Rashi" # Poderia ser input
            prompt = f"Sobre a Parashá '{st.session_state.nome_parasha_tema}', qual seria um comentário ou insight importante de {sabio_parasha} sobre um dos temas ou versículos desta Parashá?"
            titulo_etapa = f"Comentário de {sabio_parasha}"
        elif st.session_state.tipo_estudo == "tema":
            prompt = f"Como o entendimento do tema '{st.session_state.nome_parasha_tema}' pode impactar a vida diária de um judeu ou que tipo de reflexão ele nos convida a fazer?"
            titulo_etapa = "Aplicação ou Reflexão"

        st.markdown(f"### {titulo_etapa}")
        if prompt:
            with st.spinner("Buscando sabedoria adicional..."):
                try:
                    if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                    resposta = modelo_ia_geral.generate_content(prompt)
                    st.markdown(resposta.text)
                    st.session_state.etapa_estudo = 4 # Ou 0 para encerrar
                except Exception as e: st.error(f"Erro: {e}"); st.session_state.etapa_estudo = 0
        if st.session_state.tipo_estudo == "parasha" and st.session_state.etapa_estudo == 4: # Adicionar lição prática para parasha
             prompt_licao = f"Qual é uma lição prática ou mensagem para nossos dias que podemos extrair da Parashá '{st.session_state.nome_parasha_tema}'?"
             titulo_etapa_licao = "Lição Para Nossos Dias"
             st.markdown(f"### {titulo_etapa_licao}")
             with st.spinner("Extraindo lição prática..."):
                try:
                    if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                    resposta_licao = modelo_ia_geral.generate_content(prompt_licao)
                    st.markdown(resposta_licao.text)
                except Exception as e: st.error(f"Erro: {e}")
        
        st.info("Fim do Estudo Dirigido sobre este tópico.")
        if st.button("Iniciar Novo Estudo Dirigido", key="btn_novo_estudo_dirigido"):
            st.session_state.etapa_estudo = 0
            st.session_state.tipo_estudo = None
            st.session_state.nome_parasha_tema = ""
            st.rerun()
    st.markdown("---")


def interagir_com_chavruta_st():
    st.subheader("🗣️ Chavruta Interativa com Sábio")

    if 'chavruta_sabio' not in st.session_state: st.session_state.chavruta_sabio = ""
    if 'chavruta_tema' not in st.session_state: st.session_state.chavruta_tema = ""
    if 'chavruta_estilo' not in st.session_state: st.session_state.chavruta_estilo = ""
    if 'chavruta_historico' not in st.session_state: st.session_state.chavruta_historico = []
    if 'chavruta_iniciada' not in st.session_state: st.session_state.chavruta_iniciada = False

    if not st.session_state.chavruta_iniciada:
        st.session_state.chavruta_sabio = st.text_input("Com qual Sábio você gostaria de estudar hoje?", value=st.session_state.chavruta_sabio, key="chavruta_sabio_nome")
        st.session_state.chavruta_tema = st.text_input(f"Qual tema você gostaria de discutir com {st.session_state.chavruta_sabio if st.session_state.chavruta_sabio else 'o Sábio'}?", value=st.session_state.chavruta_tema, key="chavruta_tema_estudo")
        estilo_opcoes = ["moderna", "tradicional"]
        st.session_state.chavruta_estilo = st.radio(f"Prefere que {st.session_state.chavruta_sabio if st.session_state.chavruta_sabio else 'o Sábio'} use linguagem 'moderna' ou 'tradicional'?", estilo_opcoes, index=estilo_opcoes.index(st.session_state.chavruta_estilo) if st.session_state.chavruta_estilo in estilo_opcoes else 0, key="chavruta_estilo_ling")

        if st.button("Iniciar Chavruta", key="btn_iniciar_chavruta"):
            if st.session_state.chavruta_sabio and st.session_state.chavruta_tema and st.session_state.chavruta_estilo:
                st.session_state.chavruta_iniciada = True
                instrucao_linguagem = "Adapte sua linguagem para ser mais moderna, clara e acessível para um estudante de hoje."
                if st.session_state.chavruta_estilo == "tradicional":
                    instrucao_linguagem = "Use uma linguagem que reflita a erudição e o estilo da sua época, mantendo a profundidade."
                
                st.session_state.chavruta_historico = [
                    (f"Você é o Sábio {st.session_state.chavruta_sabio}, um mestre da Torá. "
                     f"Eu sou seu parceiro de estudo (Chavruta). Estamos estudando: '{st.session_state.chavruta_tema}'. "
                     f"Mantenha sua persona. {instrucao_linguagem} "
                     f"Por favor, comece me saudando e perguntando sobre o que especificamente em '{st.session_state.chavruta_tema}' eu gostaria de começar.")
                ]
                # Primeira fala da IA para iniciar
                with st.spinner("Iniciando a Chavruta..."):
                    try:
                        if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                        # Gerar a primeira mensagem da IA com base na instrução inicial
                        resposta_inicial_sabio = modelo_ia_geral.generate_content(st.session_state.chavruta_historico[0] + f"\nSua saudação e pergunta inicial como {st.session_state.chavruta_sabio}:")
                        st.session_state.chavruta_historico.append(f"Sua resposta como {st.session_state.chavruta_sabio}: {resposta_inicial_sabio.text}")
                        st.rerun() # Para atualizar a interface e mostrar a fala da IA e o campo de input do usuário
                    except Exception as e:
                        st.error(f"Erro ao iniciar Chavruta: {e}")
                        st.session_state.chavruta_iniciada = False # Reseta
            else:
                st.warning("Por favor, preencha todos os campos para iniciar a Chavruta.")
    
    if st.session_state.chavruta_iniciada:
        st.markdown(f"**Estudando com: {st.session_state.chavruta_sabio} | Tema: {st.session_state.chavruta_tema} | Linguagem: {st.session_state.chavruta_estilo}**")
        
        # Exibe o histórico da conversa
        for i, fala in enumerate(st.session_state.chavruta_historico):
            if i == 0 and "Você é o Sábio" in fala : continue # Não mostra a instrução de sistema inicial
            if "Meu parceiro de estudo (eu):" in fala:
                st.text_area("Você:", value=fala.split("Meu parceiro de estudo (eu):",1)[1].strip(), height=50, disabled=True, key=f"hist_user_{i}")
            elif f"Sua resposta como {st.session_state.chavruta_sabio}:" in fala:
                st.text_area(f"{st.session_state.chavruta_sabio}:", value=fala.split(f"Sua resposta como {st.session_state.chavruta_sabio}:",1)[1].strip(), height=100, disabled=True, key=f"hist_model_{i}")
            elif i==0 : # Primeira fala da IA (saudação)
                 st.text_area(f"{st.session_state.chavruta_sabio}:", value=fala.split(f"Sua saudação e pergunta inicial como {st.session_state.chavruta_sabio}:",1)[1].strip() if f"Sua saudação e pergunta inicial como {st.session_state.chavruta_sabio}:" in fala else fala , height=100, disabled=True, key=f"hist_model_init")


        user_input_chavruta = st.text_input("Sua vez de falar/perguntar:", key="chavruta_user_input_field")

        if st.button("Enviar para Chavruta", key="btn_chavruta_send"):
            if user_input_chavruta:
                if user_input_chavruta.lower() in ["sair", "tchau", "parar", "chega"]:
                    st.success(f"{st.session_state.chavruta_sabio}: Que nosso estudo tenha sido para elevação! Shalom.")
                    st.session_state.chavruta_iniciada = False
                    st.session_state.chavruta_historico = [] # Limpa o histórico
                    st.session_state.chavruta_sabio = ""
                    st.session_state.chavruta_tema = ""
                    st.session_state.chavruta_estilo = ""
                    st.rerun()
                else:
                    st.session_state.chavruta_historico.append(f"Meu parceiro de estudo (eu): {user_input_chavruta}")
                    prompt_chavruta_atual = "\n".join(st.session_state.chavruta_historico) + f"\nSua resposta como {st.session_state.chavruta_sabio}:"
                    
                    with st.spinner(f"{st.session_state.chavruta_sabio} está pensando..."):
                        try:
                            if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                            resposta_ia_chavruta = modelo_ia_geral.generate_content(prompt_chavruta_atual)
                            texto_resposta_chavruta = resposta_ia_chavruta.text
                            st.session_state.chavruta_historico.append(f"Sua resposta como {st.session_state.chavruta_sabio}: {texto_resposta_chavruta}")
                            # Limpar o campo de input após enviar não é direto no Streamlit sem truques mais complexos,
                            # então apenas fazemos o rerun para atualizar a tela com a nova resposta.
                            st.rerun() 
                        except Exception as e_chavruta:
                            st.error(f"Erro na Chavruta: {e_chavruta}")
                            # Remove a última fala do usuário do histórico se a geração falhou
                            if st.session_state.chavruta_historico and "Meu parceiro de estudo (eu):" in st.session_state.chavruta_historico[-1]:
                                st.session_state.chavruta_historico.pop()
            else:
                st.warning("Digite algo para continuar a Chavruta.")
        
        if st.button("Encerrar Chavruta", key="btn_chavruta_encerrar_urgente"):
            st.success(f"{st.session_state.chavruta_sabio}: Encerrando nossa sessão. Shalom!")
            st.session_state.chavruta_iniciada = False
            st.session_state.chavruta_historico = []
            st.session_state.chavruta_sabio = ""
            st.session_state.chavruta_tema = ""
            st.session_state.chavruta_estilo = ""
            st.rerun()
    st.markdown("---")


def mensagem_final_st():
    st.subheader("📜 Sobre o CHABAD - Torá com IA")
    st.markdown("""
    Parabéns! Você explorou o protótipo do 'CHABAD - Torá com IA'.
    Este ambiente demonstrou o potencial de usar a Inteligência Artificial para:
    - Aprofundar o estudo da Torá em seus múltiplos níveis (Pardes).
    - Conectar-se com a sabedoria dos Sábios e Rebes de Chabad.
    - Tornar o aprendizado judaico mais interativo, personalizado e acessível.
    - Explorar textos sagrados e fontes específicas de forma dinâmica.

    **Próximos Horizontes e Potencial para o Chabad:**
    Este protótipo é uma base sólida. Com o envolvimento do Chabad, o 'Torá com IA' pode evoluir para:
    1.  Um Aplicativo Dedicado: Com interface gráfica amigável.
    2.  Integração de Conteúdo Vasto: Utilizar a imensa biblioteca do Chabad.org e publicações Chabad.
    3.  Personalização Avançada: Perfis de usuário, acompanhamento de estudo.
    4.  Ferramentas de Estudo Comunitário.
    5.  Suporte Multilíngue Aprimorado.

    Que este projeto traga muita luz e aprendizado, e que possamos usar a tecnologia para difundir a Torá e apressar a vinda de Mashiach!
    """)
    st.markdown("---")

# --- LÓGICA DA INTERFACE DO USUÁRIO (MENU E FUNCIONALIDADES) ---
st.sidebar.title("Ferramentas de Estudo 📖")
opcoes_do_menu_lista_completa = [
    "--- Escolha uma Ferramenta ---",
    "Pensamento de Chassidut para o Dia",        # Célula 11
    "Consultar um Sábio",                       # Célula 8 (interativa)
    "Chavruta Interativa com Sábio",            # Célula 10 (com estilo)
    "Explicar Conceito Judaico por Idade",      # Célula 14 (interativa)
    "Leitura de Salmos (Tehilim)",              # Célula 16
    "Explorar Festas Judaicas",                 # Célula 12
    "Pergunta com Opção de Aprofundamento",     # Célula 15 (aprimorada)
    "Análise Pardes de um Versículo",           # Célula 27
    "Sabedoria dos Rebes de Chabad",            # Célula 28
    "Halachá/Mitzvá do Dia",                    # Célula 29
    "Conexões da Sabedoria Judaica",            # Célula 25
    "Estudo Dirigido (Parashá/Tema)",           # Célula 26
    # "Explorar Conteúdo de Página Web (Upload HTML)", # Células 18-20, 24 - Requer st.file_uploader
    # "Explorar Conteúdo de Livro PDF (Upload PDF)",   # Células 21-22, 24 - Requer st.file_uploader
    "Sobre o CHABAD - Torá com IA"              # Célula de Encerramento
]
opcao_menu_st = st.sidebar.selectbox(
    "O que você gostaria de fazer hoje?",
    opcoes_do_menu_lista_completa,
    key="menu_principal_selectbox"
)

# Lógica para cada opção do menu
if opcao_menu_st == "--- Escolha uma Ferramenta ---":
    st.info("⬅️ Por favor, escolha uma ferramenta de estudo na barra lateral para começar!")
    # st.balloons() # Balões só na página inicial

elif opcao_menu_st == "Pensamento de Chassidut para o Dia":
    st.subheader("Pensamento de Chassidut para o Dia")
    if lista_de_pensamentos_chabad:
        if st.button("Gerar Novo Pensamento", key="btn_gerar_pensamento"):
            pensamento_selecionado = random.choice(lista_de_pensamentos_chabad)
            st.markdown(f"## > *{pensamento_selecionado}*")
        else:
            st.write("Clique no botão para um pensamento inspirador.")
    else:
        st.write("Nenhum pensamento disponível no momento.")
    st.markdown("---")

elif opcao_menu_st == "Consultar um Sábio":
    st.subheader("Consultar um Sábio")
    if 'sabio_cs_nome' not in st.session_state: st.session_state.sabio_cs_nome = ""
    if 'sabio_cs_pergunta' not in st.session_state: st.session_state.sabio_cs_pergunta = ""

    nome_sabio_cs = st.text_input("Nome do Sábio:", value=st.session_state.sabio_cs_nome, key="cs_sabio_nome")
    pergunta_cs = st.text_area(f"Sua pergunta para {nome_sabio_cs if nome_sabio_cs else 'o Sábio'}:", value=st.session_state.sabio_cs_pergunta, key="cs_sabio_pergunta", height=100)

    if st.button("Enviar Consulta", key="cs_btn_enviar"):
        st.session_state.sabio_cs_nome = nome_sabio_cs
        st.session_state.sabio_cs_pergunta = pergunta_cs
        if nome_sabio_cs and pergunta_cs:
            with st.spinner(f"Consultando {nome_sabio_cs}..."):
                resposta = responder_como_sabio_st(nome_sabio_cs, pergunta_cs)
            st.markdown(f"### Resposta (como {nome_sabio_cs}):")
            st.markdown(resposta)
        else:
            st.warning("Por favor, preencha o nome do Sábio e a pergunta.")
    st.markdown("---")

elif opcao_menu_st == "Chavruta Interativa com Sábio":
    interagir_com_chavruta_st() # Chama a função definida anteriormente

elif opcao_menu_st == "Explicar Conceito Judaico por Idade":
    st.subheader("Explicar Conceito Judaico por Idade")
    if 'conceito_explicar_idade_nome' not in st.session_state: st.session_state.conceito_explicar_idade_nome = ""
    if 'conceito_explicar_idade_num' not in st.session_state: st.session_state.conceito_explicar_idade_num = "7" # Default age

    conceito_ei = st.text_input("Qual conceito judaico você gostaria de entender?", value=st.session_state.conceito_explicar_idade_nome, key="ei_conceito")
    idade_ei_str = st.text_input(f"Para qual idade (número) você gostaria da explicação de '{conceito_ei}'?", value=st.session_state.conceito_explicar_idade_num, key="ei_idade")

    if st.button("Explicar Conceito", key="ei_btn_explicar"):
        st.session_state.conceito_explicar_idade_nome = conceito_ei
        st.session_state.conceito_explicar_idade_num = idade_ei_str
        if conceito_ei and idade_ei_str:
            with st.spinner(f"Preparando explicação de '{conceito_ei}' para {idade_ei_str} anos..."):
                explicacao = explicar_conceito_idade_st(conceito_ei, idade_ei_str)
            st.markdown(explicacao)
        else:
            st.warning("Por favor, forneça o conceito e a idade.")
    st.markdown("---")

elif opcao_menu_st == "Leitura de Salmos (Tehilim)":
    st.subheader("📜 Leitura dos Salmos (Tehilim)")
    if 'salmo_num_input' not in st.session_state: st.session_state.salmo_num_input = "1"
    if 'salmo_formatos_input' not in st.session_state: st.session_state.salmo_formatos_input = "hebraico, português"

    num_salmo_st = st.text_input("Digite o número do Salmo (1-150):", value=st.session_state.salmo_num_input, key="salmo_num")
    formatos_st_str = st.text_input("Formatos (hebraico, português, transliterado, ídiche) - separados por vírgula:", value=st.session_state.salmo_formatos_input, key="salmo_formatos")
    
    if st.button("Ler Salmo", key="btn_ler_salmo"):
        st.session_state.salmo_num_input = num_salmo_st
        st.session_state.salmo_formatos_input = formatos_st_str
        formatos_lista_st = [fmt.strip() for fmt in formatos_st_str.split(',') if fmt.strip()]
        if num_salmo_st and formatos_lista_st:
            with st.spinner(f"Buscando Salmo {num_salmo_st}..."):
                resultado = buscar_salmo_formatado_st(num_salmo_st, formatos_lista_st)
            st.markdown(resultado)
            st.caption("Lembre-se: Para estudo e uso litúrgico, sempre consulte um Sefer Tehilim ou Siddur de confiança.")
        else:
            st.warning("Número do Salmo ou formato não fornecido.")
    st.markdown("---")

elif opcao_menu_st == "Explorar Festas Judaicas":
    st.subheader("🎉 Explorar Festas Judaicas")
    if 'festa_nome_input' not in st.session_state: st.session_state.festa_nome_input = ""

    nome_festa_st = st.text_input("Sobre qual festa judaica você gostaria de aprender?", value=st.session_state.festa_nome_input, key="festa_nome")
    if st.button("Buscar Informações da Festa", key="btn_buscar_festa"):
        st.session_state.festa_nome_input = nome_festa_st
        if nome_festa_st:
            with st.spinner(f"Buscando informações sobre {nome_festa_st}..."):
                conciso_f, detalhado_f = buscar_informacoes_festa_st(nome_festa_st)
            st.markdown(f"### Resumo Conciso de {nome_festa_st}")
            st.markdown(conciso_f)
            st.markdown(f"### Detalhes e Aprofundamento sobre {nome_festa_st}")
            st.markdown(detalhado_f)
        else:
            st.warning("Por favor, digite o nome de uma festa.")
    st.markdown("---")

elif opcao_menu_st == "Pergunta com Opção de Aprofundamento":
    st.subheader("💡 Pergunta com Opção de Aprofundamento")
    if 'pa_pergunta' not in st.session_state: st.session_state.pa_pergunta = ""
    if 'pa_resposta_curta' not in st.session_state: st.session_state.pa_resposta_curta = None
    
    pergunta_pa = st.text_area("Qual é a sua pergunta sobre Judaísmo?", value=st.session_state.pa_pergunta, key="pa_pergunta_area", height=100)

    if st.button("Obter Resposta Inicial", key="btn_pa_inicial"):
        st.session_state.pa_pergunta = pergunta_pa
        st.session_state.pa_resposta_curta = None # Limpa aprofundamento anterior
        if pergunta_pa:
            with st.spinner("Buscando resposta inicial..."):
                st.session_state.pa_resposta_curta = gerar_resposta_inicial_st(pergunta_pa)
            st.markdown("### Resposta Inicial (Sucinta)")
            st.markdown(st.session_state.pa_resposta_curta)
        else:
            st.warning("Por favor, faça uma pergunta.")

    if st.session_state.pa_resposta_curta and not "Erro na resposta inicial" in st.session_state.pa_resposta_curta:
        st.write("---")
        escolha_pa_st = st.radio("O que fazer agora?", 
                                 ("Nada", "Aprofundar esta resposta", "Tentar resposta mais detalhada para pergunta original"), 
                                 key="pa_radio_escolha", horizontal=True)
        if escolha_pa_st == "Aprofundar esta resposta":
            if st.button("Aprofundar Resposta Anterior", key="btn_pa_aprofundar_anterior"):
                with st.spinner("Aprofundando a resposta dada..."):
                    resposta_final_pa = gerar_resposta_detalhada_st(st.session_state.pa_pergunta, "aprofundar_resposta_anterior", st.session_state.pa_resposta_curta)
                st.markdown("### Aprofundamento da Resposta Anterior")
                st.markdown(resposta_final_pa)
        elif escolha_pa_st == "Tentar resposta mais detalhada para pergunta original":
            if st.button("Detalhar Pergunta Original", key="btn_pa_detalhar_original"):
                with st.spinner("Buscando uma resposta mais detalhada para sua pergunta original..."):
                    resposta_final_pa = gerar_resposta_detalhada_st(st.session_state.pa_pergunta, "detalhar_pergunta_original")
                st.markdown("### Resposta Detalhada da Pergunta Original")
                st.markdown(resposta_final_pa)
    st.markdown("---")

elif opcao_menu_st == "Análise Pardes de um Versículo":
    st.subheader("🔍 Análise Pardes de um Versículo da Torá")
    if 'pardes_versiculo_input' not in st.session_state: st.session_state.pardes_versiculo_input = "Gênesis 1:1"
    
    versiculo_pardes_st = st.text_input("Digite a referência do versículo da Torá (ex: Gênesis 1:1):", value=st.session_state.pardes_versiculo_input, key="pardes_versiculo")
    if st.button("Analisar Versículo (Pardes)", key="btn_analisar_pardes"):
        st.session_state.pardes_versiculo_input = versiculo_pardes_st
        if versiculo_pardes_st:
            with st.spinner(f"Analisando '{versiculo_pardes_st}' nos níveis do Pardes..."):
                resultado = analisar_versiculo_pardes_st(versiculo_pardes_st)
            st.markdown(f"### Análise Pardes para: {versiculo_pardes_st}")
            st.markdown(resultado)
            st.caption("Lembre-se: A profundidade do Pardes é vasta. Esta é uma introdução.")
        else:
            st.warning("Por favor, digite a referência de um versículo.")
    st.markdown("---")

elif opcao_menu_st == "Sabedoria dos Rebes de Chabad":
    st.subheader("🌟 Sabedoria dos Rebes de Chabad")
    st.write("De qual Rebe de Chabad você gostaria de ouvir um ensinamento ou história hoje?")
    
    opcoes_rebes_st = ["Escolha um Rebe"] + nomes_dos_rebes_chabad_lista + ["Um Rebe Aleatório"]
    if 'rebe_escolhido_idx' not in st.session_state: st.session_state.rebe_escolhido_idx = 0 # Default para "Escolha um Rebe"

    escolha_rebe_idx_st = st.selectbox("Selecione:", opcoes_rebes_st, index=st.session_state.rebe_escolhido_idx, key="rebe_selectbox")
    
    if st.button("Buscar Ensinamento/História do Rebe", key="btn_buscar_rebe"):
        st.session_state.rebe_escolhido_idx = opcoes_rebes_st.index(escolha_rebe_idx_st) # Salva a escolha
        rebe_para_consulta_st = ""
        if escolha_rebe_idx_st != "Escolha um Rebe":
            if escolha_rebe_idx_st == "Um Rebe Aleatório":
                rebe_para_consulta_st = "aleatorio"
            else:
                rebe_para_consulta_st = escolha_rebe_idx_st
            
            with st.spinner(f"Buscando sabedoria..."):
                resultado = buscar_historia_ou_ensinamento_rebe_st(rebe_para_consulta_st)
            st.markdown("### Um Ensinamento ou História do Rebe")
            st.markdown(resultado)
        else:
            st.warning("Por favor, selecione um Rebe ou a opção aleatória.")
    st.markdown("---")

elif opcao_menu_st == "Halachá/Mitzvá do Dia":
    apresentar_dica_judaica_do_dia_st() # Chama a função que já tem st.subheader e st.markdown

elif opcao_menu_st == "Conexões da Sabedoria Judaica":
    st.subheader("🔗 Conexões da Sabedoria Judaica")
    if 'conexao_item1' not in st.session_state: st.session_state.conexao_item1 = ""
    if 'conexao_item2' not in st.session_state: st.session_state.conexao_item2 = ""

    item1_st = st.text_input("Digite o primeiro elemento/conceito:", value=st.session_state.conexao_item1, key="conexao_item1_input")
    item2_st = st.text_input("Digite o segundo elemento/conceito:", value=st.session_state.conexao_item2, key="conexao_item2_input")

    if st.button("Encontrar Conexões", key="btn_encontrar_conexoes"):
        st.session_state.conexao_item1 = item1_st
        st.session_state.conexao_item2 = item2_st
        if item1_st and item2_st:
            if item1_st.lower() == item2_st.lower():
                st.warning("Tente dois elementos diferentes para uma exploração mais rica.")
            else:
                with st.spinner(f"Buscando conexões entre '{item1_st}' e '{item2_st}'..."):
                    resultado = encontrar_conexoes_judaicas_st(item1_st, item2_st)
                st.markdown("### Explorando as Conexões")
                st.markdown(resultado)
        else:
            st.warning("Por favor, forneça os dois elementos.")
    st.markdown("---")

elif opcao_menu_st == "Estudo Dirigido (Parashá/Tema)":
    conduzir_estudo_dirigido_st() # Chama a função definida

# --- IMPLEMENTAÇÃO DAS FUNCIONALIDADES DE UPLOAD E ANÁLISE DE ARQUIVOS ---
# Estas são mais complexas e precisam de st.file_uploader

elif opcao_menu_st == "Explorar Conteúdo de Página Web (Upload HTML)":
    st.subheader("📄 Explorar Conteúdo de Página Web (Upload HTML)")
    uploaded_html_file = st.file_uploader("Carregue seu arquivo HTML aqui:", type=["html", "htm"], key="html_uploader")
    
    if 'texto_html_processado' not in st.session_state:
        st.session_state.texto_html_processado = None

    if uploaded_html_file is not None:
        if st.button("Processar Arquivo HTML", key="btn_processar_html"):
            with st.spinner("Lendo e processando o arquivo HTML..."):
                try:
                    bytes_data = uploaded_html_file.read()
                    html_content_st = bytes_data.decode('utf-8') # Ou outra codificação se necessário
                    
                    soup_st = BeautifulSoup(html_content_st, 'lxml')
                    textos_extraidos_st = []
                    for paragrafo_st in soup_st.find_all('p'):
                        textos_extraidos_st.append(paragrafo_st.get_text(separator=' ', strip=True))
                    st.session_state.texto_html_processado = "\n".join(textos_extraidos_st)

                    if st.session_state.texto_html_processado.strip():
                        st.success("HTML processado com sucesso! Amostra abaixo.")
                        st.text_area("Amostra do Texto Extraído (Primeiros 1000 caracteres):", value=st.session_state.texto_html_processado[:1000], height=200, disabled=True, key="html_amostra_texto")
                    else:
                        st.warning("Não foi possível extrair texto significativo do HTML.")
                        st.session_state.texto_html_processado = None
                except Exception as e_html_proc:
                    st.error(f"Erro ao processar o HTML: {e_html_proc}")
                    st.session_state.texto_html_processado = None
    
    if st.session_state.texto_html_processado and st.session_state.texto_html_processado.strip():
        st.markdown("---")
        st.write("Agora você pode fazer perguntas sobre este texto HTML:")
        pergunta_html_st = st.text_area("Sua pergunta sobre o conteúdo do HTML:", key="html_pergunta_usuario", height=100)
        if st.button("Perguntar sobre HTML", key="btn_perguntar_html"):
            if pergunta_html_st:
                prompt_html_qa = f"""Baseando-se EXCLUSIVAMENTE no seguinte texto extraído de um arquivo HTML:
TEXTO:
\"\"\"
{st.session_state.texto_html_processado[:30000]}
\"\"\"
Responda à pergunta: "{pergunta_html_st}"
Se a resposta não estiver no texto, indique isso.
RESPOSTA:"""
                with st.spinner("Analisando o texto HTML para responder..."):
                    try:
                        if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                        resposta_html_qa = modelo_ia_geral.generate_content(prompt_html_qa)
                        st.markdown("### Resposta (Baseada no HTML):")
                        st.markdown(resposta_html_qa.text)
                    except Exception as e_html_qa:
                        st.error(f"Erro ao responder sobre o HTML: {e_html_qa}")
            else:
                st.warning("Por favor, digite uma pergunta.")
    st.markdown("---")


elif opcao_menu_st == "Explorar Conteúdo de Livro PDF (Upload PDF)":
    st.subheader("📚 Explorar Conteúdo de Livro PDF (Upload PDF)")
    uploaded_pdf_file = st.file_uploader("Carregue seu arquivo PDF aqui:", type="pdf", key="pdf_uploader")

    if 'texto_pdf_processado' not in st.session_state:
        st.session_state.texto_pdf_processado = None
    if 'nome_pdf_processado' not in st.session_state:
        st.session_state.nome_pdf_processado = ""


    if uploaded_pdf_file is not None:
        if st.button("Processar Arquivo PDF", key="btn_processar_pdf"):
            with st.spinner(f"Lendo e processando o PDF: {uploaded_pdf_file.name}..."):
                try:
                    bytes_pdf = uploaded_pdf_file.read()
                    doc_pdf_st = fitz.open(stream=bytes_pdf, filetype="pdf")
                    texto_completo_pdf_st = ""
                    for pagina_st in doc_pdf_st:
                        texto_completo_pdf_st += pagina_st.get_text()
                    doc_pdf_st.close()
                    st.session_state.texto_pdf_processado = texto_completo_pdf_st
                    st.session_state.nome_pdf_processado = uploaded_pdf_file.name

                    if st.session_state.texto_pdf_processado.strip():
                        st.success(f"PDF '{st.session_state.nome_pdf_processado}' processado! Amostra abaixo.")
                        st.text_area("Amostra do Texto Extraído (Primeiros 1000 caracteres):", value=st.session_state.texto_pdf_processado[:1000], height=200, disabled=True, key="pdf_amostra_texto")
                    else:
                        st.warning(f"Não foi possível extrair texto do PDF '{st.session_state.nome_pdf_processado}'.")
                        st.session_state.texto_pdf_processado = None
                except Exception as e_pdf_proc:
                    st.error(f"Erro ao processar o PDF: {e_pdf_proc}")
                    st.session_state.texto_pdf_processado = None

    if st.session_state.texto_pdf_processado and st.session_state.texto_pdf_processado.strip():
        st.markdown("---")
        st.write(f"Agora você pode fazer perguntas sobre o PDF '{st.session_state.nome_pdf_processado}':")
        pergunta_pdf_st = st.text_area("Sua pergunta sobre o conteúdo do PDF:", key="pdf_pergunta_usuario", height=100)
        if st.button("Perguntar sobre PDF", key="btn_perguntar_pdf"):
            if pergunta_pdf_st:
                prompt_pdf_qa = f"""Baseando-se EXCLUSIVAMENTE no seguinte texto extraído do PDF '{st.session_state.nome_pdf_processado}':
TEXTO:
\"\"\"
{st.session_state.texto_pdf_processado[:30000]}
\"\"\"
Responda à pergunta: "{pergunta_pdf_st}"
Se a resposta não estiver no texto, indique isso.
RESPOSTA:"""
                with st.spinner(f"Analisando o texto do PDF '{st.session_state.nome_pdf_processado}'..."):
                    try:
                        if not modelo_ia_geral: st.error("ERRO: Modelo IA não carregado."); return
                        resposta_pdf_qa = modelo_ia_geral.generate_content(prompt_pdf_qa)
                        st.markdown(f"### Resposta (Baseada no PDF '{st.session_state.nome_pdf_processado}'):")
                        st.markdown(resposta_pdf_qa.text)
                    except Exception as e_pdf_qa:
                        st.error(f"Erro ao responder sobre o PDF: {e_pdf_qa}")
            else:
                st.warning("Por favor, digite uma pergunta.")
    st.markdown("---")


elif opcao_menu_st == "Sobre o CHABAD - Torá com IA":
    mensagem_final_st() # Chama a função definida anteriormente

# Mensagem de rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com ❤️ e a sabedoria da Torá.")
st.sidebar.markdown("Protótipo por Yaakov Israel.")
