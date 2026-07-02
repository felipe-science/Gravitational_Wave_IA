# Análise de Dados de Ondas Gravitacionais

> Pipeline para triagem, tratamento, análise estatística e visualização de séries temporais de eventos de ondas gravitacionais (GWOSC).

---

## 📌 Índice

* [Sobre o Projeto](#-sobre-o-projeto)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Estrutura do Diretório Exploratory](#-diretório-exploratory)
* [Como Executar](#-como-executar)
* [Contribuição](#-contribuição)
* [Licença](#-licença)

---

## 💻 Sobre o Projeto

Este projeto foi desenvolvido para processar e analisar dados astronômicos de ondas gravitacionais. O fluxo compreende desde a filtragem de catálogos brutos de eventos até a extração de métricas físicas (como a massa final dos corpos pós-fusão) e a plotagem de gráficos de alta precisão da deformação espacial (*strain*).

---

## 🛠 Tecnologias Utilizadas

* **Python** (Linguagem principal)
* **Pandas** (Manipulação e análise de tabelas de dados)
* **NumPy** (Processamento numérico e arrays multidimensionais)
* **h5py** (Leitura e manipulação de arquivos estruturados HDF5)
* **Matplotlib** & **SciencePlots** (Geração de gráficos com qualidade científica para publicações)

---

### 📂 Diretório `Exploratory`

Esta pasta contém os scripts e análises iniciais para a triagem, tratamento e visualização dos dados do projeto.

* 📄 **`code_filter.py`**: Script responsável pela filtragem automatizada dos dados. 
  * **Entrada:** Lê os parâmetros estruturados a partir do arquivo `event-versions.csv`.
  * **Processamento:** Isola e filtra exclusivamente os eventos classificados como *confident*.
  * **Saída:** Gera o arquivo consolidado `data_gravitational_confident.csv` pronto para análise.

* 📄 **`estatística.py`**: Script responsável por extrair métricas estatísticas e validar os dados filtrados.
  * **Entrada:** Lê o arquivo consolidado `data_gravitational_confident.csv` gerado na etapa anterior.
  * **Processamento:** Calcula os valores extremos do dataset (eventos de maior e menor massa final) utilizando o Pandas e seleciona uma fatia segura de dados para amostragem.
  * **Saída:** Exibe no terminal os eventos com as massas máxima e mínima, além de uma lista de validação contendo os nomes dos eventos alocados entre as linhas 70 e 79.

* 📄 **`extracto_strain.py`**: Script responsável por extrair e visualizar a série temporal de ondas gravitacionais a partir de dados brutos.
  * **Entrada:** Lê o arquivo estruturado em formato HDF5 (ex: `H-H1_GWOSC_16KHZ_R1-1241816071-32.hdf5`), acessando diretamente o conjunto de dados em `strain/Strain`.
  * **Processamento:** Inspeciona as chaves internas do arquivo, extrai os valores de deformação espacial (*strain*) e constrói o eixo de tempo correspondente (0 a 32 segundos).
  * **Saída:** Imprime a estrutura do arquivo no terminal e gera um gráfico de alta qualidade (padrão de publicação com a biblioteca `scienceplots`), focando na janela de tempo do evento (15.5s a 16.5s).

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o Python instalado junto com as dependências do projeto:
```bash
pip install pandas numpy h5py matplotlib scienceplots