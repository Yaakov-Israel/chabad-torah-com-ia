# Bloco 1: Instalação de Pacotes e Configuração Inicial (Adaptado para Google Gemini)

# Instala/Atualiza as bibliotecas necessárias para tentar resolver conflitos
!pip install -U langchain langchain-google-genai google-generativeai google-ai-generativelanguage google-colab pillow -q

import os
from google.colab import userdata # Para buscar a chave API dos secrets do Colab
import google.generativeai as genai # Importa a SDK do Google GenAI
from langchain_google_genai import ChatGoogleGenerativeAI # Importa o wrapper do LangChain para Gemini
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

# --- Configuração da Chave API do Google usando Colab Secrets ---
# >>>>> CERTIFIQUE-SE QUE ESTA LINHA ABAIXO CONTÉM O NOME EXATO DO SECRET CRIADO NO PASSO 1 <<<<<
NOME_DO_SEU_SECRET_NO_COLAB = 'MINHA_CHAVE_API'
# (Esta linha está PERFEITA, pois o nome do seu secret é 'MINHA_CHAVE_API')

GOOGLE_API_KEY = None # Inicializa como None
print(f"Tentando carregar o secret: '{NOME_DO_SEU_SECRET_NO_COLAB}'...")
try:
    # Aqui ele vai tentar ler o secret com o nome 'MINHA_CHAVE_API'
    GOOGLE_API_KEY = userdata.get(NOME_DO_SEU_SECRET_NO_COLAB)

    # LINHA DE DEPURAÇÃO CRUCIAL:
    print(f"Valor bruto retornado por userdata.get('{NOME_DO_SEU_SECRET_NO_COLAB}'): [{GOOGLE_API_KEY}]")
    # (Precisamos MUITO ver o que esta linha acima vai imprimir quando você rodar)

    if GOOGLE_API_KEY and GOOGLE_API_KEY.strip(): # Verifica se não é None e não é uma string vazia/só com espaços
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        genai.configure(api_key=GOOGLE_API_KEY)
        print(f"✅ Chave API encontrada e configurada a partir do secret '{NOME_DO_SEU_SECRET_NO_COLAB}'.")
    else:
        print(f"⚠️ O secret '{NOME_DO_SEU_SECRET_NO_COLAB}' foi encontrado, mas está vazio ou contém apenas espaços.")
        GOOGLE_API_KEY = None # Garante que é None se estiver vazio

except userdata.SecretNotFoundError:
    print(f"############################################################################")
    print(f"# 🚨 ATENÇÃO: Secret '{NOME_DO_SEU_SECRET_NO_COLAB}' NÃO ENCONTRADO NO COLAB! #")
    print(f"# Verifique na interface de Secrets do Colab (ícone de chave 🔑) se:          #")
    print(f"# 1. Você criou um secret com o NOME EXATO: '{NOME_DO_SEU_SECRET_NO_COLAB}'.   #")
    print(f"# 2. O campo VALOR deste secret contém sua chave API (que começa com AIzaSy...).#")
    print(f"# 3. A opção 'Acesso do notebook' está ATIVADA para este secret.             #")
    print(f"############################################################################")
    GOOGLE_API_KEY = None # Garante que é None se não encontrado
except Exception as e:
    print(f"😥 Ocorreu um erro inesperado ao buscar o secret '{NOME_DO_SEU_SECRET_NO_COLAB}': {e}")
    GOOGLE_API_KEY = None # Garante que é None em outros erros

# Inicializa o modelo LLM (usando Gemini 1.5 Flash)
llm = None
if GOOGLE_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                     temperature=0.7,
                                     convert_system_message_to_human=True)
        print("✅ Modelo LLM (Google Gemini 1.5 Flash) inicializado com sucesso!")
    except Exception as e:
        print(f"############################################################################")
        print(f"# 😥 ERRO AO INICIALIZAR O MODELO LLM DO GOOGLE: {e}                      #")
        print(f"# Verifique se:                                                            #")
        print(f"# 1. Sua chave API (lida do secret '{NOME_DO_SEU_SECRET_NO_COLAB}') é válida e funcional. #")
        print(f"# 2. A API 'Generative Language API' está ATIVA no seu projeto Google Cloud associado a esta chave.#")
        print(f"# 3. Você tem permissões e/ou cotas suficientes para usar o modelo.        #")
        print(f"############################################################################")
else:
    print(f"❌ A chave API do Google não foi carregada corretamente do secret '{NOME_DO_SEU_SECRET_NO_COLAB}'. O modelo LLM não pode ser inicializado.")


# --- Definição do Super Agente ---
class SuperAgentePequenasEmpresas:
    def __init__(self, llm_model):
        if llm_model is None:
            raise ValueError("Modelo LLM não foi inicializado. Verifique a configuração da API Key e os logs acima.")
        self.llm = llm_model
        self.system_message_template = """
        Você é o "IA - Varejo Master", um super especialista em trazer soluções inovadoras de IA
        para serem aplicadas em pequenas empresas. Sua comunicação deve ser objetiva, sucinta,
        prática e focada em resolver as dores do usuário.
        """

    def _criar_chain(self, area_especifica_prompt=""):
        prompt_template_msgs = [
            SystemMessagePromptTemplate.from_template(self.system_message_template + "\n" + area_especifica_prompt),
            HumanMessagePromptTemplate.from_template("{solicitacao_usuario}")
        ]
        chat_prompt = ChatPromptTemplate.from_messages(prompt_template_msgs)
        return LLMChain(llm=self.llm, prompt=chat_prompt, verbose=False)

    def responder_pergunta_geral(self, solicitacao_usuario):
        chain = self._criar_chain("Seu foco é fornecer uma visão geral e conselhos práticos.")
        resposta = chain.run({"solicitacao_usuario": solicitacao_usuario})
        return resposta

    def gestao_financeira(self, solicitacao_usuario):
        prompt_especifico = "Foco Atual: Gestão Financeira. Detalhe aspectos como fluxo de caixa, contas a pagar/receber, e conciliação bancária."
        chain = self._criar_chain(prompt_especifico)
        return chain.run({"solicitacao_usuario": solicitacao_usuario})

    def planejamento_financeiro(self, solicitacao_usuario):
        prompt_especifico = "Foco Atual: Planejamento Financeiro. Forneça orientações claras, passos práticos e sugestões de ferramentas/templates."
        chain = self._criar_chain(prompt_especifico)
        return chain.run({"solicitacao_usuario": solicitacao_usuario})

    def controle_de_custos(self, solicitacao_usuario):
        prompt_especifico = "Foco Atual: Controle de Custos. Apresente estratégias para identificar, analisar e reduzir custos fixos e variáveis."
        chain = self._criar_chain(prompt_especifico)
        return chain.run({"solicitacao_usuario": solicitacao_usuario})

    def precificacao(self, solicitacao_usuario):
        prompt_especifico = "Foco Atual: Precificação de Produtos/Serviços. Explique métodos como markup, margem de contribuição e precificação baseada em valor."
        chain = self._criar_chain(prompt_especifico)
        return chain.run({"solicitacao_usuario": solicitacao_usuario})

    def acesso_a_credito(self, solicit
