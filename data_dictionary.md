# Dicionário de dados

Descreve os campos extraídos via `ffprobe` (ver `scripts/extract_metadata.sh`) que compõem o corpus analisado no artigo (Seção 4 e 5). Identificadores de caso, nomes de operador e caminhos de arquivo foram generalizados por sigilo pericial (Seção 4).

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
