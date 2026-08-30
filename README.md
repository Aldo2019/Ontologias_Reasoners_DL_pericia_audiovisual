# Corpus de Metadados Técnicos de Proveniência Audiovisual

## Descrição

Este repositório reúne um conjunto de metadados técnicos extraídos de
gravações audiovisuais oriundas de um sistema DVR (Digital Video Recorder)
com múltiplas câmeras. Os dados foram coletados por meio da ferramenta
`ffprobe` (componente do projeto FFmpeg) e constituem o corpus empírico
utilizado em uma pesquisa sobre heterogeneidade semântica em metadados
periciais audiovisuais.

O material é disponibilizado como apoio à reprodutibilidade científica e à
avaliação por pares de um artigo submetido a periódico da área de Ciência
da Informação, em conformidade com os princípios de Ciência Aberta e as
diretrizes FAIR (Findable, Accessible, Interoperable, Reusable).

## Escopo dos dados

Os arquivos aqui reunidos documentam quatro padrões recorrentes de
heterogeneidade identificados entre fontes de captura distintas do mesmo
sistema de vigilância:

1. Divergência na identificação de contêiner multimídia
2. Discrepância entre taxa de quadros nominal e taxa de quadros efetiva
3. Redundância entre marcações temporais (*timestamps*)
4. Ausência de convenção uniforme de nomenclatura entre fontes

## Composição do corpus

14 arquivos, 3 câmeras distintas, capturados em um único dia (abril de
2024), cobrindo aproximadamente 3 horas de gravação simultânea, em dois
formatos de contêiner (AVI/H.264 e DAV proprietário/H.265).

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

**Camera_7_1.json a Camera_7_6.json** — Série de 6 arquivos de metadados técnicos (ffprobe) da Câmera 07, mesmo sistema DVR, contêiner AVI/H.264, 1280×720, 15 fps, segmentos consecutivos de ~30 min cada (1798s), cobrindo um intervalo de aproximadamente 3 horas de um mesmo dia de gravação. Identificadores de caminho, operador e caso pericial removidos; preservados apenas os parâmetros técnicos objetivos. Esta série ilustra o padrão de segmentação temporal e a convenção de nomenclatura verbosa (com timestamps de início e término) característicos desta fonte, discutidos na Seção 5.4 do artigo associado.

**Camera_9_1.json a Camera_9_7.json** — Série de 7 arquivos de metadados técnicos (ffprobe) da Câmera 09, mesmo sistema DVR, contêiner proprietário DAV (Dahua)/H.265, 1920×1080. A série ilustra os três padrões de heterogeneidade mais ricos discutidos no artigo associado: (i) divergência de identificação de contêiner — parte dos arquivos é reconhecida como `dhav` (probe_score 1) e parte como fluxo `hevc` bruto (probe_score 51); (ii) discrepância entre taxa de quadros nominal e efetiva nos arquivos "raw" (`r_frame_rate` retorna valor de timebase, não fps real); (iii) redundância e conflito entre os timestamps internos dos streams de áudio e vídeo em um mesmo arquivo (`dhav`), com defasagem de ~2 segundos entre eles. Os timestamps internos (`start_pts`/`start_time`) foram intencionalmente preservados por constituírem o objeto empírico de análise; identificadores de caminho, operador e caso pericial foram removidos.

## Sanitização e privacidade

Por razões de sigilo pericial e proteção de dados, os seguintes elementos
foram generalizados ou removidos em todos os arquivos:

- Identificadores de caso
- Caminhos de arquivo completos
- Nomes de operador do sistema de captura

A remoção desses elementos não compromete a validade da análise, uma vez
que o objeto de investigação é a estrutura do metadado técnico, e não o
conteúdo substantivo de qualquer caso pericial subjacente.

Cada arquivo `.json` corresponde à saída do `ffprobe` para uma gravação
individual, no formato original de extração (streams + format).

## Ferramenta de extração

Os dados foram extraídos com o `ffprobe`, ferramenta de linha de comando de
código aberto que integra o projeto FFmpeg, amplamente validada pela
comunidade técnica internacional para extração não invasiva de metadados
de contêiner e de fluxo multimídia.

## Uso de Inteligência Artificial

Ferramentas de IA generativa foram utilizadas como apoio à estruturação e
à sanitização preliminar destes metadados. A curadoria, a definição dos
critérios de sanitização e a validação final do corpus são de
responsabilidade exclusiva dos autores.

## Licença

Este material é disponibilizado para fins de pesquisa e reprodutibilidade
científica, sob licença CC BY 4.0.

## Como citar

*Informação de citação será adicionada após a publicação do artigo
associado a este repositório.*

## Status

Este repositório está em processo de avaliação por pares. A versão
espelhada anônima disponibilizada durante essa etapa não contém
identificação de autoria nem título do artigo associado, em conformidade
com o processo de avaliação cega adotado pelo periódico.
