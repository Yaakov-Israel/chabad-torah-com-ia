# CHABAD - Torá com IA: Protótipo de um Assistente de Estudo Judaico Interativo

## Visão do Projeto

O "CHABAD - Torá com IA" é um protótipo funcional desenvolvido em Python no ambiente Google Colab, utilizando a API Gemini do Google. Este projeto visa demonstrar o potencial da Inteligência Artificial como uma ferramenta poderosa e inspiradora para o estudo da Torá e do Judaísmo, com profundo respeito e alinhamento aos ensinamentos do movimento Chabad-Lubavitch.

Acreditamos que a IA pode auxiliar na jornada de cada judeu em conectar-se com a sabedoria da Torá nos seus múltiplos níveis (Chochmá, Biná, Daat), tornando o aprendizado mais acessível, personalizado e profundo.

## O Protótipo Atual (Notebook Colab)

O notebook principal deste repositório (`CHABAD_TORÁ_COM_IA.ipynb`) contém uma série de células interativas que demonstram diversas funcionalidades, incluindo:

* **Inspiração Diária:** Pensamentos de Chassidut e ensinamentos dos Rebes de Chabad.
* **Interação com Sábios:** Consultas e estudo em dupla (Chavruta) com Sábios e Rebes, com opção de estilo de linguagem.
* **Aprendizado Adaptado:** Explicações de conceitos judaicos para diferentes faixas etárias.
* **Estudo de Textos Sagrados:** Leitura de Salmos (Tehilim) em formatos variados e análise de versículos da Torá nos quatro níveis do Pardes (Pshat, Remez, Drash, Sod).
* **Vida Judaica:** Informações sobre Festas Judaicas e uma "Halachá/Mitzvá do Dia".
* **Aprofundamento e Exploração:** Respostas com opção de detalhamento e a capacidade de encontrar conexões entre diferentes temas judaicos.
* **Uso de Fontes Externas:** Leitura e interação com conteúdo de páginas web (HTML) e documentos PDF fornecidos pelo usuário.
* **Estudo Guiado:** Um modo de estudo dirigido para Parashiot ou temas gerais do Judaísmo.
* **Menu Principal:** Uma célula que serve como um índice para as funcionalidades demonstradas.

Este protótipo foi construído com foco na interatividade célula a célula do Google Colab.

## Como Executar o Protótipo (Google Colab)

1.  **Abra o Notebook no Colab:** Clique no arquivo `.ipynb` neste repositório e depois no botão "Open in Colab" (Abrir no Colab) que geralmente aparece no GitHub.
2.  **Configure sua Chave API do Google Gemini:**
    * Obtenha uma chave API no [Google AI Studio](https://aistudio.google.com/app/apikey).
    * No Colab, na barra lateral esquerda, clique no ícone de chave (🔑) "Segredos".
    * Adicione um novo segredo com o **Nome:** `GOOGLE_API_KEY` e no campo **Valor**, cole a sua chave API.
    * Certifique-se de que a opção "Acesso ao notebook" está **LIGADA**.
3.  **Instale as Dependências:** Execute a primeira célula de código do notebook, que contém:
    ```python
    !pip install PyMuPDF google-generativeai beautifulsoup4 lxml
    ```
4.  **Carregue Arquivos (Opcional, para funcionalidades específicas):**
    * Se desejar testar a leitura de HTML, carregue o arquivo `Chabad.org em português - Torá, judaísmo e informações judaicas.htm` (ou outro de sua preferência, ajustando o nome no código) para a sessão do Colab (usando o ícone de pasta 📂 > Upload).
    * Para testar a leitura de PDFs, carregue os arquivos PDF desejados (ex: `1-fonte-da-vida.pdf`) e verifique se os nomes na lista da célula correspondente estão corretos.
5.  **Execute as Células em Ordem:** Prossiga executando as células uma a uma. As células interativas pedirão seu input. Para as que entram em loop (Chavruta, Q&A de textos), digite "sair" para encerrar a interação daquela funcionalidade.

## Potencial Futuro e Convite à Colaboração

Este protótipo é a semente de um projeto com vasto potencial. Com o envolvimento e a orientação do Chabad, o "Torá com IA" pode florescer em:

* **Um Aplicativo Completo:** Com interface gráfica intuitiva para web e dispositivos móveis.
* **Integração Profunda com o Conteúdo Chabad:** Utilizando a imensa biblioteca de Sefarim, artigos, vídeos e áudios do Chabad.org e outras publicações.
* **Recursos Avançados de Personalização:** Acompanhamento do progresso do estudo, sugestões personalizadas, etc.
* **Ferramentas Comunitárias:** Espaços para estudo em grupo e discussão.

## Contato
[Yaakov Israel]
[yaakov.ysrael@gmail.com]
