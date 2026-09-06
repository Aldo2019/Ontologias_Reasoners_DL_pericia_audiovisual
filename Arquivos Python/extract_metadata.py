#!/usr/bin/env python3
"""
extract_metadata.py

Extrai metadados técnicos de um arquivo audiovisual via ffprobe, em
formato JSON, incluindo os campos de contêiner, stream de vídeo e
probe score utilizados na análise da Seção 5 do artigo. Equivalente
em Python ao script extract_metadata.sh.

Requer ffprobe instalado e no PATH (pacote ffmpeg):
https://ffmpeg.org/download.html

Uso:
    # um único arquivo, imprime JSON no stdout
    python3 extract_metadata.py caminho/para/arquivo.mp4

    # um único arquivo, salva em arquivo
    python3 extract_metadata.py caminho/para/arquivo.mp4 -o saida.json

    # vários arquivos de uma vez (um .json por entrada, mesmo nome-base)
    python3 extract_metadata.py *.mp4 --outdir data/

    # uma pasta inteira (recursivo)
    python3 extract_metadata.py --dir caminho/da/pasta --outdir data/
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Mesmos campos extraídos pelo extract_metadata.sh original
SHOW_ENTRIES = (
    "format=format_name,probe_score,start_time,duration:"
    "stream=codec_name,r_frame_rate,avg_frame_rate,start_pts,start_time"
)

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".dav", ".hevc", ".h264", ".ts", ".flv", ".wmv"}


def run_ffprobe(input_path: Path) -> dict:
    """Executa ffprobe sobre um arquivo e retorna o JSON decodificado."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        "-show_entries", SHOW_ENTRIES,
        str(input_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        sys.exit("Erro: ffprobe não encontrado. Instale o pacote ffmpeg "
                  "(https://ffmpeg.org/download.html) e garanta que está no PATH.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Erro ao processar {input_path}: {e.stderr.strip()}")

    return json.loads(result.stdout)


def collect_inputs(files, directory):
    inputs = [Path(f) for f in files]
    if directory:
        d = Path(directory)
        inputs += sorted(p for p in d.rglob("*") if p.suffix.lower() in VIDEO_EXTENSIONS)
    return inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="Arquivo(s) de vídeo/áudio a processar")
    parser.add_argument("--dir", dest="directory", help="Processa todos os arquivos de vídeo desta pasta")
    parser.add_argument("-o", "--output", help="Caminho de saída (apenas para um único arquivo de entrada)")
    parser.add_argument("--outdir", help="Pasta de saída para múltiplos arquivos (um .json por entrada)")
    parser.add_argument("--indent", type=int, default=4, help="Indentação do JSON de saída (padrão: 4)")
    args = parser.parse_args()

    inputs = collect_inputs(args.files, args.directory)
    if not inputs:
        parser.error("Nenhum arquivo de entrada informado. Use <arquivo(s)> e/ou --dir <pasta>.")

    if len(inputs) == 1 and not args.outdir:
        metadata = run_ffprobe(inputs[0])
        text = json.dumps(metadata, indent=args.indent, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            print(f"Gravado em {args.output}")
        else:
            print(text)
        return

    outdir = Path(args.outdir) if args.outdir else Path(".")
    outdir.mkdir(parents=True, exist_ok=True)
    for path in inputs:
        metadata = run_ffprobe(path)
        out_path = outdir / f"{path.stem}.json"
        out_path.write_text(json.dumps(metadata, indent=args.indent, ensure_ascii=False), encoding="utf-8")
        print(f"{path.name} -> {out_path}")


if __name__ == "__main__":
    main()
