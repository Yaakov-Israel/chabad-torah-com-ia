# CHABAD - Torá com IA: Um Assistente de Estudo Judaico Interativo

## Visão Geral do Projeto

O "CHABAD - Torá com IA" é um protótipo desenvolvido em Python utilizando o Google Colab e a API Gemini do Google. O objetivo deste projeto é criar um assistente de estudo da Torá e do Judaísmo que seja interativo, inspirador e alinhado com os ensinamentos e a profundidade do movimento Chabad-Lubavitch.

Este protótipo demonstra a capacidade da Inteligência Artificial de:
* Agir como renomados Sábios e Rebes, respondendo a perguntas com seus estilos e sabedoria característicos.
* Facilitar o estudo em dupla (Chavruta) de forma dinâmica.
* Explicar conceitos judaicos complexos de maneira adaptada para diferentes idades.
* Auxiliar na exploração de textos sagrados, como a Torá (nos níveis do Pardes) e os Salmos (Tehilim) em diversos formatos.
* Fornecer informações sobre o ciclo da vida judaica, como as Festas.
* Oferecer respostas concisas com opção de aprofundamento.
* Interagir com conteúdo de fontes externas (páginas web e documentos PDF) para embasar respostas e estudos.
* Estimular a reflexão através da busca por conexões entre diferentes conceitos judaicos.
* Prover inspiração diária com pensamentos de Chassidut, ensinamentos dos Rebes e Mitzvot/Halachot.

## Inspiração Chabad

O nome "CHABAD - Torá com IA" reflete a inspiração central do projeto:
* **Chabad (חב"ד):** Acrônimo para Chochmá (Sabedoria), Biná (Compreensão) e Daat (Conhecimento Aplicado). Buscamos usar a IA para auxiliar nestas três faculdades intelectuais no estudo da Torá.
* **Torá com IA:** A união da sabedoria milenar da Torá com as capacidades da Inteligência Artificial moderna, com o objetivo de tornar o estudo mais acessível, profundo e pessoal.
* **Fontes Confiáveis:** O projeto visa, em seu desenvolvimento futuro, integrar e se basear em fontes ortodoxas confiáveis, com especial apreço pelo vasto repositório de conhecimento do movimento Chabad-Lubavitch.

## Funcionalidades Implementadas (Protótipo Colab)

Este repositório contém um notebook Google Colab (`.ipynb`) com células que demonstram as seguintes funcionalidades:

1.  **Configuração da API Gemini:** Conexão com a IA do Google.
2.  **Pensamento de Chassidut Diário:** Apresenta um pensamento inspirador.
3.  **Consulta aos Sábios:** Permite ao usuário perguntar a Sábios como Rashi, Rambam, Rabi Akiva, etc.
4.  **Chavruta Interativa:** Simula um estudo em dupla com um Sábio, com opção de estilo de linguagem (tradicional/moderna).
5.  **Explicação por Idade:** Adapta a explicação de conceitos judaicos para a idade do usuário.
6.  **Leitura de Salmos (Tehilim):** Apresenta Salmos em Hebraico, Português, Transliterado e (tentativa de) Ídiche.
7.  **Explorador de Festas Judaicas:** Fornece resumo e detalhes sobre as festas.
8.  **Resposta com Aprofundamento:** Oferece respostas concisas com opção de detalhamento.
9.  **Leitura e Interação com HTML:** Extrai texto de uma página web (ex: Chabad.org) e permite Q&A sobre o conteúdo.
10. **Leitura e Interação com PDF:** Extrai texto de arquivos PDF e permite Q&A sobre o conteúdo.
11. **Conexões da Sabedoria:** Explora relações entre diferentes conceitos judaicos.
12. **Estudo Dirigido:** Guia o estudo sobre uma Parashá ou tema geral do Judaísmo.
13. **Análise Pardes:** Apresenta os 4 níveis de interpretação de um versículo da Torá.
14. **Sabedoria dos Rebes de Chabad:** Compartilha ensinamentos e histórias dos Rebes.
15. **Halachá/Mitzvá do Dia:** Oferece uma dica prática ou inspiradora.
16. **Menu Principal:** Lista as funcionalidades disponíveis no protótipo.
17. **Mensagem de Conclusão:** Resume o protótipo e a visão de futuro.

*(As funcionalidades interativas são implementadas usando `input()` no ambiente Colab).*

## Como Usar (No Google Colab)

1.  **Obtenha uma Chave API do Google Gemini:** Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey) e crie sua chave API.
2.  **Configure o Segredo no Colab:**
    * Abra o notebook no Google Colab.
    * Na barra lateral esquerda, clique no ícone de chave (🔑) "Segredos".
    * Adicione um novo segredo com o **Nome:** `GOOGLE_API_KEY` e no campo **Valor**, cole a sua chave API.
    * Certifique-se de que "Acesso ao notebook" está LIGADO.
3.  **Carregue os Arquivos Necessários (se for usar as funcionalidades de leitura de HTML/PDF):**
    * Para a leitura de HTML, carregue o arquivo `Chabad.org em português - Torá, judaísmo e informações judaicas.htm` (ou o arquivo HTML que desejar, ajustando o nome no código).
    * Para a leitura de PDFs, carregue os arquivos PDF listados na célula correspondente (ex: `1-fonte-da-vida.pdf`, etc.) ou adicione os seus e atualize a lista no código.
4.  **Execute as Células:** Comece pela célula de instalação (`!pip install ...`) e siga a ordem das células. As células interativas pedirão seu input. Para as células de Chavruta ou Q&A com loop, digite "sair" para encerrar a interação daquela célula.

## Visão de Futuro e Colaboração

Este protótipo é um ponto de partida. A visão é que o "CHABAD - Torá com IA" possa se tornar uma plataforma robusta e acessível, enriquecida pelo vasto conteúdo e pela orientação do movimento Chabad-Lubavitch. As possibilidades incluem:

* Desenvolvimento de um aplicativo dedicado (web/mobile) com interface gráfica amigável.
* Integração direta com as bases de dados e publicações do Chabad.org.
* Recursos de personalização para acompanhar o progresso do estudo do usuário.
* Ferramentas comunitárias e de aprendizado em grupo.
* Suporte multilíngue aprimorado.

Convidamos o Chabad e outros interessados a explorar este protótipo, fornecer feedback e discutir como podemos, juntos, usar a tecnologia para difundir a luz da Torá e do Chassidut, aproximando a vinda de Mashiach.

## Contato
[Yaakov Israel]
[yaakov.ysrael@gmail.com]
