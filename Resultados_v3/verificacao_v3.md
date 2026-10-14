# Verificação de Validação Ontológica — Execução v3

- **Arquivo analisado:** `esquema_conceitual_2.ttl`
- **SHA-256:** `7557c7225844fbb74967c6252a10259beec40c74f0bef3ce7e02123aa7acf644`
- **Data/Hora da verificação:** `2026-10-14T17:31:28.738126-03:00`
- **Ferramentas:** Python 3.13.16, Owlready2 0.51, Java java version "11.0.16.1" 2022-08-18 LTS, HermiT v1.4.3.456 (core HermiT 1.3.8.1099 em Owlready2), Pellet v2.3.1
- **Nota de anonimização:** Identificadores pessoais e caminhos absolutos foram sanitizados com `[omitido]`.

---

## 1. Tabela Comparativa (Expectativa Teórica vs. HermiT v3 vs. Pellet v3)

| Grupo | Fonte / Modo | Indivíduos | Divergente | Probe score baixo | Ambas | Nenhuma |
|---|---|---|---|---|---|---|
| Câmera 09 (7 segmentos) | Teórico | 21 | 13 | 4 | 4 | 8 |
| | HermiT v3 | 21 | 13 | 4 | 4 | 8 |
| | Pellet v3 | 21 | 13 | 4 | 4 | 8 |
| Controle: Câmeras 04 e 07 (7 arquivos) | Teórico | 21 | 0 | 0 | 0 | 21 |
| | HermiT v3 | 21 | 0 | 0 | 0 | 21 |
| | Pellet v3 | 21 | 0 | 0 | 0 | 21 |
| Amostra ilustrativa | Teórico | 3 | 2 | 1 | 0 | 0 |
| | HermiT v3 | 3 | 2 | 1 | 0 | 0 |
| | Pellet v3 | 3 | 2 | 1 | 0 | 0 |
| **Total** | **Teórico** | **45** | **15** | **5** | **4** | **29** |
| | **HermiT v3** | **45** | **15** | **5** | **4** | **29** |
| | **Pellet v3** | **45** | **15** | **5** | **4** | **29** |

*Observação metodológica:* As colunas "Divergente" e "Probe score baixo" representam a contagem total de instâncias inferidas em cada classe respectiva, incluindo os indivíduos classificados simultaneamente em ambas. O número total de indivíduos pertencentes a ao menos uma classe é 16 (15 + 5 − 4), e 29 pertencem a nenhuma.

---

## 2. Relato de Conformidade e Divergências

- **(a) Contagens obtidas por raciocinador:**
  - **HermiT v3:** 15 MetadadoDivergente, 5 MetadadoComProbeScoreBaixo, 4 em ambas, 29 em nenhuma (Total: 45/45).
  - **Pellet v3:** 15 MetadadoDivergente, 5 MetadadoComProbeScoreBaixo, 4 em ambas, 29 em nenhuma (Total: 45/45).
- **(b) HermiT = Pellet indivíduo a indivíduo:** Sim, concordância exata em 45/45 indivíduos (100% de coincidência).
- **(c) Ambos = Expectativa teórica:** Sim, concordância total e irrestrita com a matriz conceitual.
- **(d) Divergências encontradas:**
  Nenhuma divergência identificada.

---

## 3. Conclusão

1. Os raciocinadores HermiT v1.4.3.456 e Pellet v2.3.1 confirmaram que a ontologia v3 é consistente e sem classes insatisfatíveis.
2. A classificação dos 45 indivíduos de MetadadoTécnico foi 100% idêntica entre HermiT e Pellet em todas as classes analisadas.
3. Ambos os raciocinadores coincidiram perfeitamente com a expectativa teórica (15 divergentes, 5 de probe score baixo, 4 em ambas e 29 em nenhuma).
4. O grupo de controle (21 indivíduos das Câmeras 04 e 07) não gerou qualquer falso-positivo em nenhum dos dois mecanismos.
5. Conclui-se que a versão v3 atinge concordância absoluta (45/45) entre teoria e inferência computacional automatizada.
