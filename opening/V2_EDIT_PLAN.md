# EP300 · Vídeo de abertura · V2 — decisões editoriais

> Deriva da V1 (que deriva da V0). Fonte técnica = `v2/plan.py`. V0 e V1 continuam intactas (`v0/`, `v1/`, `02_PROJETOS/EP300_ABERTURA_V0|V1`).
> Entrada desta rodada: feedback do Gabriel sobre a V1 (chat, 29/09) — arco cinema, cold open com reação, continuidade, safe area, SFX, história, final→looping.

## Arco (fala gravada não muda de ordem — o que mudou foi o entorno visual)
COLD OPEN humano → ANTES DA SESSÃO (para a sala) → selo EP 300 + Gustavo/Lucian → dados × acho → DE ONDE VEM (a volta do **Lucian**) →
EVOLUÇÃO DO PROGRAMA (EP 1 → hoje) → o que mudou (ferramentas/UA/GA4/IA) → o que não mudou (203×, apelidos, Pica-Pau) → 191/348/140 →
empresas/Google/PM-RJ → ficha de presença → “a gente chegou antes” → vocês/700 mil/2038/110 países/EP 197/gente → título →
300 comemorado → **vira o lockup do LOOP**.

## O que mudou na V2 (por pedido)
| Tema | Decisão |
|---|---|
| Cold open | `b0` (bastidor 24/05/2023) até 9,3 s: “Fala aí… sejam bem-vindos” / **“Começou mesmo?”** / “Começa de novo…” + os dois rindo (não corta na frase) → “Tá no ar, tá valendo” (`b3`). PB + REC. Removível (`PRESHOTS`). |
| Antes da sessão | 5 páginas faladas **para a sala** (ninguém clica): saídas p/ quem disser “eu acho” · levanta a mão · olha pro lado · celular só se marcar a gente · pipoca + “vocês vieram ao cinema assistir a um podcast”. Cada página empurra a anterior; ~4,5–5 s de leitura por página. Balde = versão corrigida do Gabriel. |
| CTA digital | Removidos: pílula “toca pra ver”, ▶, cursor, botão “play”. (O texto “alguém apertou o play” continua porque é a fala.) O selo 300 abre em íris a partir dele mesmo. |
| Continuidade | Telas cheias encostadas (ou com < 0,45 s de câmera entre elas) se **empurram**: a seguinte desliza da direita e empurra a anterior; nunca aparece câmera entre elas. Verificado por `qa_leak.py` (composição sobre magenta). |
| História | “A volta do **Lucian**” · frame real do EP 1 (YouTube `4EPVBU7WgDg`, 2021) · **Evolução do programa**: EP 1/2021, EP 73/2022, EP 100/2023 (ao vivo, com plateia), EP 153/2024, EP 210/2025, hoje — frames do arquivo histórico oficial (`00_ARQUIVO_HISTORICO`), + 2,4 s de pausa sem voz. |
| Ferramentas | Logos reais em adesivo-tile (simple-icons CC0): GA, GTM, BigQuery, Looker Studio, Power BI, Ads, Meta, Hotjar, Search Console, Google + Reportei; Amplitude = wordmark. |
| Stickers | Usados os “refeitos” do Gabriel: Guta, Lucas, Vitória (3 estados + 1), Mafê (3), Phill (4), Bonel (7), Layla (3), balde, viatura. Recortes de fundo preto (tiras Layla/Phill/Bonel) feitos por flood-fill; **rostos intocados**. Nenhum sticker novo de pessoa foi necessário. |
| Vitória | Mesma foto, **sem** “zoeira nº”: corações nos olhos (desenhados sobre o adesivo; posição dos olhos por YuNet). |
| Toddynho | Carton **original** desenhado (texto TODDYNHO + selo GA4) cai no “todinho todo”. |
| Pica-Pau | Silhueta **original** de pica-pau (“Alô, polícia?”) + viatura do Gabriel entrando + os dois olhando. Personagem protegido não usado. |
| 191 pessoas | 4 convidados históricos (Phill, Mafê, Bonel, Layla) + 2 frames reais; reações trocam a cada número (191 → 348 → 140+). Ninguém “FALTA FOTO”. |
| Setas | Removidas as da cena “vocês”; a seta da placa SAÍDA foi reposicionada (não cruza o texto). |
| Safe area | Retângulo 90/54 px: `qa_cues_v2.py --safe` percorre todas as cenas (ver relatório). |
| “acho” | Só textura nas laterais; hierarquia DADOS → 11.526 → VEZES. |
| Bandeiras | Quadradas, cantos arredondados, borda de tinta + sombra sólida (formato do site). Os 65 `.webp` originais estão no repositório do site (privado) — desenhei os 16 usados. |
| Emoji | Só com função; reação troca (🙋→😅, 📣→🙌). |
| SFX | Sintéticos macios (`sfx_v2.py`) + biblioteca MA mais baixa e com low-pass; **ducking −10 dB sob a voz**. Big numbers: “tique-taque” que acompanha o contador (fim do scratch). 300 = estouro + confete + língua de sogra (curto). |
| Final → LOOPING | `final_v2`: 300 conta → estoura (confete) → Gustavo e Lucian comemoram + “vocês estão aqui” → o 300 laranja vira o lockup do loop; mosaico, logo e patrocinadores entram. Os últimos 1,5 s são os **quadros 118,5–120 s do próprio loop**; o loop começa no quadro 0 sem corte. |

## Tempo de leitura
`qa_reading.py`: em telas sem voz, texto visível ≥ 0,35 s/palavra + 0,9 s. Ajustes: páginas do aviso ~5 s; cues com “payoff” curto ganharam +0,6–0,7 s.

## Sincronismo
Ver `SYNC_E_FEEDBACK/sync_report.json` (V2): imagem×imagem das fechadas contra a geral corrigida, começo/meio/fim — resíduos ≤ 35 ms (≈1 quadro); drift de relógio câmera×mesa sem tendência (≤ 41 ms de ruído).
