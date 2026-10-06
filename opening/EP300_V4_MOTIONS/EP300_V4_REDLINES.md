> **SUPERADO em 03/10/2026 pelo registro das 26 imagens em `../EP300_CHAT_CLEAR_HANDOFF.md` §4** (cópias em `redlines_source/`). Mantido só como transcrição histórica; onde divergir, vale o handoff. Ex.: o balde foi trocado (A aplicado) e o Pica-Pau novo é asset do Gabriel (`USER_CONFIRMED_ASSET_EXISTS / FILE_NOT_LOCATED`), não "falta asset".

# EP300 V4 — Redlines do Gabriel (prints anotados) e estado de cada um

> 02/10/2026. Autoridade: 1) sequência Premiere atual · 2) anotações do Gabriel nos prints · 3) decisões aprovadas · 4) mapas antigos. Anotação nova vence.
> Status: **APLICADO** (está no preview) · **PREPARADO** (slot/prop pronto, falta asset) · **PENDENTE** (precisa decisão ou asset — ver pergunta no fim).

## Lote 1 — slots (previews já assistidos)
| Slot | Anotação | Status |
|---|---|---|
| S01 | polaroid EP1: "não usar esse take… tirar!!!!" | APLICADO (polaroid removida) |
| S01 | "não usar esse emoji de hover pra dar ideia de susto. Trocar…" | APLICADO (Lucian `still`) |
| S05 | "modelo." → estilo sticker | APLICADO |
| S07 | print do EP1 "pose horrível. Ajustar por outro" | APLICADO (outro frame do mesmo clipe EP1, 2,0 s) |
| S08 | "troca a frase para: já paga até boleto" | APLICADO |
| S09 | "o certo é Toddynho" · carton → sticker Toddynho | APLICADO (grafia + `stickers/toddynho.png` fornecido por você, substituível pela prop `toddynhoSrc`) |
| S10 | globo "emojis sempre estilo sticker" | APLICADO |

## Lote 2 — pré-sessão (V2 proxy)
| Tela | Anotação | Status |
|---|---|---|
| Cold open | "TIRAR ESSE TAKE DO VÍDEO FINAL!!!! NÃO USAR ESSE" + (msg) manter **só** Lucian "começou? começa de novo" + risada, **sem** "tá no ar, tá valendo", sem 2º erro | APLICADO no assembly (clipe de arquivo cortado em 4,15–6,50 s: "Começou mesmo? Começou mesmo? Começa de novo aqui." + risada). **Suposição:** colocado depois da tela do 300, antes da fala — mover se quiser outro lugar |
| Contagem 3-2-1 | "visualmente amadora" | APLICADO — `P01-CONTAGEM` redesenhada (anel + ticks + numeral sticker laranja) |
| Aviso p.1 | "o vídeo final deve começar por aqui" · seta invertida: `← SAÍDA 🏃` / `🏃 SAÍDA →` | APLICADO (vídeo = contagem → aviso; sem cold open antes) |
| Aviso p.2 | "emoji cortando… transformar em sticker e validar qualidade (baixa resolução)" (🙋 e 😅) | APLICADO (emoji vetorial, contorno sticker, inteiro; 🙋 sai quando entra 😅) |
| Aviso p.1/3/4/5 | "se você falar" → Se · "você não está sozinho" → Você · "só vamos reclamar" → Só · "vocês vieram" → Vocês | APLICADO |
| Aviso p.4 | "trocar esse sticker: Gustavo sorrindo ou boca aberta" | APLICADO (`gustavo-hover-transicao`: sorrindo, boca aberta) |
| Aviso p.5 | "a gente trocou esse balde, tentar trocar imagem…" | PREPARADO — placeholder `BALDE_NEEDS_NEW_IMAGE` (prop `bucketSrc`); não achei a imagem atual do balde/saco (as pastas `desatualizado` estão marcadas como desatualizadas) |
| Tela do 300 | tirar rostos repetidos (sobra o do selo) · alinhar texto+caixa, maiúsculo · "alinhar ao centro as logos e infos; MB como realização e Kino como apoiador" · estrutura da tela final | APLICADO (`P03-TELA-300`: selo central, pill centralizada "A sessão vai começar", PATROCÍNIO OFICIAL · CAFÉ OFICIAL · REALIZAÇÃO · APOIADOR). Kinoplex = `brand/logo_kinoplex_original.png`, **branca, original, sem sticker** |
| "Vocês estão aqui e contando" | "não faz sentido… conexão melhor com o tema" · "tela final funciona melhor que a inicial" | APLICADO como proposta — `F01-FINAL-300` (300 sobe, "300 episódios, 300 perguntas…" / "e a de hoje começa agora.", logos). **Texto é prop**: alternativas "a pergunta continua." · "300 respostas. Falta a pergunta." |

## Lote 3 — telas V2 que NÃO são slot na sua timeline (câmera ativa ali)
Nenhuma está desativada na sequência de 5:15, então não existe lugar definido para elas. **Não construí** — anotações guardadas:
| Tela V2 | Anotação | Falta |
|---|---|---|
| Evolução (a pergunta foi mudando) | EP1: "trocar print por outro melhor" · EP100: "outro com luz melhor" · EP210: "outro melhor, sem o CTA embaixo" · EP153: "trocar print (Gustavo em pose ruim)" | 4 frames novos do acervo + posição |
| Ferramentas (C03_01) | "a logo da Reportei não segue o mesmo padrão. Ajustar" | tile branco com ícone da Reportei (só tenho o wordmark) + posição |
| Bordão 203× | "tentar colocar mais prints (sensação de muitas vezes), com reações boas · prints de cenários diferentes · evitar EP288 (outro estúdio em SP)" | frames do acervo + decisão de usar supercut |
| 16 apelidos | "se essa tela ficar… trocar emoji" (rosto lateral do Lucian) | decisão se a tela fica |
| Pica-Pau 24× | "colocar novo sticker do Pica-Pau" | sticker (personagem protegido: você fornece) |
| 191 pessoas | "mais sticker e/ou mais prints — sensação de muita gente, não de ranking" · "EP187 convidado remoto: BANIDO" | stickers/frames + decisão |
| PM-RJ | "tentar trocar esse frame dele" | frame novo do EP126 |
| Países | "colocar mais bandeiras" | bandeiras (só desenhei 16) |
| Final V2 | "vocês estão aqui e contando" | ver F01 acima |

## Regras novas incorporadas ao QA permanente
- **STICKER_BOUNDS_CHECK** (`reports/sticker_bounds.py`): em estado de leitura nada cortado nem fora da safe area (90/54 px); inclui contorno branco, emojis, logos, rostos, Toddynho, DeLorean, Marty/Doc.
- Emoji solto = sticker (contorno branco); emoji inline em pill/texto pode ficar inline.
- Kinoplex: logo **branca e original**, nunca sticker.
