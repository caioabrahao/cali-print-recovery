from pathlib import Path
import json
import time

currentDir = Path(__file__).resolve()
REGISTRY_DIR = currentDir.parent.parent.parent.parent / "bookkeeper" / "registry"


def saveIndividualRegistry(registryData):
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    timestamp_id = int(time.time() * 1000)
    fileName = REGISTRY_DIR / f"reading_{timestamp_id}.json"

    with open(fileName, "w", encoding="utf-8") as arquivo:
        json.dump(registryData, arquivo, ensure_ascii=False, indent=4)

    print(f"Registry created at: {REGISTRY_DIR.resolve()}")
    limpar_arquivos_antigos()


def limpar_arquivos_antigos():
    arquivos = [f for f in REGISTRY_DIR.iterdir() if f.is_file()]
    arquivos.sort(key=lambda f: f.stat().st_mtime)

    while len(arquivos) > 5:
        arquivo_mais_antigo = arquivos.pop(0)
        arquivo_mais_antigo.unlink()  
