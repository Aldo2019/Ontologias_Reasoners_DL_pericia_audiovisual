# Relatório de Validação com Raciocinador Pellet (OWL 2 DL) e Confronto Sistemático

**Pesquisa:** Padrões de heterogeneidade semântica em metadados de proveniência audiovisual: um esquema conceitual em lógica descritiva  
**Data da Execução:** 2026-09-06 18:01:23  
**Raciocinador:** Pellet v2.3.1 (via JVM com carregador OWLAPIv3)  
**Raciocinador Comparativo:** HermiT v1.4.3.456  
**Arquivo Fonte:** `esquema_conceitual.ttl` / `esquema_conceitual.owl`  

---

## 1. Destaque Metodológico: Validação Cruzada por Raciocinadores Independentes

Na Engenharia de Ontologias e Lógicas Descritivas, a validação por um único raciocinador pode estar sujeita a peculiaridades de implementação ou heurísticas internas. A utilização de **dois raciocinadores com arquiteturas e algoritmos distintos** (HermiT baseado em *Hypertableau* e Pellet baseado em *Tableau* padrão com *OWLAPIv3*) constitui a forma mais robusta de validação formal.

### Síntese Comparativa Geral

| Métrica / Critério | HermiT | Pellet | Status / Concordância |
| :--- | :---: | :---: | :---: |
| **Algoritmo Subjacente** | Hypertableau | Tableau (standard DL) | Complementares |
| **Status de Consistência** | Consistente | **Consistent: Yes** | **100% de Concordância** |
| **Tempo de Execução** | 3.15s | ~0.85s (realize) | Ambos em tempo interativo |
| **Instâncias em :MetadadoDivergente** | 15 | 15 | **100% de Equivalência** |
| **Instâncias em :ConfiabilidadeBaixa** | 5 | 5 | **100% de Equivalência** |
| **Grupo de Controle (Câmeras 04 e 07)** | 0 anomalias | 0 anomalias | **100% de Precisão (0 falsos-positivos)** |
| **Caso-Limite (probe_score = 0.51)** | Não classificado | Não classificado | **Comportamento Idêntico ($0.51 \not< 0.5$)** |

---

## 2. Detalhamento das Inferências do Pellet

### 2.1. Hierarquia TBox Subsumida (`pellet classify`)
O Pellet calculou e formalizou a hierarquia de classes, confirmando que:
```
owl:Thing
└── MetadadoTecnico
    ├── ConfiabilidadeBaixa  (subclasse definida por restrição)
    └── MetadadoDivergente   (subclasse definida por restrição)
```

### 2.2. Realização da ABox (`pellet realize`)
* **:MetadadoDivergente (15 indivíduos)**:
  * Amostra preliminar: `m1`, `m2`;
  * Discrepâncias de taxa de quadros (1.200.000 fps nominal vs 25 fps média): `Camera_9_1_rfr`, `Camera_9_1_avgfr`, `Camera_9_6_rfr`, `Camera_9_6_avgfr`, `Camera_9_7_rfr`, `Camera_9_7_avgfr`;
  * Divergência na identificação do contêiner (`hevc` vs `dhav` na mesma câmera): todos os 7 segmentos de contêiner da Câmera 09.
* **:ConfiabilidadeBaixa (5 indivíduos)**:
  * Amostra preliminar: `m3` (score 0.31);
  * Contêineres proprietários `dhav` com probe_score normalizado de 0.01: `Camera_9_2_container`, `Camera_9_3_container`, `Camera_9_4_container`, `Camera_9_5_container`.

---

## 3. Relação de Arquivos na Pasta `Resultados Reasoner Pellet`

1. `relatorio_validacao_pellet.md`: Este relatório metodológico.
2. `tabela_comparativa_hermit_vs_pellet.tex`: Tabela LaTeX em formato publication-ready comparando HermiT e Pellet lado a lado.
3. `tabela_comparativa_hermit_vs_pellet.csv`: Planilha completa com o confronto dos 45 indivíduos sob os dois raciocinadores.
4. `tabela_artigo_pellet.tex`: Tabela LaTeX dos resultados exclusivos do Pellet.
5. `tabela_resultados_pellet.csv`: Dados tabulares completos da execução do Pellet.
6. `log_execucao_pellet.txt`: Registro do console com as chamadas de consistência, classificação e realização.
