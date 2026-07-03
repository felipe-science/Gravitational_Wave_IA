# Análise de Dados de Ondas Gravitacionais[cite: 3]

> Pipeline para triagem, tratamento, análise estatística e visualização de séries temporais de eventos de ondas gravitacionais (GWOSC).[cite: 3]

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

Este projeto foi desenvolvido para processar, analisar e visualizar dados astronômicos de ondas gravitacionais obtidos diretamente do GWOSC[cite: 2, 3]. O fluxo de trabalho foi automatizado para realizar o download de catálogos confiáveis, consolidar as versões mais recentes de cada evento gravitacional, tratar os dados nulos e gerar métricas físicas e visualizações estatísticas avançadas com qualidade de publicação científica[cite: 1, 2, 3].

---

## 🛠 Tecnologias Utilizadas

* **Python** (Linguagem principal do projeto)[cite: 3]
* **Pandas** (Manipulação, limpeza e análise estruturada das tabelas de dados)[cite: 3]
* **NumPy** (Processamento numérico e computação baseada em arrays multidimensionais)[cite: 3]
* **h5py** (Leitura e inspeção de arquivos altamente estruturados no formato HDF5)[cite: 3]
* **Matplotlib** & **SciencePlots** (Geração de gráficos customizados com formatação científica rigorosa para artigos e relatórios)[cite: 3]
* **Seaborn** (Criação de gráficos avançados de densidade de contorno e mapas de calor)
* **gwosc** (API oficial para consulta remota e download dos conjuntos de dados de ondas gravitacionais)[cite: 2]
* **tqdm** (Interface gráfica em terminal com barra de progresso para monitoramento de loops demorados)[cite: 2]

---

### 📂 Diretório `Exploratory`[cite: 3]

Esta pasta armazena os scripts executáveis que compõem as etapas de ingestão, engenharia e análise visual do pipeline[cite: 3].

* 📄 **`code_filter.py`**: Script encarregado de realizar a busca ativa, download e higienização inicial dos dados na plataforma GWOSC[cite: 2].
  * **Processamento:** Varre catálogos específicos (`GWTC-1-confident`, `GWTC-2.1-confident`, `GWTC-3-confident`, `GWTC-4.1`, `GWTC-5.0` e `O4_Discovery_Papers`) em busca de eventos[cite: 2]. Utiliza expressões regulares para mapear os sufixos de versão (ex: `GW150914-v4`), garantindo que apenas a revisão mais recente e atualizada de cada evento seja mantida no dicionário consolidado[cite: 2].
  * **Saída:** Escreve um arquivo bruto unificado chamado `gw_events.csv`[cite: 2]. Em seguida, remove registros inconsistentes que apresentem campos nulos (`dropna()`) e exporta uma base limpa chamada `gw_filtered_events.csv`[cite: 2].

* 📄 **`estatística.py`**: Script responsável pelo motor de análise descritiva e pela renderização dos gráficos analíticos.
  * **Entrada:** Consome a base de dados tratada `gw_filtered_events.csv`[cite: 1].
  * **Processamento:** Localiza os índices extremos do dataset para identificar os eventos espaciais com a maior e a menor massa final registrada (`final_mass_source`)[cite: 1]. Calcula parâmetros matemáticos essenciais como médias ($\mu$) e desvios padrão ($\sigma$) para massas, spins e distâncias[cite: 1].
  * **Saída:** Exibe no terminal os nomes dos eventos correspondentes às massas máximas e mínimas[cite: 1]. Gera e salva de forma automatizada seis visualizações de alta resolução na pasta `img/`[cite: 1]:
    * `mass1_x_mass2.png`: Gráfico de dispersão correlacionando as massas dos corpos primários ($m_1$) e secundários ($m_2$) em comparação com a linha de referência ideal $y = x$[cite: 1].
    * `distance_mass.png`: Dispersão correlacionando a Distância de Luminosidade (Mpc) com a Massa Final da Fonte ($M_\odot$)[cite: 1].
    * `join_q_chi_eff.png`: Gráfico de densidade de contorno bidimensional (KDE) mapeando a distribuição conjunta entre o Spin Efetivo ($\chi_{eff}$) e a Razão de Massa ($q$) através da paleta de cores *mako*[cite: 1].
    * `FinalMass.png`: Histograma de distribuição da Massa Final contendo legendas dinâmicas da média ($\mu$) e desvio padrão ($\sigma$) calculados[cite: 1].
    * `Mass1Mass2.png`: Histograma comparativo e sobreposto detalhando o comportamento amostral das frequências de $m_1$ e $m_2$ simultaneamente[cite: 1].
    * `Spin.png`: Histograma da frequência de distribuição associada aos spins efetivos dos sistemas binários[cite: 1].

* 📄 **`extracto_strain.py`**: Script focado na extração física e no isolamento de séries temporais a partir de dados brutos de sensores[cite: 3].
  * **Entrada:** Abre e mapeia arquivos estruturados em formato binário HDF5 (como `H-H1_GWOSC_16KHZ_R1-1241816071-32.hdf5`), acessando as séries temporais sob o caminho `strain/Strain`[cite: 3].
  * **Processamento:** Mapeia os metadados internos do arquivo e projeta o vetor temporal calibrado em segundos[cite: 3].
  * **Saída:** Imprime a estrutura de chaves internas do arquivo HDF5 e exporta um gráfico focalizado na janela temporal do evento (entre os segundos 15.5 e 16.5)[cite: 3].

---

## 🚀 Como Executar[cite: 3]

### Pré-requisitos[cite: 3]
Certifique-se de possuir o ambiente Python configurado localmente. Instale todas as dependências e bibliotecas externas necessárias executando o comando abaixo no terminal[cite: 1, 2, 3]:

```bash
pip install pandas numpy h5py matplotlib scienceplots seaborn gwosc tqdm