# EP300 — Delta V3 → V4

> 2026-10-02. Base: `EP300_V4_EDITORIAL_MAP.md` (IDs de beat). "V3" = remap do preflight sobre assets da V2 (nenhuma V3 renderizada).
> **49 beats: KEEP 23 · ADAPT 15 · DROP 6 · NEW 5.** Dos 44 beats vindos da V2, **38 sobrevivem (86%)**; 6 caem.

## KEEP (23) — sem retrabalho de conteúdo
- A1 cold open arquivo (C00_00) · A2 contagem (C00_01) · A3 aviso (C00_03) · A4 tela EP 300 (C00_02, sem Kinoplex)
- C1 300 perguntas (C02_02) · C3 ferramentas + ATÉ HOJE (C03_01) · C4 UA desligou (C03_02) · C5 153 / 4 em 10 (C03_03) · C7 de nada Vitória (C03_04, reordenado) · C10 botão → modelo (C03_08)
- D4 diamante negro (C04_04) · D5 gritem (C04_05) · D6 Pica-Pau (C04_06) · D8 setores/Google (C05_02) · D10 PM RJ (C05_04) · D11 ficha de presença (C05_05)
- E1 acerta antes (C06_01) · E3 todinho / MMM (C06_03)
- F1 vocês (C07_01) · F3 2038 (C07_03) · F5 EP 197 (C07_05) · F6 gente (C07_06)
- G4 final 300 / loop (C09_01) — só recalcular início

## ADAPT (15)
**Dado mudou → re-render do overlay (7):**
- C6 GA4 1/3 → **3/10** (C03_05)
- C9 IA 1/4 → **metade**; pills ATRIBUIÇÃO + INCREMENTALIDADE; **4 em 10** (C03_07)
- D1 203 → **+200** (C04_01)
- D3 16 → **60+** (C04_03)
- D7 191/348/140 → **quase 200 / quase 350 / 140+** (C05_01)
- F2 106 mil h → **100+ mil h** (C07_02)
- F4 110 países → **+100** (C07_04)

**Texto/estrutura mudou, dado não (8):**
- B1 abertura: confete ancorado em "…episódio 300", take 42.5 (C01_01)
- B4 origem: respaçar nós, ~28 s de fala (C02_01)
- C2 pausa sem voz de 2,4 s (C02_03)
- D9 "Queria": um sticker só (C05_03)
- E5 Meridian/MCP: remover Layla (C06_05)
- E6 dez/24: rótulo revisado; a piada é o beat (C06_06)
- E7 fev/26: "IMPOSSÍVEL" → "não dava pra fazer"; sem "IA NA HOME DO GA" (C06_07)
- G2 título após "futuro da mensuração", tempo recalculado (C08_01)

## DROP (6)
- B2 dados × "acho" (C01_02) — removido do roteiro e da fala
- B3 494 vezes (C01_03) — idem
- C8 "gosto pouco" (C03_06) — fala nova inverte o sentido
- D2 episódio de origem (C04_02) — não falado
- E2 bleep do palavrão do Lucian (C06_02) — sem palavrão equivalente
- E4 "de nada, Purple" + Guta/Lucas (C06_04) — **provisório (DROP\*)**: ouvir 412.3–413.6; se for "Purple", vira ADAPT

## NEW (5)
- B5 gancho "cenário antigo / MesaCast" (70.9–74.8) — opcional; **localizar** frame histórico, não criar
- F7 "Acredita? / Acredito, cara." (532.4–534.0) — reação de câmera, sem insert
- G1 "hard/soft skill… empresas são feitas de pessoas" (580.9–591.0) — opcional, sem insert
- G3 "Mas isso eu espero que a gente resolva agora. Um episódio pra pôr tudo." (603.6–607.0) — ponte, sem insert
- K1 Kinoplex — **BLOCKED**, sem posição/rótulo/tratamento

## Fora da contagem (mudanças que não são beat)
- **Ordem:** só uma troca — "de nada, Vitória" (C7) passa a vir **depois** do GA4 (C6).
- **EDL:** emenda D6→D7 (273.8–279.0 + 334.8) substitui o 316.5–326.5 do preflight (gagueira "de mais de 40").
- **Ponte nova na EDL:** 161.5–165.0 ("o que mudou foi o que entrou do lado do GA4") não estava mapeada.
- **Duração de fala:** ≈ 5:00 (V2 ≈ 7:24) + pausas.
- **Assets novos criados:** 0. Overlays a re-renderizar: 7 por dado + 8 por texto = até 15 (os mesmos 15 ADAPT; nem todos exigem render novo — E6/G2/G4 só re-âncora).
