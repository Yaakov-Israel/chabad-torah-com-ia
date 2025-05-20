import streamlit as st
import google.generativeai as genai
import random
import os
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import lxml

# --- Configuração da Página ---
st.set_page_config(page_title="CHABAD - Torá com IA", layout="wide", initial_sidebar_state="expanded")

# --- Carregar API Key e Configurar Modelo ---
GOOGLE_API_KEY = None
modelo_ia_geral = None

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("ERRO: Chave API 'GOOGLE_API_KEY' não encontrada nos Segredos do Streamlit.")
    st.info("Adicione sua GOOGLE_API_KEY aos Segredos do seu app no Streamlit Cloud.")
    st.stop()
except FileNotFoundError: # Mais para dev local
    st.error("ERRO: Arquivo de Segredos (secrets.toml) não encontrado.")
    st.info("No Streamlit Cloud, configure os segredos na interface.")
    st.stop()

if not GOOGLE_API_KEY:
    st.error("ERRO: GOOGLE_API_KEY não carregada ou vazia.")
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.sidebar.error(f"ERRO ao configurar API Key: {e}")
    st.stop()

try:
    modelo_ia_geral = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.sidebar.error(f"ERRO ao carregar modelo Gemini: {e}")
    st.stop()

# --- Título Principal ---
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

def solicitar_ia(prompt_texto):
    if not modelo_ia_geral: return "ERRO INTERNO: Modelo de IA não inicializado."
    try:
        resposta = modelo_ia_geral.generate_content(prompt_texto)
        return resposta.text
    except Exception as e:
        return f"Erro na comunicação com a IA: {e}"

def responder_como_sabio_st(nome_sabio, pergunta_usuario):
    prompt = f"Por favor, responda à seguinte pergunta como se você fosse o {nome_sabio}, utilizando a sua conhecida lógica, sabedoria e os ensinamentos judaicos que lhe são característicos. A pergunta é: \"{pergunta_usuario}\""
    return solicitar_ia(prompt)

def explicar_conceito_idade_st(conceito, idade_str):
    try:
        idade = int(idade_str)
        if idade <= 0: return "A idade deve ser um número positivo."
    except ValueError: return "A idade precisa ser um número."
    prompt = f"Por favor, explique o conceito judaico de '{conceito}' de maneira simples e clara, adaptada para alguém com {idade} anos. Utilize linguagem, exemplos e analogias apropriadas."
    return solicitar_ia(prompt)

def buscar_salmo_formatado_st(numero_salmo_str, lista_formatos):
    try:
        num_salmo = int(numero_salmo_str)
        if not 1 <= num_salmo <= 150: return "Número do Salmo inválido (1-150)."
    except ValueError: return "Por favor, digite um número válido para o Salmo."
    if not lista_formatos: return "Escolha pelo menos um formato."
    prompt = f"Preciso do Salmo (Tehilim) número {num_salmo}.\nPor favor, apresente-o nos seguintes formatos: {', '.join(lista_formatos)}.\n\nFormatos:\n- 'hebraico': Com nikud.\n- 'português': Tradução.\n- 'transliterado': Para falantes de português.\n- 'ídiche': Em Ídiche.\n\nSe algum formato não estiver disponível, mencione. Organize de forma clara."
    return solicitar_ia(prompt)

def buscar_informacoes_festa_st(nome_festa):
    prompt_conciso = f"Descrição concisa da festa judaica '{nome_festa}', significado principal e quando ocorre."
    conciso = solicitar_ia(prompt_conciso)
    detalhado = ""
    if conciso and not conciso.startswith("Erro"):
        prompt_detalhado = f"Para a festa '{nome_festa}', elabore sobre: principais mitzvot e costumes, proibições importantes (trabalho, alimentação, etc.), e significado espiritual/histórico das observâncias."
        detalhado = solicitar_ia(prompt_detalhado)
    return conciso, detalhado

def gerar_resposta_inicial_st(pergunta):
    prompt = f"Resposta inicial concisa e direta para: \"{pergunta}\""
    return solicitar_ia(prompt)

def gerar_resposta_detalhada_st(pergunta, instrucao, resposta_curta=None):
    prompt = ""
    if instrucao == "aprofundar_curta" and resposta_curta:
        prompt = f"Sobre a pergunta \"{pergunta}\" (resposta inicial: \"{resposta_curta}\"), aprofunde com detalhes, exemplos ou fontes."
    elif instrucao == "detalhar_original":
        prompt = f"Sobre a pergunta: \"{pergunta}\", forneça uma resposta completa e detalhada, explorando facetas, fontes e compreensão abrangente."
    else: return "Instrução de detalhamento não reconhecida."
    return solicitar_ia(prompt)

def encontrar_conexoes_judaicas_st(item1, item2):
    prompt = f"Considere os elementos judaicos:\n1: \"{item1}\"\n2: \"{item2}\"\n\nExplore e explique conexões, paralelos, contrastes ou lições ao relacioná-los. Baseie-se em fontes e sabedoria judaica. Seja criativo e profundo."
    return solicitar_ia(prompt)

def analisar_versiculo_pardes_st(referencia_versiculo):
    prompt = f"Analise o versículo da Torá: \"{referencia_versiculo}\" nos 4 níveis do Pardes (Pshat, Remez, Drash, Sod). Explique cada nível concisamente. Se um nível for complexo ou menos aplicável, indique."
    return solicitar_ia(prompt)

def buscar_historia_ou_ensinamento_rebe_st(nome_rebe_req):
    rebe_final = nome_rebe_req
    if nome_rebe_req.lower() == "aleatorio":
        rebe_final = random.choice(nomes_dos_rebes_chabad_lista)
        st.write(f"(Sorteado: {rebe_final})")
    prompt = f"Compartilhe um ensinamento inspirador OU uma história curta e significativa sobre {rebe_final}.\nInclua uma nota breve sobre quem foi este Rebe e sua liderança. Objetivo: transmitir a essência de seu legado Chabad de forma edificante."
    return solicitar_ia(prompt)

def apresentar_dica_judaica_do_dia_st():
    tipo_dica = random.choice(["halacha", "mitzva"])
    prompt, titulo = "", ""
    if tipo_dica == "halacha":
        prompt = "Compartilhe uma Halachá prática e concisa, relevante para o dia a dia, com breve explicação de sua importância ou aplicação."
        titulo = "💡 Halachá do Dia 💡"
    else:
        prompt = "Sugira uma Mitzvá (ou boa ação) para focar hoje/semana, com breve explicação do significado e sugestão prática."
        titulo = "✨ Mitzvá para Inspirar ✨"
    st.subheader(titulo)
    with st.spinner("Buscando inspiração..."):
        dica = solicitar_ia(prompt)
    st.markdown(dica)
    st.markdown("---")

def conduzir_estudo_dirigido_st():
    st.subheader("🌟 Modo Estudo Dirigido 🌟")
    if 'sd_tipo' not in st.session_state: st.session_state.sd_tipo = None
    if 'sd_topico' not in st.session_state: st.session_state.sd_topico = ""
    if 'sd_etapa' not in st.session_state: st.session_state.sd_etapa = 0

    if st.session_state.sd_etapa == 0:
        tipo = st.radio("Estudar:", ("Parashá da Semana", "Tema Geral do Judaísmo"), key="sd_radio_tipo", horizontal=True)
        st.session_state.sd_topico = st.text_input(f"Qual {tipo.split()[0].lower()} você gostaria de estudar?", key="sd_input_topico")
        if st.button("Iniciar Estudo Dirigido", key="sd_btn_iniciar"):
            if st.session_state.sd_topico:
                st.session_state.sd_tipo = tipo.split()[0].lower()
                st.session_state.sd_etapa = 1
                st.rerun()
            else: st.warning("Informe a Parashá ou Tema.")
    
    prompts_estudo = {
        "parasha": [
            (f"Resumo conciso dos principais eventos e temas da Parashá '{{topico}}'.", "Resumo da Parashá: {topico}"),
            (f"Um versículo chave da Parashá '{{topico}}' e por quê? Apresente o versículo e breve explicação.", "Versículo Chave e Significado"),
            (f"Sobre a Parashá '{{topico}}', um comentário importante de Rashi sobre um tema ou versículo.", "Comentário de Rashi"),
            (f"Uma lição prática para nossos dias da Parashá '{{topico}}'.", "Lição Para Nossos Dias")
        ],
        "tema": [
            (f"Introdução clara e concisa sobre o tema '{{topico}}' no Judaísmo e sua importância.", "Introdução ao Tema: {topico}"),
            (f"Conceitos chave, fontes principais (Torá, Talmud, Sábios) relacionados ao tema '{{topico}}'.", "Conceitos Chave e Fontes"),
            (f"Como o entendimento do tema '{{topico}}' pode impactar a vida diária ou que reflexão ele convida?", "Aplicação ou Reflexão")
        ]
    }

    if 0 < st.session_state.sd_etapa <= len(prompts_estudo.get(st.session_state.sd_tipo, [])):
        etapa_atual = st.session_state.sd_etapa -1
        prompt_template, titulo_template = prompts_estudo[st.session_state.sd_tipo][etapa_atual]
        
        prompt_final = prompt_template.format(topico=st.session_state.sd_topico)
        titulo_final = titulo_template.format(topico=st.session_state.sd_topico)
        
        st.markdown(f"### {titulo_final}")
        if 'sd_conteudo_etapa' not in st.session_state or st.session_state.get('sd_etapa_atual_processada') != st.session_state.sd_etapa :
            with st.spinner("Buscando informações..."):
                st.session_state.sd_conteudo_etapa = solicitar_ia(prompt_final)
                st.session_state.sd_etapa_atual_processada = st.session_state.sd_etapa
        st.markdown(st.session_state.sd_conteudo_etapa)

        if st.session_state.sd_etapa < len(prompts_estudo[st.session_state.sd_tipo]):
            if st.button("Próxima Etapa", key=f"sd_btn_next_etapa{st.session_state.sd_etapa}"):
                st.session_state.sd_etapa += 1
                st.rerun()
        else:
            st.success("Fim do Estudo Dirigido sobre este tópico.")
        
        if st.button("Encerrar/Novo Estudo Dirigido", key="sd_btn_reset"):
            st.session_state.sd_etapa = 0
            st.session_state.sd_tipo = None
            st.session_state.sd_topico = ""
            st.session_state.pop('sd_conteudo_etapa', None)
            st.session_state.pop('sd_etapa_atual_processada', None)
            st.rerun()
    st.markdown("---")


def interagir_com_chavruta_st():
    st.subheader("🗣️ Chavruta Interativa com Sábio")
    if 'ch_sabio' not in st.session_state: st.session_state.ch_sabio = ""
    if 'ch_tema' not in st.session_state: st.session_state.ch_tema = ""
    if 'ch_estilo' not in st.session_state: st.session_state.ch_estilo = "moderna"
    if 'ch_historico' not in st.session_state: st.session_state.ch_historico = []
    if 'ch_iniciada' not in st.session_state: st.session_state.ch_iniciada = False

    if not st.session_state.ch_iniciada:
        cols = st.columns(3)
        with cols[0]: st.session_state.ch_sabio = st.text_input("Sábio:", value=st.session_state.ch_sabio, key="ch_input_sabio")
        with cols[1]: st.session_state.ch_tema = st.text_input("Tema:", value=st.session_state.ch_tema, key="ch_input_tema")
        with cols[2]: st.session_state.ch_estilo = st.radio("Linguagem:", ["moderna", "tradicional"], index=["moderna", "tradicional"].index(st.session_state.ch_estilo), key="ch_radio_estilo", horizontal=True)
        
        if st.button("Iniciar Chavruta", key="ch_btn_iniciar"):
            if st.session_state.ch_sabio and st.session_state.ch_tema:
                st.session_state.ch_iniciada = True
                inst_lang = "Adapte sua linguagem para ser moderna, clara e acessível." if st.session_state.ch_estilo == "moderna" else "Use uma linguagem que reflita erudição e estilo da sua época."
                st.session_state.ch_historico = [
                    f"Você é o Sábio {st.session_state.ch_sabio}. Eu sou seu parceiro de estudo (Chavruta) sobre '{st.session_state.ch_tema}'. Mantenha sua persona. {inst_lang} Por favor, comece me saudando e perguntando sobre o que em '{st.session_state.ch_tema}' eu gostaria de começar."
                ]
                with st.spinner("Iniciando..."):
                    saudacao = solicitar_ia(st.session_state.ch_historico[0] + f"\nSua saudação e pergunta inicial como {st.session_state.ch_sabio}:")
                st.session_state.ch_historico.append(f"Sábio: {saudacao}") # Nome genérico 'Sábio' para o histórico
                st.rerun()
            else: st.warning("Preencha Sábio e Tema.")
    
    if st.session_state.ch_iniciada:
        st.markdown(f"**Estudo com: {st.session_state.ch_sabio} | Tema: {st.session_state.ch_tema} | Linguagem: {st.session_state.ch_estilo}**")
        for i, msg in enumerate(st.session_state.ch_historico):
            if i == 0 and "Você é o Sábio" in msg: continue
            if msg.startswith("Eu:"): st.text_area("Você:", value=msg[3:].strip(), height=75, disabled=True, key=f"ch_hist_u_{i}")
            elif msg.startswith("Sábio:"): st.text_area(f"{st.session_state.ch_sabio}:", value=msg[len("Sábio:")+1:].strip(), height=150, disabled=True, key=f"ch_hist_s_{i}")
        
        user_msg = st.text_input("Sua vez:", key="ch_input_user_msg")
        col_send, col_end = st.columns(2)
        with col_send:
            if st.button("Enviar", key="ch_btn_send"):
                if user_msg:
                    st.session_state.ch_historico.append(f"Eu: {user_msg}")
                    prompt_atual = "\n".join(st.session_state.ch_historico) + f"\nSua resposta como {st.session_state.ch_sabio}:"
                    with st.spinner(f"{st.session_state.ch_sabio} está pensando..."):
                        resposta = solicitar_ia(prompt_atual)
                    st.session_state.ch_historico.append(f"Sábio: {resposta}")
                    st.rerun()
                else: st.warning("Digite sua mensagem.")
        with col_end:
            if st.button("Encerrar Chavruta", key="ch_btn_end"):
                st.success(f"{st.session_state.ch_sabio}: Que nosso estudo tenha sido proveitoso! Shalom.")
                st.session_state.ch_iniciada = False
                st.session_state.ch_historico = []
                st.session_state.ch_sabio, st.session_state.ch_tema, st.session_state.ch_estilo = "", "", "moderna"
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
    "Pensamento de Chassidut para o Dia",
    "Consultar um Sábio",
    "Chavruta Interativa com Sábio",
    "Explicar Conceito Judaico por Idade",
    "Leitura de Salmos (Tehilim)",
    "Explorar Festas Judaicas",
    "Pergunta com Opção de Aprofundamento",
    "Análise Pardes de um Versículo",
    "Sabedoria dos Rebes de Chabad",
    "Halachá/Mitzvá do Dia",
    "Conexões da Sabedoria Judaica",
    "Estudo Dirigido (Parashá/Tema)",
    "Explorar Conteúdo de Página Web (Upload HTML)",
    "Explorar Conteúdo de Livro PDF (Upload PDF)",
    "Sobre o CHABAD - Torá com IA"
]
opcao_menu_st = st.sidebar.selectbox(
    "O que você gostaria de fazer hoje?",
    opcoes_do_menu_lista_completa,
    key="menu_principal_selectbox_final"
)

# --- Execução da Funcionalidade Escolhida ---

if opcao_menu_st == "--- Escolha uma Ferramenta ---":
    st.info("⬅️ Por favor, escolha uma ferramenta de estudo na barra lateral para começar!")
    # st.balloons()

elif opcao_menu_st == "Pensamento de Chassidut para o Dia":
    st.subheader("Pensamento de Chassidut para o Dia")
    if lista_de_pensamentos_chabad:
        if st.button("Gerar Novo Pensamento", key="btn_pensamento_chassidut_gerar"):
            pensamento_selecionado = random.choice(lista_de_pensamentos_chabad)
            st.markdown(f"## > *{pensamento_selecionado}*")
        else:
            st.write("Clique no botão para um pensamento inspirador.")
    else:
        st.write("Nenhum pensamento disponível no momento.")
    st.markdown("---")

elif opcao_menu_st == "Consultar um Sábio":
    st.subheader("Consultar um Sábio")
    if 'cs_sabio_nome_st' not in st.session_state: st.session_state.cs_sabio_nome_st = ""
    if 'cs_sabio_pergunta_st' not in st.session_state: st.session_state.cs_sabio_pergunta_st = ""

    nome_sabio_cs_st = st.text_input("Nome do Sábio:", value=st.session_state.cs_sabio_nome_st, key="cs_nome_sabio_final")
    pergunta_cs_st = st.text_area(f"Sua pergunta para {nome_sabio_cs_st if nome_sabio_cs_st else 'o Sábio'}:", value=st.session_state.cs_sabio_pergunta_st, key="cs_pergunta_sabio_final", height=100)

    if st.button("Enviar Consulta ao Sábio", key="cs_btn_enviar_final"):
        st.session_state.cs_sabio_nome_st = nome_sabio_cs_st
        st.session_state.cs_sabio_pergunta_st = pergunta_cs_st
        if nome_sabio_cs_st and pergunta_cs_st:
            with st.spinner(f"Consultando {nome_sabio_cs_st}..."):
                resposta = responder_como_sabio_st(nome_sabio_cs_st, pergunta_cs_st)
            st.markdown(f"### Resposta (como {nome_sabio_cs_st}):")
            st.markdown(resposta)
        else:
            st.warning("Preencha o nome do Sábio e a pergunta.")
    st.markdown("---")

elif opcao_menu_st == "Chavruta Interativa com Sábio":
    interagir_com_chavruta_st()

elif opcao_menu_st == "Explicar Conceito Judaico por Idade":
    st.subheader("Explicar Conceito Judaico por Idade")
    if 'ei_conceito_st' not in st.session_state: st.session_state.ei_conceito_st = ""
    if 'ei_idade_st' not in st.session_state: st.session_state.ei_idade_st = "7"

    conceito_ei_st_val = st.text_input("Qual conceito judaico você gostaria de entender?", value=st.session_state.ei_conceito_st, key="ei_conceito_final")
    idade_ei_st_val = st.text_input(f"Para qual idade (número) você gostaria da explicação de '{conceito_ei_st_val}'?", value=st.session_state.ei_idade_st, key="ei_idade_final")

    if st.button("Explicar Conceito por Idade", key="ei_btn_explicar_final"):
        st.session_state.ei_conceito_st = conceito_ei_st_val
        st.session_state.ei_idade_st = idade_ei_st_val
        if conceito_ei_st_val and idade_ei_st_val:
            with st.spinner(f"Preparando explicação de '{conceito_ei_st_val}' para {idade_ei_st_val} anos..."):
                explicacao = explicar_conceito_idade_st(conceito_ei_st_val, idade_ei_st_val)
            st.markdown(explicacao)
        else:
            st.warning("Forneça o conceito e a idade.")
    st.markdown("---")

elif opcao_menu_st == "Leitura de Salmos (Tehilim)":
    st.subheader("📜 Leitura dos Salmos (Tehilim)")
    if 'salmo_num_st_val' not in st.session_state: st.session_state.salmo_num_st_val = "1"
    if 'salmo_formatos_st_val' not in st.session_state: st.session_state.salmo_formatos_st_val = "hebraico, português"

    num_salmo_st_val = st.text_input("Digite o número do Salmo (1-150):", value=st.session_state.salmo_num_st_val, key="salmo_num_final")
    formatos_st_str_val = st.text_input("Formatos (hebraico, português, transliterado, ídiche) - separados por vírgula:", value=st.session_state.salmo_formatos_st_val, key="salmo_formatos_final")
    
    if st.button("Ler Salmo Selecionado", key="btn_ler_salmo_final"):
        st.session_state.salmo_num_st_val = num_salmo_st_val
        st.session_state.salmo_formatos_st_val = formatos_st_str_val
        formatos_lista_st_val = [fmt.strip() for fmt in formatos_st_str_val.split(',') if fmt.strip()]
        if num_salmo_st_val and formatos_lista_st_val:
            with st.spinner(f"Buscando Salmo {num_salmo_st_val}..."):
                resultado = buscar_salmo_formatado_st(num_salmo_st_val, formatos_lista_st_val)
            st.markdown(resultado)
            st.caption("Lembre-se: Para estudo e uso litúrgico, sempre consulte um Sefer Tehilim ou Siddur de confiança.")
        else:
            st.warning("Número do Salmo ou formato não fornecido.")
    st.markdown("---")

elif opcao_menu_st == "Explorar Festas Judaicas":
    st.subheader("🎉 Explorar Festas Judaicas")
    if 'festa_nome_st_val' not in st.session_state: st.session_state.festa_nome_st_val = ""

    nome_festa_st_val = st.text_input("Sobre qual festa judaica você gostaria de aprender?", value=st.session_state.festa_nome_st_val, key="festa_nome_final")
    if st.button("Buscar Informações da Festa Escolhida", key="btn_buscar_festa_final"):
        st.session_state.festa_nome_st_val = nome_festa_st_val
        if nome_festa_st_val:
            with st.spinner(f"Buscando informações sobre {nome_festa_st_val}..."):
                conciso_f_val, detalhado_f_val = buscar_informacoes_festa_st(nome_festa_st_val)
            st.markdown(f"### Resumo Conciso de {nome_festa_st_val}")
            st.markdown(conciso_f_val)
            st.markdown(f"### Detalhes e Aprofundamento sobre {nome_festa_st_val}")
            st.markdown(detalhado_f_val)
        else:
            st.warning("Digite o nome de uma festa.")
    st.markdown("---")

elif opcao_menu_st == "Pergunta com Opção de Aprofundamento":
    st.subheader("💡 Pergunta com Opção de Aprofundamento")
    if 'pa_pergunta_st_val' not in st.session_state: st.session_state.pa_pergunta_st_val = ""
    if 'pa_resposta_curta_st_val' not in st.session_state: st.session_state.pa_resposta_curta_st_val = None
    if 'pa_escolha_st_val' not in st.session_state: st.session_state.pa_escolha_st_val = "Nada"


    pergunta_pa_st_val = st.text_area("Qual é a sua pergunta sobre Judaísmo?", value=st.session_state.pa_pergunta_st_val, key="pa_pergunta_area_final", height=100)

    if st.button("Obter Resposta Inicial para Pergunta", key="btn_pa_inicial_final"):
        st.session_state.pa_pergunta_st_val = pergunta_pa_st_val
        st.session_state.pa_resposta_curta_st_val = None 
        if pergunta_pa_st_val:
            with st.spinner("Buscando resposta inicial..."):
                st.session_state.pa_resposta_curta_st_val = gerar_resposta_inicial_st(pergunta_pa_st_val)
            st.markdown("### Resposta Inicial (Sucinta)")
            st.markdown(st.session_state.pa_resposta_curta_st_val)
        else:
            st.warning("Por favor, faça uma pergunta.")

    if st.session_state.pa_resposta_curta_st_val and not "Erro na resposta inicial" in st.session_state.pa_resposta_curta_st_val:
        st.write("---")
        opcoes_aprofundamento = ["Nada", "Aprofundar esta resposta", "Tentar resposta mais detalhada para pergunta original"]
        st.session_state.pa_escolha_st_val = st.radio("O que fazer agora?", 
                                 opcoes_aprofundamento, 
                                 index=opcoes_aprofundamento.index(st.session_state.pa_escolha_st_val) if st.session_state.pa_escolha_st_val in opcoes_aprofundamento else 0,
                                 key="pa_radio_escolha_final", horizontal=True)
        
        if st.session_state.pa_escolha_st_val == "Aprofundar esta resposta":
            if st.button("Confirmar Aprofundamento da Resposta", key="btn_pa_aprofundar_anterior_final"):
                with st.spinner("Aprofundando a resposta dada..."):
                    resposta_final_pa_val = gerar_resposta_detalhada_st(st.session_state.pa_pergunta_st_val, "aprofundar_curta", st.session_state.pa_resposta_curta_st_val)
                st.markdown("### Aprofundamento da Resposta Anterior")
                st.markdown(resposta_final_pa_val)
        elif st.session_state.pa_escolha_st_val == "Tentar resposta mais detalhada para pergunta original":
            if st.button("Confirmar Detalhamento da Pergunta Original", key="btn_pa_detalhar_original_final"):
                with st.spinner("Buscando uma resposta mais detalhada para sua pergunta original..."):
                    resposta_final_pa_val = gerar_resposta_detalhada_st(st.session_state.pa_pergunta_st_val, "detalhar_original")
                st.markdown("### Resposta Detalhada da Pergunta Original")
                st.markdown(resposta_final_pa_val)
    st.markdown("---")


elif opcao_menu_st == "Análise Pardes de um Versículo":
    st.subheader("🔍 Análise Pardes de um Versículo da Torá")
    if 'pardes_versiculo_st_val' not in st.session_state: st.session_state.pardes_versiculo_st_val = "Gênesis 1:1"
    
    versiculo_pardes_st_val = st.text_input("Digite a referência do versículo da Torá (ex: Gênesis 1:1):", value=st.session_state.pardes_versiculo_st_val, key="pardes_versiculo_final")
    if st.button("Analisar Versículo (Pardes)", key="btn_analisar_pardes_final"):
        st.session_state.pardes_versiculo_st_val = versiculo_pardes_st_val
        if versiculo_pardes_st_val:
            with st.spinner(f"Analisando '{versiculo_pardes_st_val}' nos níveis do Pardes..."):
                resultado = analisar_versiculo_pardes_st(versiculo_pardes_st_val)
            st.markdown(f"### Análise Pardes para: {versiculo_pardes_st_val}")
            st.markdown(resultado)
            st.caption("Lembre-se: A profundidade do Pardes é vasta. Esta é uma introdução.")
        else:
            st.warning("Digite a referência de um versículo.")
    st.markdown("---")

elif opcao_menu_st == "Sabedoria dos Rebes de Chabad":
    st.subheader("🌟 Sabedoria dos Rebes de Chabad")
    if 'rebe_escolha_st_val' not in st.session_state: st.session_state.rebe_escolha_st_val = "Escolha um Rebe"

    opcoes_rebes_st_lista = ["Escolha um Rebe"] + nomes_dos_rebes_chabad_lista + ["Um Rebe Aleatório"]
    rebe_selecionado_st_val = st.selectbox("Selecione:", opcoes_rebes_st_lista, index=opcoes_rebes_st_lista.index(st.session_state.rebe_escolha_st_val) if st.session_state.rebe_escolha_st_val in opcoes_rebes_st_lista else 0, key="rebe_selectbox_final")
    
    if st.button("Buscar Ensinamento/História", key="btn_buscar_rebe_final"):
        st.session_state.rebe_escolha_st_val = rebe_selecionado_st_val
        rebe_para_consulta_final = ""
        if rebe_selecionado_st_val != "Escolha um Rebe":
            if rebe_selecionado_st_val == "Um Rebe Aleatório":
                rebe_para_consulta_final = "aleatorio"
            else:
                rebe_para_consulta_final = rebe_selecionado_st_val
            
            with st.spinner(f"Buscando sabedoria..."):
                resultado = buscar_historia_ou_ensinamento_rebe_st(rebe_para_consulta_final)
            st.markdown("### Um Ensinamento ou História do Rebe")
            st.markdown(resultado)
        else:
            st.warning("Selecione um Rebe ou a opção aleatória.")
    st.markdown("---")

elif opcao_menu_st == "Halachá/Mitzvá do Dia":
    apresentar_dica_judaica_do_dia_st()

elif opcao_menu_st == "Conexões da Sabedoria Judaica":
    st.subheader("🔗 Conexões da Sabedoria Judaica")
    if 'conexao_item1_st_val' not in st.session_state: st.session_state.conexao_item1_st_val = ""
    if 'conexao_item2_st_val' not in st.session_state: st.session_state.conexao_item2_st_val = ""

    item1_st_val = st.text_input("Digite o primeiro elemento/conceito:", value=st.session_state.conexao_item1_st_val, key="conexao_item1_final")
    item2_st_val = st.text_input("Digite o segundo elemento/conceito:", value=st.session_state.conexao_item2_st_val, key="conexao_item2_final")

    if st.button("Encontrar Conexões", key="btn_encontrar_conexoes_final"):
        st.session_state.conexao_item1_st_val = item1_st_val
        st.session_state.conexao_item2_st_val = item2_st_val
        if item1_st_val and item2_st_val:
            if item1_st_val.lower() == item2_st_val.lower():
                st.warning("Tente dois elementos diferentes.")
            else:
                with st.spinner(f"Buscando conexões entre '{item1_st_val}' e '{item2_st_val}'..."):
                    resultado = encontrar_conexoes_judaicas_st(item1_st_val, item2_st_val)
                st.markdown("### Explorando as Conexões")
                st.markdown(resultado)
        else:
            st.warning("Forneça os dois elementos.")
    st.markdown("---")

elif opcao_menu_st == "Estudo Dirigido (Parashá/Tema)":
    conduzir_estudo_dirigido_st()

elif opcao_menu_st == "Explorar Conteúdo de Página Web (Upload HTML)":
    st.subheader("📄 Explorar Conteúdo de Página Web")
    uploaded_html = st.file_uploader("Carregue seu arquivo HTML:", type=["html", "htm"], key="html_uploader_final")
    
    if 'html_texto_st' not in st.session_state: st.session_state.html_texto_st = None

    if uploaded_html is not None:
        if st.button("Processar HTML", key="btn_proc_html_final"):
            with st.spinner("Processando HTML..."):
                try:
                    html_bytes = uploaded_html.read()
                    html_str = html_bytes.decode('utf-8')
                    soup = BeautifulSoup(html_str, 'lxml')
                    paragrafos = [p.get_text(separator=' ', strip=True) for p in soup.find_all('p')]
                    st.session_state.html_texto_st = "\n".join(paragrafos)
                    if st.session_state.html_texto_st.strip():
                        st.success("HTML processado! Amostra abaixo.")
                        st.text_area("Amostra do Texto:", value=st.session_state.html_texto_st[:1000], height=150, disabled=True, key="html_amostra_final")
                    else:
                        st.warning("Não extraí texto dos parágrafos do HTML.")
                        st.session_state.html_texto_st = None
                except Exception as e: st.error(f"Erro ao processar HTML: {e}"); st.session_state.html_texto_st = None
    
    if st.session_state.html_texto_st:
        st.markdown("---")
        q_html = st.text_area("Sua pergunta sobre o conteúdo do HTML:", key="html_q_usuario_final", height=100)
        if st.button("Perguntar sobre HTML", key="btn_q_html_final"):
            if q_html:
                prompt = f"Baseando-se EXCLUSIVAMENTE no texto HTML fornecido:\nTEXTO: \"\"\"\n{st.session_state.html_texto_st[:30000]}\n\"\"\"\nResponda: \"{q_html}\"\nSe a resposta não estiver no texto, indique."
                with st.spinner("Analisando HTML..."):
                    resposta = solicitar_ia(prompt)
                st.markdown("### Resposta (Baseada no HTML):"); st.markdown(resposta)
            else: st.warning("Digite uma pergunta.")
    st.markdown("---")

elif opcao_menu_st == "Explorar Conteúdo de Livro PDF (Upload PDF)":
    st.subheader("📚 Explorar Conteúdo de Livro PDF")
    uploaded_pdf = st.file_uploader("Carregue seu arquivo PDF:", type="pdf", key="pdf_uploader_final")

    if 'pdf_texto_st' not in st.session_state: st.session_state.pdf_texto_st = None
    if 'pdf_nome_st' not in st.session_state: st.session_state.pdf_nome_st = ""

    if uploaded_pdf is not None:
        if st.button("Processar PDF", key="btn_proc_pdf_final"):
            with st.spinner(f"Processando PDF: {uploaded_pdf.name}..."):
                try:
                    pdf_bytes = uploaded_pdf.read()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    texto_pdf = "".join([page.get_text() for page in doc])
                    doc.close()
                    st.session_state.pdf_texto_st = texto_pdf
                    st.session_state.pdf_nome_st = uploaded_pdf.name
                    if st.session_state.pdf_texto_st.strip():
                        st.success(f"PDF '{st.session_state.pdf_nome_st}' processado! Amostra abaixo.")
                        st.text_area("Amostra do Texto:", value=st.session_state.pdf_texto_st[:1000], height=150, disabled=True, key="pdf_amostra_final")
                    else:
                        st.warning(f"Não extraí texto do PDF '{st.session_state.pdf_nome_st}'.")
                        st.session_state.pdf_texto_st = None
                except Exception as e: st.error(f"Erro ao processar PDF: {e}"); st.session_state.pdf_texto_st = None
    
    if st.session_state.pdf_texto_st:
        st.markdown("---")
        q_pdf = st.text_area(f"Sua pergunta sobre o conteúdo do PDF '{st.session_state.pdf_nome_st}':", key="pdf_q_usuario_final", height=100)
        if st.button("Perguntar sobre PDF", key="btn_q_pdf_final"):
            if q_pdf:
                prompt = f"Baseando-se EXCLUSIVAMENTE no texto do PDF '{st.session_state.pdf_nome_st}' fornecido:\nTEXTO: \"\"\"\n{st.session_state.pdf_texto_st[:30000]}\n\"\"\"\nResponda: \"{q_pdf}\"\nSe a resposta não estiver no texto, indique."
                with st.spinner(f"Analisando PDF '{st.session_state.pdf_nome_st}'..."):
                    resposta = solicitar_ia(prompt)
                st.markdown(f"### Resposta (Baseada no PDF '{st.session_state.pdf_nome_st}'):"); st.markdown(resposta)
            else: st.warning("Digite uma pergunta.")
    st.markdown("---")

elif opcao_menu_st == "Sobre o CHABAD - Torá com IA":
    mensagem_final_st()

# Mensagem de rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com ❤️ e a sabedoria da Torá.")
st.sidebar.markdown("Protótipo por Yaakov Israel.")
