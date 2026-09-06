# Corpus Anônimo de Metadados Técnicos Audiovisuais

## Descrição

Este repositório disponibiliza um corpus de metadados técnicos extraídos de gravações audiovisuais provenientes de um sistema de gravação digital (DVR — *Digital Video Recorder*) com múltiplas câmeras.

Os dados foram obtidos por meio do `ffprobe`, componente do projeto FFmpeg, e são disponibilizados para fins de reprodutibilidade científica, transparência metodológica e avaliação por pares.

O corpus permite examinar características estruturais e padrões de heterogeneidade presentes em metadados técnicos de arquivos audiovisuais provenientes de diferentes fontes de captura.

Repositório de apoio ao artigo **"Padrões de heterogeneidade semântica em metadados de proveniência audiovisual: um esquema conceitual em lógica descritiva"** 

Este repositório reúne os materiais de apoio à pesquisa, em conformidade com os princípios de Ciência Aberta e as diretrizes FAIR (Wilkinson et al., 2016):

```
.
├── Arquivos Metadados/            # 14 arquivos JSON com os metadados técnicos extraídos do corpus (Câmeras 4, 7 e 9)
├── Arquivos Python/               # Scripts de extração, povoamento da ABox e testes de raciocinadores
├── Resultados HermiT/             # Pacote de validação com HermiT (relatório técnico, tabelas LaTeX/CSV e ontologia inferida)
├── Resultados Pellet/             # Pacote de validação com Pellet e confronto sistemático HermiT vs. Pellet
├── esquema_conceitual.ttl         # Esquema ontológico em OWL 2 DL (sintaxe Turtle)
├── esquema_conceitual.owl         # Esquema ontológico sincronizado em RDF/XML (compatível com Owlready2 e Protégé)
└── metadados_exemplo.csv          # Amostra ilustrativa da estrutura tabular do corpus
```

## Sobre a pesquisa

O artigo identifica quatro padrões recorrentes de heterogeneidade semântica em metadados técnicos de proveniência audiovisual (divergência de *contêiner*, discrepância entre taxa de quadros nominal e efetiva, redundância de *timestamps* e ausência de convenção de nomenclatura), extraídos via `ffprobe` de um corpus real oriundo de um sistema DVR multi-câmera, e propõe, a partir deles, um esquema conceitual de classes, propriedades e axiomas em Lógica Descritiva (LD), estruturalmente alinhado ao padrão PROV-O.

### Validação por Raciocinadores (HermiT e Pellet)

A proposta conceitual foi **submetida a validação computacional formal** por meio de dois raciocinadores dedutivos independentes com algoritmos distintos:
* **HermiT** (v1.4.3.456, baseado em *Hypertableau*);
* **Pellet** (v2.3.1, baseado em *Tableau standard* com suporte a OWLAPIv3).

**Resultados obtidos:**
1. **Consistência Lógica:** Ambos os raciocinadores atestaram que a ontologia é **100% consistente e satisfatível**.
2. **Concordância Inter-Reasoner:** Obteve-se **100% de equivalência** entre a predição teórica (Seção 6), as inferências do HermiT e as do Pellet:
   * 15 indivíduos classificados em `:MetadadoDivergente` (taxas nominais anômalas e divergência de contêineres hevc/dhav);
   * 5 indivíduos classificados em `:ConfiabilidadeBaixa` (`probe_score` normalizado $< 0.5$);
   * 0 falso-positivo no grupo de controle (Câmeras 04 e 07);
   * Validação empírica do caso-limite da Seção 6.4 (`probe_score` = 0.51 não classificado em baixa confiabilidade).

Os relatórios detalhados, logs de execução, tabelas em LaTeX e modelos com triplas inferidas estão disponíveis nas pastas `Resultados HermiT/` e `Resultados Pellet/`.

## Como citar

Durante o processo de avaliação por pares do artigo, o acesso a este material é fornecido por meio de espelho anonimizado, em conformidade com a política de avaliação cega do periódico.
A informação bibliográfica para citação será disponibilizada juntamente com a versão definitiva do estudo.

# Licença dos dados e da documentação

O conteúdo deste repositório (dicionário de dados, amostra de metadados, esquema ontológico e relatórios) está licenciado sob **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Texto completo da licença: https://creativecommons.org/licenses/by/4.0/deed.pt_BR

# Scripts e Ferramentas (`Arquivos Python/`)

* `extract_metadata.py`: Extração automatizada via `ffprobe` em formato JSON.
* `populate_abox.py`: Povoamento determinístico da ABox a partir dos JSONs.
* `ler_ttl.py`: Validação sintática do arquivo Turtle e conversão automática para RDF/XML.
* `test_reasoner.py` / `gerar_resultados_hermit.py`: Execução e exportação dos testes do raciocinador HermiT.
* `test_pellet.py` / `gerar_resultados_pellet.py`: Execução e exportação dos testes do raciocinador Pellet.

## Uso

Requer Python 3.10+ com `owlready2` e `rdflib`, além de Java (JVM 11+) para a execução dos raciocinadores.

# Esquema conceitual (OWL / Turtle)

`esquema_conceitual.ttl` reproduz, em sintaxe Turtle (OWL 2 DL), os axiomas discutidos na Seção 6 do artigo: as sete classes principais (Seção 6.1), as propriedades de objeto e de dado e as duas classes definidas por restrição — `MetadadoDivergente` e `ConfiabilidadeBaixa` (Seção 6.2) —, além do alinhamento a PROV-O (Seção 6.3) e da ABox expandida do corpus real.

## Como inspecionar

Abra o arquivo `esquema_conceitual.ttl` ou `esquema_conceitual.owl` diretamente no [Protégé](https://protege.stanford.edu/) para visualizar a hierarquia de classes e propriedades, ou utilize os scripts Python disponibilizados para reproduzir as inferências computacionais via linha de comando.

 Dicionário de dados

Descreve os campos extraídos via `ffprobe` (ver `extract_metadata.py`) que compõem o corpus analisado no artigo (Seção 4 e 5). Identificadores de caso, nomes de operador e caminhos de arquivo foram generalizados por sigilo pericial (Seção 4).

| Campo               | Tipo         | Descrição                                                                 | Padrão relacionado (Seção 5) |
|---------------------|--------------|----------------------------------------------------------------------------|-------------------------------|
| `source_id`         | string       | Identificador anonimizado da fonte de captura (câmera/canal DVR)          | —                              |
| `evidence_id`       | string       | Identificador anonimizado do evento/evidência                             | —                              |
| `container_reported`| string       | Formato de contêiner reportado pelo `ffprobe` (`format_name`)             | 5.1                            |
| `probe_score`       | decimal [0,1]| Métrica de confiança da identificação do contêiner                        | 5.1                            |
| `r_frame_rate`       | string       | Taxa de quadros nominal, conforme reportada no stream (`r_frame_rate`)    | 5.2                            |
| `avg_frame_rate`     | string       | Taxa de quadros média, calculada (`avg_frame_rate`)                       | 5.2                            |
| `start_time`         | decimal      | Timestamp de início reportado no metadado interno do stream               | 5.3                            |
| `start_pts`          | integer      | Presentation timestamp de início (unidades de *timebase*)                 | 5.3                            |
| `filename_timestamp`| string       | Timestamp extraído do nome do arquivo, quando presente                    | 5.3                            |
| `naming_convention` | string       | Convenção de nomenclatura observada na fonte (categorizada)               | 5.4                            |
| `codec`              | string       | Codec de vídeo identificado (`codec_name`)                                | 4                               |

## Observação sobre a amostra publicada

`metadados_exemplo.csv` contém uma amostra **ilustrativa e sintética**, com a mesma estrutura de campos do corpus real, usada apenas para demonstrar o esquema de dados. **Substitua este arquivo pelos dados sanitizados reais do corpus** (Seção 4) antes da publicação definitiva do repositório, mantendo a mesma estrutura de colunas para preservar a rastreabilidade entre o artigo, a ontologia e os dados.

## Escopo dos dados

O corpus contempla quatro padrões recorrentes de heterogeneidade identificados nos metadados analisados:

1. Divergência na identificação do contêiner multimídia;
2. Discrepância entre taxa de quadros nominal e taxa de quadros efetiva;
3. Redundância ou divergência entre marcações temporais (*timestamps*);
4. Ausência de convenção uniforme de nomenclatura entre diferentes fontes de captura.

## Composição do corpus

O corpus é composto por **14 arquivos de metadados**, correspondentes a **3 câmeras distintas**, obtidos a partir de gravações realizadas em um mesmo período temporal.

Os arquivos representam aproximadamente **3 horas de gravação**, distribuídas entre diferentes segmentos e dois grupos principais de estruturas de contêiner:

* AVI/H.264;
* DAV/H.265.

Os arquivos disponibilizados correspondem exclusivamente aos metadados técnicos extraídos, não contendo o conteúdo audiovisual original.

## Arquivos

| Arquivo           | Câmera | Contêiner  | Codec       | Resolução |             Tamanho | Padrão ilustrado                                 |
| ----------------- | -----: | ---------- | ----------- | --------- | ------------------: | ------------------------------------------------ |
| `Camera_4.json`   |     04 | AVI        | H.264       | 1280×720  |   354.054.390 bytes | Linha de base; contêiner e nomenclatura estáveis |
| `Camera_7_1.json` |     07 | AVI        | H.264       | 1280×720  |   354.144.836 bytes | Nomenclatura com informações temporais           |
| `Camera_7_2.json` |     07 | AVI        | H.264       | 1280×720  |   354.124.396 bytes | Nomenclatura com informações temporais           |
| `Camera_7_3.json` |     07 | AVI        | H.264       | 1280×720  |   354.147.456 bytes | Nomenclatura com informações temporais           |
| `Camera_7_4.json` |     07 | AVI        | H.264       | 1280×720  |   354.103.738 bytes | Nomenclatura com informações temporais           |
| `Camera_7_5.json` |     07 | AVI        | H.264       | 1280×720  |   354.200.142 bytes | Nomenclatura com informações temporais           |
| `Camera_7_6.json` |     07 | AVI        | H.264       | 1280×720  |   354.143.854 bytes | Nomenclatura com informações temporais           |
| `Camera_9_1.json` |     09 | HEVC (raw) | H.265       | 1920×1080 | 1.306.066.944 bytes | `probe_score` 51; fluxo bruto                    |
| `Camera_9_2.json` |     09 | DAV (dhav) | AAC + H.265 | 1920×1080 |   252.239.872 bytes | Defasagem temporal entre áudio e vídeo           |
| `Camera_9_3.json` |     09 | DAV (dhav) | AAC + H.265 | 1920×1080 |   252.108.800 bytes | Estrutura DAV                                    |
| `Camera_9_4.json` |     09 | DAV (dhav) | AAC + H.265 | 1920×1080 |   258.531.328 bytes | Estrutura DAV                                    |
| `Camera_9_5.json` |     09 | DAV (dhav) | AAC + H.265 | 1920×1080 |   252.960.768 bytes | Estrutura DAV                                    |
| `Camera_9_6.json` |     09 | HEVC (raw) | H.265       | 1920×1080 |   256.204.800 bytes | `probe_score` 51; `r_frame_rate` anômico         |
| `Camera_9_7.json` |     09 | HEVC (raw) | H.265       | 1920×1080 |   253.763.584 bytes | Fluxo HEVC bruto                                 |

## Descrição dos grupos

### Camera_4.json

Contém metadados técnicos de uma gravação da Câmera 04, com contêiner AVI e codec H.264, resolução de 1280×720 e taxa nominal de 15 fps. O arquivo representa aproximadamente 30 minutos de gravação.

### Camera_7_1.json a Camera_7_6.json

Conjunto de seis arquivos de metadados técnicos da Câmera 07, utilizando contêiner AVI e codec H.264, com resolução de 1280×720 e taxa nominal de 15 fps.

Os arquivos correspondem a segmentos consecutivos de aproximadamente 30 minutos, totalizando aproximadamente três horas de gravação. O conjunto permite observar padrões de segmentação temporal e de nomenclatura.

### Camera_9_1.json a Camera_9_7.json

Conjunto de sete arquivos de metadados técnicos da Câmera 09, associados a gravações utilizando H.265.

O grupo apresenta diferentes formas de identificação estrutural pelo `ffprobe`, incluindo arquivos reconhecidos como `dhav` e arquivos identificados como fluxo HEVC bruto. Também são observadas diferenças entre taxas de quadros nominais e efetivas e divergências entre marcações temporais internas dos fluxos de áudio e vídeo.

Os campos temporais internos, incluindo `start_pts` e `start_time`, foram preservados por constituírem informações relevantes para a análise dos metadados.

## Estrutura dos dados

Cada arquivo `.json` corresponde à saída do `ffprobe` para uma gravação individual e contém informações técnicas referentes aos fluxos e ao contêiner multimídia.

Os dados incluem, quando disponíveis, informações como:

* identificação do formato;
* contêiner;
* codec;
* resolução;
* taxa de quadros;
* duração;
* bitrate;
* informações de fluxo;
* parâmetros temporais;
* informações estruturais do arquivo.

Não são disponibilizados os arquivos audiovisuais originais.

## Sanitização e privacidade

Antes da disponibilização, os dados foram submetidos a procedimentos de sanitização destinados à remoção ou generalização de informações potencialmente identificadoras.

Foram removidos ou generalizados, quando presentes:

* identificadores de caso;
* caminhos completos de arquivos;
* nomes de operadores;
* informações diretamente associadas à identificação da fonte original.

Foram preservados os parâmetros técnicos necessários à compreensão e à reprodução da análise, incluindo informações estruturais dos contêineres, codecs, fluxos e marcações temporais.

A sanitização foi realizada de modo a preservar o conteúdo técnico necessário à investigação, sem disponibilizar informações que permitam identificar pessoas, casos ou fontes específicas.

## Ferramenta de extração

Os metadados foram extraídos utilizando o `ffprobe`, ferramenta de linha de comando integrante do projeto FFmpeg.

O `ffprobe` permite a inspeção não invasiva de informações relacionadas a contêineres e fluxos multimídia, possibilitando a obtenção de parâmetros técnicos sem alteração do conteúdo original analisado.

## Uso de Inteligência Artificial

Ferramentas de inteligência artificial generativa foram utilizadas como apoio à organização e à sanitização preliminar dos dados.

A definição dos critérios de sanitização, a curadoria do corpus e a validação final dos dados foram realizadas pelos pesquisadores responsáveis pelo estudo.

A utilização de ferramentas de IA não substituiu a verificação humana dos dados disponibilizados.

## Reprodutibilidade e Ciência Aberta

O corpus é disponibilizado para favorecer a transparência metodológica, a reprodutibilidade dos procedimentos analíticos e a reutilização dos dados em pesquisas relacionadas à análise de metadados audiovisuais.

Os dados foram organizados em formato estruturado (`JSON`) para facilitar sua leitura, processamento automatizado e reutilização em diferentes ambientes computacionais.

## Status

Este repositório é disponibilizado em versão anônima para fins de avaliação por pares.

A versão pública durante o processo de revisão não contém nomes de autores, afiliações institucionais, informações de contato ou outros elementos destinados à identificação dos pesquisadores responsáveis pelo estudo.
