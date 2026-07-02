import pandas as pd
from pathlib import Path

# 1. Caminho base das pastas
path0 = Path('../data')

# 2. Lendo o CSV e aplicando .str.strip() para remover qualquer espaço ou '\r' invisível
df = pd.read_csv("data_gravitational_confident.csv")
nomes_no_csv = set(df['shortName'].astype(str).str.strip())

# 3. Listando apenas as PASTAS reais que existem dentro de ../data (ignorando arquivos soltos)
if path0.exists():
    pastas_no_pc = set(f.name for f in path0.iterdir() if f.is_dir())
else:
    print("❌ Erro: A pasta base '../data' não foi encontrada!")
    pastas_no_pc = set()

# 4. Fazendo as comparações matemáticas (usando conjuntos/sets)
baten_certinho = nomes_no_csv.intersection(pastas_no_pc)
apenas_no_csv = nomes_no_csv - pastas_no_pc
apenas_no_pc = pastas_no_pc - nomes_no_csv

# 5. Exibindo o relatório detalhado
print("📊 ================= RELATÓRIO DE COMPARAÇÃO =================")
print(f"• Total de eventos listados no seu CSV: {len(nomes_no_csv)}")
print(f"• Total de pastas físicas achadas em ../data: {len(pastas_no_pc)}")
print(f"• Eventos que batem perfeitamente (Match): {len(baten_certinho)}")
print(f"• Eventos que NÃO deram Match: {len(apenas_no_csv)}")
print("=============================================================\n")

if apenas_no_csv:
    print(f"❌ NOMES NO CSV QUE NÃO ENCONTRARAM NENHUMA PASTA CORRESPONDENTE ({len(apenas_no_csv)}):")
    # Agora mostra TODOS os que não deram match, sem esconder nada
    for name in sorted(apenas_no_csv):
        print(f"  - '{name}'")
else:
    print("✓ Todos os nomes do CSV deram match com as pastas do PC!")

print("\n-------------------------------------------------------------")

if apenas_no_pc:
    print(f"📁 PASTAS NO SEU PC QUE NÃO ESTÃO LISTADAS NO CSV ({len(apenas_no_pc)}):")
    for name in sorted(apenas_no_pc):
        print(f"  - '{name}'")
else:
    print("✓ Não existem pastas extras no seu PC (todas as pastas físicas estão no CSV).")