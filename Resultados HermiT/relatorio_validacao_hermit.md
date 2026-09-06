# Relatório de Validação Computacional com Raciocinador HermiT (OWL 2 DL)

**Pesquisa:** Padrões de heterogeneidade semântica em metadados de proveniência audiovisual: um esquema conceitual em lógica descritiva  
**Data do Teste:** 2026-09-06 17:56:45  
**Raciocinador:** HermiT v1.4.3.456 (integrado via Owlready2 v0.51 sobre Java OpenJDK 11 LTS)  
**Arquivo Fonte:** `esquema_conceitual.ttl` / `esquema_conceitual.owl`  

---

## 1. Contexto Metodológico e Objetivos

O esquema conceitual proposto na Seção 6 do artigo modela a heterogeneidade semântica de metadados técnicos de proveniência audiovisual extraídos de sistemas DVR multi-câmera.

O objetivo deste procedimento de validação computacional é:
1. **Verificar a Consistência Lógica:** Comprovar a ausência de contradições nos axiomas TBox e asserções ABox sob a semântica de OWL 2 DL.
2. **Avaliar a Computabilidade das Classes por Restrição:** Demonstrar que os raciocinadores dedutivos classificam automaticamente as instâncias nas classes [:MetadadoDivergente](file:///d:/Mestrado/ECI/Brajis/Ontologias_Reasoners_DL_pericia_audiovisual/esquema_conceitual.ttl#L130) e [:ConfiabilidadeBaixa](file:///d:/Mestrado/ECI/Brajis/Ontologias_Reasoners_DL_pericia_audiovisual/esquema_conceitual.ttl#L144), validando a formalização matemática descrita nas Seções 6.1 e 6.2 do artigo.
3. **Comprovar o Isolamento do Grupo de Controle:** Demonstrar que fontes sem heterogeneidade (Câmeras 04 e 07) não geram falsos positivos de inconsistência ou divergência.

---

## 2. Ambiente e Configuração Experimental

* **Linguagem / Framework:** Python 3.13 com biblioteca `owlready2` (v0.51) e `rdflib` (v7.6.0).
* **Motor de Raciocínio:** HermiT (Tableau algorithm para OWL 2 DL).
* **JVM:** OpenJDK 64-Bit Server VM (build 11.0.16.1+1-LTS-1).
* **Tempo de Execução do HermiT:** 3.15 segundos.
* **Status de Consistência:** **Consistente** (Ontology is Satisfiable).

---

## 3. Síntese dos Resultados da Classificação

| Classe por Restrição (OWL 2 DL) | Definição Formal | Previsto no Artigo | Inferido pelo HermiT | Concordância |
| :--- | :--- | :---: | :---: | :---: |
| **MetadadoDivergente** | $\text{MetadadoTecnico} \sqcap \exists \text{correlacionaComDivergencia}.\text{MetadadoTecnico}$ | 15 instâncias | 15 instâncias | **100% (Exato)** |
| **ConfiabilidadeBaixa** | $\text{MetadadoTecnico} \sqcap \exists \text{temGrauDeConfianca}.(\text{xsd:decimal}[< 0.5])$ | 5 instâncias | 5 instâncias | **100% (Exato)** |
| **Controle (Câmeras 04 e 07)** | N/A (fontes sem anomalias) | 0 divergências | 0 divergências | **100% (Sem falsos positivos)** |

---

## 4. Análise dos Padrões de Heterogeneidade Validados

### 4.1. Divergência de Taxa de Quadros (FPS Nominal vs. Efetivo)
* **Axioma:** Os indivíduos de `r_frame_rate` (1.200.000 fps) e `avg_frame_rate` (25 fps) da Câmera 09 foram correlacionados com `:correlacionaComDivergencia`.
* **Inferência do HermiT:** Todas as 6 instâncias (`Camera_9_1_rfr`, `Camera_9_1_avgfr`, `Camera_9_6_rfr`, `Camera_9_6_avgfr`, `Camera_9_7_rfr`, `Camera_9_7_avgfr`) foram subsumidas automaticamente em `:MetadadoDivergente`.

### 4.2. Divergência de Identificação de Contêiner
* **Axioma:** Segmentos da Câmera 09 identificados como fluxo bruto (`hevc`) e contêiner proprietário (`dhav`) receberam relações de divergência cruzada.
* **Inferência do HermiT:** Todos os 7 indivíduos de contêiner da Câmera 09 foram classificados em `:MetadadoDivergente`.

### 4.3. Grau de Confiança e Caso-Limite (Threshold 0.5)
* Os contêineres `dhav` (`Camera_9_2_container` a `Camera_9_5_container`) com `probe_score` 0.01 foram classificados com sucesso em `:ConfiabilidadeBaixa`.
* **Caso-Limite Confirmado:** Os segmentos `Camera_9_1`, `Camera_9_6` e `Camera_9_7` possuem `probe_score` normalizado de **0.51**. Conforme a teoria de restrição de datatypes em Lógica Descritiva, $0.51 \not< 0.5$, de modo que o raciocinador **NÃO** os classificou como `:ConfiabilidadeBaixa`. Isso valida empiricamente a discussão da Seção 6.4 do artigo sobre a calibração do limiar.

---

## 5. Relação de Arquivos Deste Pacote

1. `relatorio_validacao_hermit.md`: Este relatório com os fundamentos e resultados analíticos.
2. `tabela_artigo.tex`: Tabela formatada em LaTeX para inclusão direta no manuscrito.
3. `tabela_resultados_hermit.csv`: Planilha completa contendo todos os 45 indivíduos analisados e seus status.
4. `log_execucao_hermit.txt`: Log verbatim da saída do console e JVM com a execução do HermiT.
5. `ontologia_com_inferencias.owl`: Modelo OWL salvo contendo as triplas inferidas pelo raciocinador (compatível com o Protégé).
