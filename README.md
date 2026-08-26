# Ontologias e Reasoners em Description Logics aplicados à Perícia Audiovisual — Corpus de Metadados

Este repositório disponibiliza, em conformidade com os princípios de Ciência Aberta, o corpus de metadados técnicos que fundamenta a análise empírica apresentada no artigo:

> COSTA, Aldo Faria; ALMEIDA, Maurício Barcellos. Ontologias e Reasoners em Description Logics aplicados à representação formal de metadados de proveniência em perícia audiovisual: implicações para a prova de autoria e cadeia de custódia digital. *RDBCI: Revista Digital de Biblioteconomia e Ciência da Informação* (submetido, 2026).

## Sobre o corpus

Os arquivos JSON contidos neste repositório correspondem a metadados técnicos extraídos via **ffprobe** (componente do projeto FFmpeg) a partir de gravações reais de um sistema DVR multi-câmera, utilizados como base empírica para a identificação dos quatro padrões de heterogeneidade semântica discutidos na Seção 5 do artigo:

1. Divergência na identificação de contêiner e confiabilidade do parser
2. Discrepância entre taxa de quadros nominal e taxa de quadros efetiva
3. Redundância e potencial conflito entre timestamps
4. Ausência de convenção uniforme de nomenclatura entre fontes

**Composição do corpus:** 14 arquivos, 3 câmeras distintas, capturados em um único dia (24/04/2024), cobrindo aproximadamente 3 horas de gravação simultânea, em dois formatos de contêiner (AVI/H.264 e DAV proprietário/H.265).

## Arquivos

| Arquivo | Câmera | Contêiner | Codec | Resolução | Tamanho | Padrão(ões) ilustrado(s) |
|---|---|---|---|---|---|---|
| `Camera_4.json` | 04 | AVI | H.264 | 1280×720 | 354.054.390 bytes | — (linha de base, contêiner/nomenclatura estáveis) |
| `Camera_7_1.json` | 07 | AVI | H.264 | 1280×720 | 354.144.836 bytes | 5.4 — nomenclatura verbosa (início+fim) |
| `Camera_7_2.json` | 07 | AVI | H.264 | 1280×720 | 354.124.396 bytes | 5.4 |
| `Camera_7_3.json` | 07 | AVI | H.264 | 1280×720 | 354.147.456 bytes | 5.4 |
| `Camera_7_4.json` | 07 | AVI | H.264 | 1280×720 | 354.103.738 bytes | 5.4 |
| `Camera_7_5.json` | 07 | AVI | H.264 | 1280×720 | 354.200.142 bytes | 5.4 |
| `Camera_7_6.json` | 07 | AVI | H.264 | 1280×720 | 354.143.854 bytes | 5.4 |
| `Camera_9_1.json` | 09 | HEVC (raw) | H.265 | 1920×1080 | 1.306.066.944 bytes | 5.1 — probe_score 51, fluxo bruto |
| `Camera_9_2.json` | 09 | DAV (dhav) | AAC+H.265 | 1920×1080 | 252.239.872 bytes | 5.3 — gap de ~2s áudio/vídeo |
| `Camera_9_3.json` | 09 | DAV (dhav) | AAC+H.265 | 1920×1080 | 252.108.800 bytes | 5.3 |
| `Camera_9_4.json` | 09 | DAV (dhav) | AAC+H.265 | 1920×1080 | 258.531.328 bytes | 5.3 |
| `Camera_9_5.json` | 09 | DAV (dhav) | AAC+H.265 | 1920×1080 | 252.960.768 bytes | 5.3 |
| `Camera_9_6.json` | 09 | HEVC (raw) | H.265 | 1920×1080 | 256.204.800 bytes | 5.1, 5.2 — probe_score 51, `r_frame_rate` anômalo |
| `Camera_9_7.json` | 09 | HEVC (raw) | H.265 | 1920×1080 | 253.763.584 bytes | 5.1, 5.2 |

### Descrição por grupo

**Camera_4.json** — Metadados técnicos (ffprobe) de gravação da Câmera 04, contêiner AVI/H.264, 1280×720, 15 fps, ~30 min de duração (1798s). Identificadores de caminho, operador e caso pericial removidos; preservados apenas os parâmetros técnicos objetivos de codificação e estrutura de contêiner.

**Camera_7_1.json a Camera_7_6.json** — Série de 6 arquivos de metadados técnicos (ffprobe) da Câmera 07, mesmo sistema DVR, contêiner AVI/H.264, 1280×720, 15 fps, segmentos consecutivos de ~30 min cada (1798s), cobrindo o intervalo de aproximadamente 12h30 às 15h30 de um mesmo dia de gravação. Identificadores de caminho, operador e caso pericial removidos; preservados apenas os parâmetros técnicos objetivos. Esta série ilustra o padrão de segmentação temporal e a convenção de nomenclatura verbosa (com timestamps de início e término) característicos desta fonte, discutidos na Seção 5.4 do artigo.

**Camera_9_1.json a Camera_9_7.json** — Série de 7 arquivos de metadados técnicos (ffprobe) da Câmera 09, mesmo sistema DVR, contêiner proprietário DAV (Dahua)/H.265, 1920×1080. A série ilustra os três padrões de heterogeneidade mais ricos discutidos no artigo: (i) divergência de identificação de contêiner — parte dos arquivos é reconhecida como `dhav` (probe_score 1) e parte como fluxo `hevc` bruto (probe_score 51); (ii) discrepância entre taxa de quadros nominal e efetiva nos arquivos "raw" (`r_frame_rate` retorna valor de timebase, não fps real); (iii) redundância e conflito entre os timestamps internos dos streams de áudio e vídeo em um mesmo arquivo (`dhav`), com defasagem de ~2 segundos entre eles. Os timestamps internos (`start_pts`/`start_time`) foram intencionalmente preservados por constituírem o objeto empírico de análise (Seção 5.3); identificadores de caminho, operador e caso pericial foram removidos.

## Sanitização e sigilo pericial

Por se tratar de metadados originados de um caso de perícia computacional real, os dados foram **sanitizados** antes da publicação: identificadores de caminho de arquivo, nomes de operador e qualquer outro campo potencialmente identificável do caso pericial subjacente foram removidos ou generalizados (campo `filename` reduzido a `Camera_N` ou `Camera_N_M`). Foram preservados exclusivamente os padrões técnicos objetivos (parâmetros de codificação, estrutura de contêiner, timestamps internos de stream, taxas de quadro), que constituem o objeto de investigação do artigo — a estrutura do metadado, e não o conteúdo substantivo do caso. Os timestamps Unix internos (`start_pts`/`start_time`) foram mantidos por serem o próprio objeto empírico do Padrão 5.3; eles revelam apenas a data/hora de captura já divulgada abertamente na Seção 4 do artigo (24/04/2024, ~12h26–15h30), sem identificar caso, operador ou local.

## Estrutura do repositório


Cada arquivo `.json` corresponde à saída do `ffprobe` para uma gravação individual, no formato original de extração (streams + format).

## Uso de Inteligência Artificial

Ferramentas de IA generativa foram utilizadas como apoio à estruturação e à sanitização preliminar destes metadados. A curadoria, a definição dos critérios de sanitização e a validação final do corpus são de responsabilidade exclusiva dos autores.

## Licença

Este material é disponibilizado para fins de pesquisa e reprodutibilidade científica. [Licença CC BY 4.0]

## Citação

Se utilizar este corpus, por favor cite o artigo original (referência completa acima) e este repositório.

## Contato

Aldo Faria Costa — aldofc@ufmg.br
Programa de Pós-Graduação em Gestão e Organização do Conhecimento (PPGGOC), Escola de Ciência da Informação, UFMG
