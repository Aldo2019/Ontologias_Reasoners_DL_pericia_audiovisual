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

## Sanitização e sigilo pericial

Por se tratar de metadados originados de um caso de perícia computacional real, os dados foram **sanitizados** antes da publicação: identificadores de caminho de arquivo, nomes de operador e qualquer outro campo potencialmente identificável do caso pericial subjacente foram removidos ou generalizados. Foram preservados exclusivamente os padrões técnicos objetivos (parâmetros de codificação, estrutura de contêiner, timestamps, taxas de quadro), que constituem o objeto de investigação do artigo — a estrutura do metadado, e não o conteúdo substantivo do caso.

## Estrutura do repositório


Cada arquivo `.json` corresponde à saída do `ffprobe` para uma gravação individual, no formato original de extração (streams + format).

## Uso de Inteligência Artificial

Ferramentas de IA generativa foram utilizadas como apoio à estruturação e à sanitização preliminar destes metadados. A curadoria, a definição dos critérios de sanitização e a validação final do corpus são de responsabilidade exclusiva dos autores.

## Licença

Este material é disponibilizado para fins de pesquisa e reprodutibilidade científica. [Defina aqui a licença desejada — sugestão: CC BY 4.0]

## Citação

Se utilizar este corpus, por favor cite o artigo original (referência completa acima) e este repositório.

## Contato

Aldo Faria Costa — aldofc@ufmg.br
Programa de Pós-Graduação em Gestão e Organização do Conhecimento (PPGGOC), Escola de Ciência da Informação, UFMG
