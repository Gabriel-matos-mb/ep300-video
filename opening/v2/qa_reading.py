"""EP300 · V2 — QA de TEMPO DE LEITURA: em telas sem voz, todo texto precisa ficar visível >= 0,35 s/palavra + 0,9 s (cinema, tela grande, uma vez)."""
import sys; sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')
import plan
SEMVOZ = {'C00_03', 'C00_02', 'C08_01', 'C02_03'}
bad = 0
for c in plan.CUES:
    if c['id'] not in SEMVOZ: continue
    end = c['dur'] - .35
    for el in c['els']:
        txt = el.get('text') or ' '.join(el.get('lines', []) or [])
        if not txt or el['k'] in ('custom', 'exit_sign'): continue
        at = el.get('at', 0); out = el.get('out', end)
        vis = out - at - .5          # ~0,5 s de entrada
        need = .35 * len(txt.split()) + .9
        flag = '  <<< CURTO' if vis < need else ''
        if flag: bad += 1
        print(f"{c['id']} at={at:5.1f} visível≈{vis:4.1f}s precisa≈{need:3.1f}s  {txt[:60]}{flag}")
print('curtos:', bad)
