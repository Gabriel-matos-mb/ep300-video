# Aprendizados e case replicável — EP300 Cinema Opening

> Objetivo: não só "fizemos um vídeo para o EP300", mas "o que aprendemos
> construindo uma abertura audiovisual de evento baseada numa experiência digital
> interativa?" — preenchido conforme o trabalho avança, não escrito de uma vez.
> Regra: FAZER → USAR → OBSERVAR → APRENDER → GENERALIZAR. Nada aqui é promovido a
> capacidade compartilhada sem evidência (ver `evidence-model` no wiki).

## PROBLEMA
Produzir um vídeo de abertura de evento presencial (telão de cinema) cuja
linguagem visual deve derivar de uma experiência digital ainda em construção por
outra equipe (Claudio/Lucian), com prazo fixo de evento e sem controle sobre
quando os assets ficam prontos.

## CONTEXTO
Ver [CONTEXT.md](CONTEXT.md) e [STATUS.md](STATUS.md).

## DEPENDÊNCIAS
Gravação (data a confirmar), especificações do telão, site do EP300. Ver
[CONTEXT.md](CONTEXT.md).

## DECISÕES
- Manter o breakdown do roteiro no wiki (`ep300-roteiro-edicao.md`), não duplicado
  em `projects/` — evita duas fontes do mesmo conteúdo.
- Criar `projects/ep300-cinema-opening/` como camada de contexto/produção
  específica, sem mexer nas regras gerais de Podcast/Cursos/Copilot.
- Não fechar direção visual fina antes do site chegar — mapa provisório em
  `VISUAL_SYSTEM.md`, gramática de motion só depois.
- Não criar `agents/`, `workflows/`, `templates/`, `scripts/` vazios — só quando
  houver evidência real de repetição.
- **Princípio de handoff editorial** (registrado 2026-09-26, ainda experimental):
  toda geração audiovisual automatizada, quando aplicável neste projeto, deve
  deixar componentes individuais nomeados e reutilizáveis (não só o render final)
  — para o Gabriel conseguir assumir a montagem manualmente no Premiere sem
  depender de uma automação obscura. Ver candidato "Motion Kit" abaixo.

## PROCESSO
- **V0 (28/09):** take real → sincronia das 3 câmeras por correlação de áudio → transcrição local (large-v3, sem VAD)
  → mapa narrativo (fala → intenção → câmera → visual → som) → `plan.py` como fonte única → overlays por cue
  (Pillow → ProRes 4444 alpha) → base de câmera por proxies → mix → composição em streaming → QA → XML Premiere
  + manifesto → Drive oficial → Studio (outputs, mesmo modelo do Copilot 04).
- **Motion Kit (2ª validação):** 39 overlays individuais nomeados `Cxx_yy_NOME.mov` + XML que os posiciona —
  se o Gabriel conseguir reeditar no Premiere a partir disso, o candidato "Motion Kit" ganha a 2ª evidência.

## FERRAMENTAS
`hyperframes-*` (composição/motion), Studio (`#/ep300`), wiki (breakdown),
Notion (roteiro oficial).

## RESULTADO
(preencher após a exibição em 08/10/2026)

## ERROS
- Whisper marca fim de palavra cedo: 3 emendas cortaram sílabas ("empresas", "por anos", 1ª tentativa de "fora de
  casa"). Só a **retranscrição do resultado** + energia em 10 ms pegou — regra da skill edicao-youtube-mb confirmada.
- ffmpeg com 41 entradas ProRes deslocadas no tempo estourou memória → composição em streaming (só overlays ativos).
- Testes do Studio usavam o manifest REAL como fixture (retrato pré-gravação) — quebraram quando o estado real
  avançou; movidos para `studio/scripts/fixtures/productions/`.

## APRENDIZADOS
(preencher no fechamento — comparar com o Debriefing oficial do evento no Notion)

## CANDIDATOS A CAPACIDADE REUTILIZÁVEL (sem evidência ainda — não implementar)

Identificados a partir do pedido original, avaliados pelos critérios (repete? tem
entrada/saída clara? economiza trabalho real? reduz erro? seguro? específico deste
projeto ou global?):

| Candidato | O que faria | Por que ainda é só candidato |
|---|---|---|
| Site Visual Analyzer | Inventariar componentes/tokens de um site e propor tradução para motion | Só faz sentido quando o site do EP300 chegar; zero evidência de repetição ainda |
| Script-to-Scene Mapper | Transformar roteiro em breakdown operacional (o que já foi feito à mão em `ep300-roteiro-edicao.md`) | Foi feito manualmente 1 vez; se se repetir em outra produção de evento, vira candidato real |
| Screen/Cinema QA | Checklist de safe area/contraste/sync específico de projeção em telão | Depende das specs do telão chegarem para ter conteúdo real de teste |
| Asset Checker | Conferir se todos os assets do banco de material (`ep300-roteiro-edicao.md`) existem antes de travar edição | Útil já nesta produção, mas ainda é um checklist manual — automação só se o banco crescer muito |
| Motion QA | Validar consistência do "fio visual" (marca-texto laranja, grade de proporção repetida) entre inserts | Precisa da gramática de motion existir primeiro |
| Render Validator | Conferir formato/resolução de entrega contra as specs confirmadas do telão | Só é acionável depois que o telão responder |
| Motion Kit (nomenclatura cena→ordem→tipo→conteúdo, ex. `C03_01_CARD_300_EPISODIOS.mov`) | Organizar toda geração automatizada de inserts/motion em arquivos individuais nomeados, não só o render final | **1ª validação real: Analytics Copilot 2** (a IA gerou inserts/motion separados e organizados, permitindo o Gabriel assumir a montagem manual no Premiere). EP300 seria a **2ª validação** — só GENERALIZAR (virar padrão do pipeline) se funcionar de novo aqui |

Nenhum destes será implementado nesta rodada — registrados para não perder o
sinal, revisar quando houver evidência (uso real repetido, não só possibilidade).

## Específico do EP300 vs. potencialmente reutilizável

**Específico do EP300**: o roteiro, a linguagem visual derivada do site do EP300,
as datas/local do evento, os cuidados editoriais (Uncover, empresas a nomear).

**Potencialmente reutilizável** (sem promover ainda): a estrutura de projeto
`projects/<slug>/` para produções de evento/telão fora do fluxo semanal de
Podcast/YouTube; o padrão de "mapa visual provisório → gramática de motion" para
traduzir uma experiência digital em vídeo; o checklist parametrizável de QA de
telão. Promoção a capacidade compartilhada exige decisão do Gabriel, não
generalização automática.


## 2026-09-29 — V0 → V1 (madrugada autônoma)

- **Sync por áudio não garante sync de imagem.** A CAM_GERAL (captura HDMI + áudio da mesa) grava a imagem ~150–180 ms
  atrasada em relação ao próprio áudio. Correlacionar áudio câmera×mesa alinhou as fechadas certo, mas a geral ficou fora.
  Método que resolveu: **imagem×imagem** (movimento da cabeça da mesma pessoa na fechada × na geral, `v1/sync_check.py --vidvid`),
  começo/meio/fim. Lip-sync por boca×envelope foi ruidoso demais (duas vozes) — não usar como prova.
- **Arquivo registrado ≠ handoff.** A V0 estava no Studio, mas o Gabriel entra por `#/ep300` (item fixado) e lá a versão era
  só texto; o player vivia em `#/processos/…`. Validar o caminho que o humano realmente usa, não a rota que eu conheço.
- **Marcadores do Premiere são legíveis**: `.prproj` = XML gzip; FCP XML exportado pelo Gabriel traz `<marker>` com comentário.
  Lumetri só no .prproj (FCP XML não carrega) → preservar via 'colar atributos' + aproximação numérica só no proxy.
- **Caminhos > 260 caracteres** no Drive (`300_[Kinoplex] …/erros de gravação antigos/…`) quebram Python/Premiere no Windows;
  `glob` também quebra com `[Kinoplex]` (usar `glob.escape`). Mídia referenciada no XML vai para cópia com nome curto.
- **QA visual por folha de contato sobre o quadro real** pegou ~15 oclusões/sobras antes do render; a retranscrição do proxy
  pegou um resto de sílaba ('…co' de 2025) que o envelope de energia não mostrava.
- Transição de papel em tela cheia: elementos precisam ser recortados pela mesma máscara, senão vazam sobre a câmera.

## V2 (29/09) — aprendizados
- **Vazamento de câmera entre telas cheias** era wipe-out da anterior + wipe-in da seguinte encostadas. Correção estrutural: empurrão (`push_in/push_out` no motor) e teste determinístico
  compondo todos os overlays sobre magenta (`v2/qa_leak.py`). Testar com `--strict` prova que o teste não é vazio.
- **Fim do filme = início do loop:** o final importa o `build.py` do loop e termina nos quadros 118,5–120 s do próprio loop (diferença ≤ 2/255 vs o quadro do loop).
- **Ducking + ganho baixo** resolvem "SFX compete com voz"; medir SFX×voz por evento (`v2/qa_audio.py`).
- Drive é lento em `find`: usar `ls` por pasta e `ffmpeg -ss` antes do `-i` em arquivos de GB.
- Estágios "Revisão/QA/Master/Exibição" no card EP300 usam gates antigos (`gravacao`/`telao`) e mostram ✓ mesmo sem master — inexato (fora do escopo; ver oportunidade de rota).
