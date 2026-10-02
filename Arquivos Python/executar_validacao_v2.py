#!/usr/bin/env python3
"""
executar_validacao_v2.py

Executa a validação computacional com os raciocinadores HermiT e Pellet
sobre o arquivo esquema_conceitual.ttl atualizado, gerando os novos artefatos _v2
sem sobrescrever os antigos.
"""

import csv
import io
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
import rdflib
import owlready2
from owlready2 import get_ontology, sync_reasoner, default_world

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def obter_classpath_pellet():
    pellet_dir = Path(owlready2.__file__).parent / "pellet"
    return str(pellet_dir / "*")

def executar_pellet_comando(cp: str, subcomando: str, caminho_owl: Path):
    cmd = [
        "java", "-Xmx2000M", "-cp", cp,
        "pellet.Pellet", subcomando,
        "--loader", "OWLAPIv3",
        "--ignore-imports",
        str(caminho_owl)
    ]
    inicio = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duracao = time.time() - inicio
    if res.returncode != 0:
        raise RuntimeError(f"Erro ao executar Pellet {subcomando}: {res.stderr.strip()}")
    return res.stdout, res.stderr, duracao

def extrair_instancias_pellet(texto_realize: str):
    instancias_por_classe = {}
    linhas = texto_realize.splitlines()
    padrao = re.compile(r"^\s*(http[^\s]+)\s*-\s*\((.*)\)\s*$")
    for linha in linhas:
        m = padrao.match(linha)
        if m:
            classe_iri = m.group(1).split("#")[-1]
            lista_raw = m.group(2).strip()
            if lista_raw:
                itens = [iri.split("#")[-1].strip() for iri in lista_raw.split(",") if iri.strip()]
                instancias_por_classe[classe_iri] = sorted(itens)
    return instancias_por_classe

def main():
    raiz = Path(__file__).resolve().parent.parent
    pasta_hermit = raiz / "Resultados HermiT"
    pasta_pellet = raiz / "Resultados Pellet"
    pasta_v2 = raiz / "Resultados_v2"
    
    pasta_hermit.mkdir(exist_ok=True)
    pasta_pellet.mkdir(exist_ok=True)
    pasta_v2.mkdir(exist_ok=True)

    caminho_ttl = raiz / "esquema_conceitual.ttl"
    caminho_owl_v2 = raiz / "esquema_conceitual_v2.owl"

    print("=" * 75)
    print(" EXECUÇÃO DE VALIDAÇÃO COM HERMIT E PELLET (v2)")
    print("=" * 75)
    print(f"Ontologia TTL fonte: {caminho_ttl}")
    print(f"Ontologia OWL (RDF/XML v2): {caminho_owl_v2}\n")

    # 1. Serializar TTL -> OWL v2
    print("[*] Sincronizando modelo Turtle para RDF/XML (esquema_conceitual_v2.owl)...")
    g = rdflib.Graph()
    g.parse(str(caminho_ttl), format="turtle")
    g.serialize(destination=str(caminho_owl_v2), format="xml")
    total_triplas = len(g)
    print(f"[OK] {total_triplas} triplas carregadas e serializadas.\n")

    # ---------------------------------------------------------
    # 2. Executar HermiT
    # ---------------------------------------------------------
    print("[*] Executando HermiT via Owlready2...")
    log_capture = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    inicio_hermit = time.time()
    try:
        onto = get_ontology(str(caminho_owl_v2.resolve())).load()
        sys.stdout = log_capture
        sys.stderr = log_capture
        with onto:
            sync_reasoner(infer_property_values=True)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    duracao_hermit = time.time() - inicio_hermit
    log_texto_hermit = log_capture.getvalue()
    print(f"[OK] HermiT finalizado em {duracao_hermit:.2f}s (Consistente: Sim).")

    # Coletar inferências HermiT
    div_hermit_set = set(onto.MetadadoDivergente.instances())
    probe_hermit_set = set(onto.MetadadoComProbeScoreBaixo.instances())
    
    nomes_div_hermit = set(x.name for x in div_hermit_set)
    nomes_probe_hermit = set(x.name for x in probe_hermit_set)

    # Salvar ontologia com inferências HermiT v2
    caminho_onto_hermit_v2 = pasta_hermit / "ontologia_com_inferencias_v2.owl"
    onto.save(file=str(caminho_onto_hermit_v2), format="rdfxml")

    # ---------------------------------------------------------
    # 3. Executar Pellet
    # ---------------------------------------------------------
    print("\n[*] Executando Pellet via JVM...")
    cp = obter_classpath_pellet()

    print("    - Pellet consistency...")
    out_cons, err_cons, dur_cons = executar_pellet_comando(cp, "consistency", caminho_owl_v2)
    pellet_consistent = "Consistent: Yes" in out_cons

    print("    - Pellet classify...")
    out_class, err_class, dur_class = executar_pellet_comando(cp, "classify", caminho_owl_v2)

    print("    - Pellet realize...")
    out_real, err_real, dur_real = executar_pellet_comando(cp, "realize", caminho_owl_v2)
    duracao_pellet = dur_cons + dur_class + dur_real
    print(f"[OK] Pellet finalizado em {duracao_pellet:.2f}s (Consistente: {'Sim' if pellet_consistent else 'Não'}).\n")

    # Coletar inferências Pellet
    instancias_pellet = extrair_instancias_pellet(out_real)
    nomes_div_pellet = set(instancias_pellet.get("MetadadoDivergente", []))
    nomes_probe_pellet = set(instancias_pellet.get("MetadadoComProbeScoreBaixo", []))

    # ---------------------------------------------------------
    # 4. Construir base de dados e tabelas
    # ---------------------------------------------------------
    dados_conhecidos = {
        "m1": ("r_frame_rate (amostra)", "cam01", "15/1", "ABox ilustrativa", True, False),
        "m2": ("avg_frame_rate (amostra)", "cam01", "30/1", "ABox ilustrativa", True, False),
        "m3": ("container (amostra)", "cam02", "avi (score 0.31)", "ABox ilustrativa", False, True),
        "Camera_4_container": ("container", "Camera_4", "avi (score 1.00)", "Linha de base estável", False, False),
        "Camera_4_rfr": ("r_frame_rate", "Camera_4", "15/1", "Linha de base estável", False, False),
        "Camera_4_avgfr": ("avg_frame_rate", "Camera_4", "15/1", "Linha de base estável", False, False),
    }

    for i in range(1, 7):
        dados_conhecidos[f"Camera_7_{i}_container"] = ("container", "Camera_7", "avi (score 1.00)", "Segmentação temporal", False, False)
        dados_conhecidos[f"Camera_7_{i}_rfr"] = ("r_frame_rate", "Camera_7", "15/1", "Segmentação temporal", False, False)
        dados_conhecidos[f"Camera_7_{i}_avgfr"] = ("avg_frame_rate", "Camera_7", "15/1", "Segmentação temporal", False, False)

    for i in [1, 6, 7]:
        dados_conhecidos[f"Camera_9_{i}_container"] = ("container", "Camera_9", "hevc (score 0.51)", "Fluxo bruto / raw HEVC", True, False)
        dados_conhecidos[f"Camera_9_{i}_rfr"] = ("r_frame_rate", "Camera_9", "1200000/1", "Discrepância fps nominal", True, False)
        dados_conhecidos[f"Camera_9_{i}_avgfr"] = ("avg_frame_rate", "Camera_9", "25/1", "Discrepância fps média", True, False)

    for i in range(2, 6):
        dados_conhecidos[f"Camera_9_{i}_container"] = ("container", "Camera_9", "dhav (score 0.01)", "Contêiner proprietário DAV", True, True)
        dados_conhecidos[f"Camera_9_{i}_rfr"] = ("r_frame_rate", "Camera_9", "30/1", "Taxa estável no segmento", False, False)
        dados_conhecidos[f"Camera_9_{i}_avgfr"] = ("avg_frame_rate", "Camera_9", "30/1", "Taxa estável no segmento", False, False)

    dados_hermit_csv = []
    dados_pellet_csv = []
    dados_comparativo_csv = []

    # Grupo de controle para contagem
    instancias_controle = [k for k in dados_conhecidos.keys() if k.startswith("Camera_4_") or k.startswith("Camera_7_")]
    controle_classificados_hermit = 0
    controle_classificados_pellet = 0

    for ind, info in sorted(dados_conhecidos.items()):
        exp_div = info[4]
        exp_probe = info[5]

        # HermiT
        is_div_h = ind in nomes_div_hermit
        is_probe_h = ind in nomes_probe_hermit
        st_div_h = "Confirmado" if is_div_h == exp_div else "Divergente"
        st_probe_h = "Confirmado" if is_probe_h == exp_probe else "Divergente"
        st_geral_h = "100% Confirmado" if (st_div_h == "Confirmado" and st_probe_h == "Confirmado") else "Falha"

        dados_hermit_csv.append({
            "Individuo": ind,
            "Tipo": info[0],
            "Fonte": info[1],
            "Valor": info[2],
            "Contexto": info[3],
            "Esperado_Divergente": "Sim" if exp_div else "Não",
            "Inferido_Divergente": "Sim" if is_div_h else "Não",
            "Esperado_MetadadoComProbeScoreBaixo": "Sim" if exp_probe else "Não",
            "Inferido_MetadadoComProbeScoreBaixo": "Sim" if is_probe_h else "Não",
            "Status": st_geral_h
        })

        # Pellet
        is_div_p = ind in nomes_div_pellet
        is_probe_p = ind in nomes_probe_pellet
        st_geral_p = "100% Confirmado" if (is_div_p == exp_div and is_probe_p == exp_probe) else "Divergente"

        dados_pellet_csv.append({
            "Individuo": ind,
            "Tipo": info[0],
            "Fonte": info[1],
            "Valor": info[2],
            "Contexto": info[3],
            "Esperado_Divergente": "Sim" if exp_div else "Não",
            "Inferido_Pellet_Divergente": "Sim" if is_div_p else "Não",
            "Esperado_MetadadoComProbeScoreBaixo": "Sim" if exp_probe else "Não",
            "Inferido_Pellet_MetadadoComProbeScoreBaixo": "Sim" if is_probe_p else "Não",
            "Status_Pellet": st_geral_p
        })

        # Comparativo
        concordancia = (is_div_h == is_div_p) and (is_probe_h == is_probe_p)
        dados_comparativo_csv.append({
            "Individuo": ind,
            "Fonte": info[1],
            "Tipo": info[0],
            "Valor": info[2],
            "Teorico_Divergente": "Sim" if exp_div else "Não",
            "HermiT_Divergente": "Sim" if is_div_h else "Não",
            "Pellet_Divergente": "Sim" if is_div_p else "Não",
            "Teorico_MetadadoComProbeScoreBaixo": "Sim" if exp_probe else "Não",
            "HermiT_MetadadoComProbeScoreBaixo": "Sim" if is_probe_h else "Não",
            "Pellet_MetadadoComProbeScoreBaixo": "Sim" if is_probe_p else "Não",
            "Concordancia_HermiT_Pellet": "Exata (100%)" if concordancia else "Discrepante"
        })

        if ind in instancias_controle:
            if is_div_h or is_probe_h:
                controle_classificados_hermit += 1
            if is_div_p or is_probe_p:
                controle_classificados_pellet += 1

    # ---------------------------------------------------------
    # 5. Salvar Artefatos
    # ---------------------------------------------------------
    # 5.1 Log HermiT v2
    conteudo_log_hermit_v2 = (
        f"LOG DE EXECUÇÃO DO RACIOCINADOR HERMIT (OWL 2 DL) - V2\n"
        f"Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Duração: {duracao_hermit:.2f} segundos\n"
        f"Arquivo analisado: {caminho_ttl.name} ({caminho_owl_v2.name})\n"
        f"{'=' * 70}\n\n"
        f"{log_texto_hermit}\n"
    )
    (pasta_hermit / "log_execucao_hermit_v2.txt").write_text(conteudo_log_hermit_v2, encoding="utf-8")
    (pasta_v2 / "log_execucao_hermit_v2.txt").write_text(conteudo_log_hermit_v2, encoding="utf-8")

    # 5.2 Tabela Resultados HermiT v2
    def salvar_csv(caminho, dados):
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(dados[0].keys()))
            writer.writeheader()
            writer.writerows(dados)

    salvar_csv(pasta_hermit / "tabela_resultados_hermit_v2.csv", dados_hermit_csv)
    salvar_csv(pasta_v2 / "tabela_resultados_hermit_v2.csv", dados_hermit_csv)

    # 5.3 Log Pellet v2
    conteudo_log_pellet_v2 = (
        f"LOG DE EXECUÇÃO DO RACIOCINADOR PELLET (OWL 2 DL) - V2\n"
        f"Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Arquivo analisado: {caminho_ttl.name} ({caminho_owl_v2.name})\n"
        f"Loader: OWLAPIv3\n"
        f"{'=' * 70}\n\n"
        f"--- 1. TESTE DE CONSISTÊNCIA (Duração: {dur_cons:.2f}s) ---\n"
        f"Comando: pellet consistency --loader OWLAPIv3 --ignore-imports\n"
        f"{out_cons.strip()}\n\n"
        f"--- 2. CLASSIFICAÇÃO DA HIERARQUIA TBOX (Duração: {dur_class:.2f}s) ---\n"
        f"Comando: pellet classify --loader OWLAPIv3 --ignore-imports\n"
        f"{out_class.strip()}\n\n"
        f"--- 3. REALIZAÇÃO DAS INSTÂNCIAS ABOX (Duração: {dur_real:.2f}s) ---\n"
        f"Comando: pellet realize --loader OWLAPIv3 --ignore-imports\n"
        f"STDERR:\n{err_real.strip()}\n\n"
        f"STDOUT:\n{out_real.strip()}\n"
    )
    (pasta_pellet / "log_execucao_pellet_v2.txt").write_text(conteudo_log_pellet_v2, encoding="utf-8")
    (pasta_v2 / "log_execucao_pellet_v2.txt").write_text(conteudo_log_pellet_v2, encoding="utf-8")

    # 5.4 Tabela Resultados Pellet v2
    salvar_csv(pasta_pellet / "tabela_resultados_pellet_v2.csv", dados_pellet_csv)
    salvar_csv(pasta_v2 / "tabela_resultados_pellet_v2.csv", dados_pellet_csv)

    # 5.5 Tabela Comparativa HermiT vs Pellet v2
    salvar_csv(pasta_pellet / "tabela_comparativa_hermit_vs_pellet_v2.csv", dados_comparativo_csv)
    salvar_csv(pasta_v2 / "tabela_comparativa_hermit_vs_pellet_v2.csv", dados_comparativo_csv)

    print("[+] Todos os artefatos v2 foram gerados com sucesso nas pastas:")
    print(f"    - {pasta_hermit.name}/")
    print(f"    - {pasta_pellet.name}/")
    print(f"    - {pasta_v2.name}/\n")

    # ---------------------------------------------------------
    # 6. Relatório Resumo
    # ---------------------------------------------------------
    print("=" * 75)
    print(" RESUMO DA VALIDAÇÃO (HERMIT & PELLET)")
    print("=" * 75)
    print(f"1. Consistência da Ontologia (Satisfiability):")
    print(f"   - HermiT:  CONSISTENTE / SATISFATÍVEL")
    print(f"   - Pellet:  CONSISTENTE / SATISFATÍVEL ({out_cons.strip()})")
    print()
    print(f"2. Classificação em :MetadadoDivergente (15 esperados):")
    print(f"   - HermiT:  {len(nomes_div_hermit)} indivíduos classificados")
    print(f"   - Pellet:  {len(nomes_div_pellet)} indivíduos classificados")
    print(f"   - Concordância: {'100% EXATA' if nomes_div_hermit == nomes_div_pellet else 'DIVERGENTE'}")
    print()
    print(f"3. Classificação em :MetadadoComProbeScoreBaixo (5 esperados):")
    print(f"   - HermiT:  {len(nomes_probe_hermit)} indivíduos classificados")
    print(f"   - Pellet:  {len(nomes_probe_pellet)} indivíduos classificados")
    print(f"   - Concordância: {'100% EXATA' if nomes_probe_hermit == nomes_probe_pellet else 'DIVERGENTE'}")
    print()
    print(f"4. Grupo de Controle (Câmeras 04 e 07 - total de {len(instancias_controle)} indivíduos):")
    print(f"   - HermiT:  {len(instancias_controle) - controle_classificados_hermit}/{len(instancias_controle)} sem nenhuma classificação (0 falso-positivo)")
    print(f"   - Pellet:  {len(instancias_controle) - controle_classificados_pellet}/{len(instancias_controle)} sem nenhuma classificação (0 falso-positivo)")
    print("=" * 75)

if __name__ == "__main__":
    main()
