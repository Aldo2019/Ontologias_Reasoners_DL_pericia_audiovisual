#!/usr/bin/env python3
"""
ler_ttl.py

Script para leitura, validação e carregamento de arquivos .ttl (Turtle).
Permite:
1. Fazer o parse e validação sintática via rdflib
2. Contar classes, propriedades e indivíduos
3. Exportar para RDF/XML para consumo direto pelo Owlready2 / Protégé
"""

import sys
from pathlib import Path
import rdflib

def ler_e_validar_ttl(caminho_ttl: Path):
    print(f"[*] Lendo arquivo: {caminho_ttl}")
    if not caminho_ttl.exists():
        print(f"[ERRO] Arquivo não encontrado: {caminho_ttl}")
        return None

    g = rdflib.Graph()
    try:
        g.parse(str(caminho_ttl), format="turtle")
        print(f"[SUCESSO] Sintaxe Turtle válida! Total de triplas carregadas: {len(g)}")
        return g
    except Exception as e:
        print(f"[ERRO DE SINTAXE] Não foi possível ler o arquivo Turtle:")
        print(f"    {e}")
        return None

def analisar_conteudo(g: rdflib.Graph):
    OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
    RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")

    classes = set(g.subjects(RDF.type, OWL.Class))
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    data_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    named_individuals = set(g.subjects(RDF.type, OWL.NamedIndividual))

    # Identificar instâncias tipadas (excluindo classes e propriedades)
    meta_types = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology,
                   OWL.AllDisjointClasses, OWL.AllDisjointProperties, OWL.Restriction, RDFS.Datatype}
    instancias = set()
    for s, p, o in g.triples((None, RDF.type, None)):
        if o not in meta_types and not isinstance(s, rdflib.BNode):
            instancias.add(s)

    print("\n--- Estatísticas do Grafo ---")
    print(f"Total de Triplas: {len(g)}")
    print(f"Classes OWL declaradas: {len(classes)}")
    print(f"Propriedades de Objeto: {len(obj_props)}")
    print(f"Propriedades de Dado: {len(data_props)}")
    print(f"Indivíduos/Instâncias identificados: {len(instancias)}")

def converter_para_owl_xml(g: rdflib.Graph, caminho_saida: Path):
    print(f"\n[*] Exportando ontologia para RDF/XML em: {caminho_saida}")
    g.serialize(destination=str(caminho_saida), format="xml")
    print(f"[SUCESSO] Arquivo RDF/XML gerado com sucesso ({caminho_saida.stat().st_size} bytes).")

if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent
    ttl_padrao = raiz / "esquema_conceitual.ttl"
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else ttl_padrao

    grafo = ler_e_validar_ttl(caminho)
    if grafo:
        analisar_conteudo(grafo)
        saida_owl = caminho.with_suffix(".owl")
        converter_para_owl_xml(grafo, saida_owl)
