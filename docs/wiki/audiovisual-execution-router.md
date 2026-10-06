# Audiovisual Execution Router

**Regra arquitetural transversal (02/10/2026; corrigido em 03/10/2026):** Claude não escolhe uma ferramenta simplesmente porque sabe usá-la. Antes de executar uma tarefa audiovisual, classificar a natureza, escolher o motor apropriado, escolher o modelo Claude correto, executar preservando autoridades humanas.

Referência: mapeia TRABALHO → MOTOR → MODELO.

---

## Princípio Central

**TRABALHO**  
↓  
**MOTOR** (qual ferramenta/autoridade)  
↓  
**MODELO** (qual Claude)  
↓  
**EXECUÇÃO** (preservando decisões anteriores e autoridades)

Nunca: MODELO/FERRAMENTA → tentar encaixar o trabalho nela.

---

> **Nota 03/10/2026 (evidência EP300):** além de Remotion/HyperFrames, o EP300 usou o **motor V2 (Python/PIL, `v2/engine.py`;
> re-render nativo em `review01/b2` e `b3`)** para motions já definidos na V2 — rota LEGADO/ESPECIALIZADA: boa para repetir
> a linguagem aprovada, 1080p nativo (4K = ampliação 2×). Para 4K nativo de componente novo, preferir Remotion (`RSCALE=2`).
> Layers extraídos por **matte** de renders prontos foram abandonados (recortes ruins): re-render nativo é o padrão.

---

## 1. EDITORIAL

Se a tarefa envolve escolha de:
- take;
- câmera;
- multicam;
- performance;
- reação/expressão;
- interpretação da fala;
- timing de humor;
- continuidade narrativa;
- montagem;
- ritmo global;
- decisão subjetiva entre performances;
- framing editorial;
- tratamento de cor/áudio já realizado manualmente.

**ROUTE:** PREMIERE / HUMAN EDITORIAL AUTHORITY

Claude pode:
- analisar;
- localizar;
- comparar;
- sugerir;
- preparar;
- fazer QA técnico.

Claude **NÃO** pode substituir silenciosamente uma decisão editorial humana.

Uma ferramenta automática também não pode reconstruir uma montagem humana já existente sem autorização explícita.

---

## 2. MOTION EDITORIAL

Se a tarefa é transformar uma ideia em momento visual expressivo:
- typography hero;
- números hero;
- stickers;
- polaroids;
- scrapbook;
- timelines narrativas;
- composições com muitos assets;
- fullscreen visual;
- punchline visual;
- transições gráficas;
- micro-histórias visuais;
- motion baseado em conceito;
- entradas/coreografias de vários elementos.

**ROUTE PREFERENCIAL (BENCHMARKING):**

**HYPERFRAMES + GSAP**

```
PURPOSE: EDITORIAL_MOTION_DESIGN
STATUS: CANDIDATE — benchmarks em progresso
DECISION PONTO: não é ainda substituto definitivo do Remotion
```

**Heurística:** HyperFrames = desenhar/coreografar O MOMENTO.

Ver [[hyperframes]] para detalhe de quando cada engine é mais apropriado.

---

## 3. SISTEMA DE VÍDEO

Se a necessidade é construir:
- reutilizável;
- parametrizado;
- baseado em JSON/dados;
- gerador;
- template;
- produção em lote;
- componente audiovisual;
- lower third reutilizável;
- gráfico parametrizado;
- legendagem sistemática;
- estrutura que produzirá muitos vídeos;
- automação audiovisual.

**ROUTE:** REMOTION

```
PURPOSE: PROGRAMMATIC_VIDEO_SYSTEM
STATUS: DEFAULT
```

**Heurística:** Remotion = construir O SISTEMA.

Não considerar HyperFrames e Remotion concorrentes absolutos. Eles coexistem.

---

## 4. PROCESSAMENTO TÉCNICO

Se a tarefa é determinística:
- transcode;
- codec;
- proxy;
- resize;
- FPS;
- extração de frames;
- contact sheet;
- mux/demux;
- metadata;
- inspeção de streams;
- conversão;
- preparação de assets;
- render auxiliar;
- QA técnico;
- concatenação quando a decisão editorial já está determinada.

**ROUTE:** FFMPEG / FFPROBE

```
PURPOSE: MEDIA_UTILITY / TECHNICAL_QA
```

**REGRA CRÍTICA:**

FFmpeg **PODE** executar uma decisão editorial JÁ TOMADA.

FFmpeg **NÃO PODE** tomar a decisão editorial.

FFmpeg nunca deve reconstruir automaticamente uma timeline humana autoritativa apenas porque tecnicamente consegue acessar os arquivos brutos.

---

## 5. SPECIALIST ROUTES

### Motion Canvas

**Status:** SPECIALIST / NÃO DEFAULT

Considerar quando a tarefa for predominantemente:
- diagrama;
- fluxo;
- arquitetura;
- explicação visual;
- visualização vetorial;
- animação educacional;
- relações espaciais/diagramáticas complexas.

Não adicionar ao pipeline por padrão se HyperFrames/Remotion resolverem adequadamente.

---

## 6. ANALYSIS TOOLCHAIN

Ferramentas de:
- transcrição;
- speech analysis;
- ffprobe;
- frame extraction;
- scene detection;
- metadata;
- computer vision;
- comparação;
- QA.

pertencem à camada: **ANALYSIS**

e **NÃO** à camada: **EDITORIAL AUTHORITY**.

Analisar uma timeline não concede autoridade para remontá-la.

---

## 7. PRESERVAÇÃO DE AUTORIDADE

Antes de executar:

**EXISTE UMA DECISÃO HUMANA ANTERIOR?**

- **SIM:** preservar. A ferramenta deve trabalhar AO REDOR da decisão existente.
- **NÃO:** verificar se Claude possui autoridade para decidir. Se for decisão editorial subjetiva sem precedente: HUMAN REVIEW.

Autonomia operacional ≠ autonomia editorial.

---

## 8. REGRA DA FERRAMENTA MAIS SIMPLES

Antes de escolher uma solução:

**"Existe uma ferramenta mais simples e barata que resolve isto com a mesma qualidade?"**

- Se SIM: usar a mais simples.

Exemplos:
- não usar Opus + HyperFrames para tarefa determinística que FFmpeg ou script simples resolve.
- Não usar motion engine para corrigir metadata.
- Não usar FFmpeg para fazer motion design.
- Não usar Remotion para reconstruir edição do Premiere.

---

## 9. REUSE BEFORE REBUILD

Antes de construir:

verificar se já existe:
- asset aprovado;
- motion aprovado;
- template;
- componente;
- composição;
- decisão;
- render;
- implementação reutilizável.

Se existe e é adequado: **REUTILIZAR**.

Não reconstruir automaticamente trabalho já aprovado.

---

## 10. EDITABILIDADE

Se o resultado voltar para Premiere ou outro NLE:

preservar editabilidade sempre que tecnicamente razoável.

Preferir, conforme o caso:
- alpha;
- layers;
- assets separados;
- composição editável;
- source project;
- parâmetros;
- versões intermediárias.

Não flatten/destruir uma estrutura editável sem necessidade ou autorização.

Ver [[principios-confirmados-ep300]] § 11 (EDITABILIDADE É PARTE DA ENTREGA).

---

## 11. PIPELINE DE VALIDAÇÃO

Para outputs audiovisuais automáticos:

```
BUILD
  ↓
RENDER PROXY
  ↓
TECHNICAL QA
  ↓
VISUAL SELF-REVIEW
  ↓
CORREÇÃO OBJETIVA, quando necessária
  ↓
HUMAN CREATIVE REVIEW, quando houver decisão criativa
  ↓
INTEGRATION
```

Claude pode corrigir autonomamente problemas objetivos:
- clipping;
- safe area;
- logo cortada;
- asset deformado;
- texto ilegível;
- colisão;
- frame vazio acidental;
- render quebrado;
- contraste evidentemente insuficiente;
- timing tecnicamente quebrado.

Claude **NÃO** deve transformar uma revisão técnica em autorização para redesenhar criativamente o trabalho.

---

## 12. MODEL ROUTER

A escolha do modelo acontece **DEPOIS** da escolha do trabalho e motor.

**Heurística inicial:**

### HAIKU
- localizar arquivos;
- conferir assets;
- metadata;
- checklists;
- reconciliação documental;
- QA simples;
- tarefas mecânicas.

### SONNET
- implementação normal;
- código;
- automação;
- Remotion;
- HyperFrames quando a direção já está definida;
- análise audiovisual mais complexa;
- QA visual mais sofisticado.

### OPUS
- problema criativo realmente complexo;
- motion design novo/difícil;
- benchmark;
- raciocínio audiovisual que Sonnet não resolveu satisfatoriamente.

Preferir inicialmente **MEDIUM** quando Opus for necessário. Subir esforço somente se houver evidência de necessidade.

---

## 13. DECISION TREE RESUMIDA

Pergunte:

**"É decisão de montagem/performance/take/câmera?"**  
↓ SIM → PREMIERE / HUMAN  
↓ NÃO ↓

**"É motion único, expressivo, narrativo ou editorial?"**  
↓ SIM → HYPERFRAMES + GSAP [CANDIDATE enquanto benchmark]  
↓ NÃO ↓

**"É sistema reutilizável, parametrizado ou produção em escala?"**  
↓ SIM → REMOTION  
↓ NÃO ↓

**"É processamento técnico determinístico?"**  
↓ SIM → FFMPEG / scripts  
↓ NÃO ↓

**"É diagrama/animação vetorial explicativa especializada?"**  
↓ SIM → considerar MOTION CANVAS  
↓ NÃO ↓

**"É análise/transcrição/metadata?"**  
↓ SIM → ANALYSIS TOOLCHAIN  
↓ NÃO ↓

Se continuar ambíguo: não escolher ferramenta arbitrariamente. Classificar melhor a tarefa primeiro.

---

## 14. ARQUITETURA DESEJADA

```
                 HUMAN / GABRIEL
                       |
                 direção editorial
                       |
                    PREMIERE
                       |
          +------------+-------------+
          |            |             |
     HYPERFRAMES    REMOTION       FFMPEG
       + GSAP
          |            |             |
       MOTION       VIDEO SYSTEM    UTILITY
       DESIGN       / SCALE          / QA
          |            |             |
          +------------+-------------+
                       |
                    PREMIERE
                       |
                     FINAL
```

Claude Code atua **ACIMA** desses motores como orquestrador.

Claude decide qual motor utilizar com base na natureza do trabalho — **respeitando autoridade humana, custo, reutilização e editabilidade**.

---

## Integração com estruturas existentes

Esta regra é **complementar** a:

- [[principios-confirmados-ep300]] — governa ESTADOS E CICLO DE VIDA (FILE EXISTS ≠ DELIVERED, READY_FOR_HUMAN ≠ APROVADO, etc.). O ROUTER governa QUAL FERRAMENTA LEVA AO ESTADO CORRETO.

- [[automation-architecture]] — governa QUAL MECANISMO DE AUTOMAÇÃO usar (Script/Claude/Skill/Hook/etc.). O ROUTER diz ANTES DISSO se deve automatizar e qual ferramenta escolher.

- [[production-model]] — governa CICLO DE VIDA de arquivos (SOURCE/WORKING/DELIVERABLE/etc.). O ROUTER diz QUAL FERRAMENTA GERA OS ARQUIVOS QUE PRODUÇÃO_MODEL CLASSIFICA.

---

## Checklist: antes de executar

- [ ] Trabalho foi classificado em categoria 1–6 acima?
- [ ] Autoridade humana anterior (§7) foi preservada?
- [ ] Ferramenta mais simples (§8) foi priorizada?
- [ ] Reutilização (§9) foi verificada?
- [ ] Editabilidade (§10) foi considerada?
- [ ] Modelo Claude (§12) foi escolhido APÓS ferramenta, não antes?
- [ ] Pipline de validação (§11) foi planejado?
- [ ] Regra crítica do FFmpeg (§4) foi respeitada (não reconstruir edição humana)?

---

## Fonte

Consolidado a partir de trabalho real (EP300, Manifesto, Copilot 04, benchmarks 2026-10). Incorpora [[principios-confirmados-ep300]], [[automation-architecture]], [[production-model]], [[estilo-edicao]].
