# Design system: arena

O portfólio mostra sistemas se comportando ao vivo, com a linguagem de jogo online: requisições que percorrem a arquitetura, casos contados como replay, projetos listados como servidores. Vocabulário de jogo fica na forma e na interação; os rótulos continuam em português direto, sem metáfora para decifrar.

## Princípios

1. **O desenho é a prova.** Toda afirmação técnica importante vem com o desenho do sistema em que ela aconteceu.
2. **Âmbar marca o que importa.** Cantoneiras, ação principal, item ativo e anotações nos desenhos. Nada mais recebe a cor.
3. **Interface de jogo, não fliperama.** Nada de brilho, neon, gradiente ou animação gratuita. A referência é um painel de estado bem desenhado.
4. **Estrutura carrega informação.** Bordas separam unidades de conteúdo; o losango marca início de seção; a faixa âmbar marca o topo de um cartão.

## Cores

| Token | Escuro (padrão) | Claro | Uso |
|---|---|---|---|
| `--paper` | `#15131D` | `#EEEDF2` | Fundo da página |
| `--sheet` | `#1D1A28` | `#FFFFFF` | Painéis, cartões, caixas dos desenhos |
| `--ink` | `#F0EDE6` | `#1B1826` | Texto e traços principais |
| `--muted` | `#A8A3B8` | `#5C5870` | Texto de apoio |
| `--line` | `#3B3652` | `#CBC8D8` | Bordas e divisórias |
| `--grid` | `#221F30` | `#E6E4EE` | Quadriculado do painel principal |
| `--accent` / `--pencil` | `#F2A33A` | `#A65E00` | Destaque, anotações, foco do teclado |

O modo claro existe para quem preferir, mas a identidade do site é o escuro: sem escolha salva, ele abre escuro, independentemente do sistema.

## Tipografia

| Família | Papel |
|---|---|
| **Chakra Petch** (500, 700) | Títulos, navegação, rótulos, botões e todo texto dentro dos desenhos |
| **Atkinson Hyperlegible** (400, 700) | Texto corrido. Desenhada para máxima legibilidade, equilibra a geometria da Chakra Petch |

Escala: `--step--1` 0,875rem, `--step-0` 1,0625rem (corpo), `--step-1` 1,3rem, `--step-2` 1,85rem, `--step-3` até 4rem (nome). Texto corrido com no máximo 40rem de largura.

## Layout

- Coluna única alinhada à esquerda, largura máxima de 70rem.
- Seções separadas por espaço; cada título de seção começa com o losango âmbar.
- Navegação f## Componentes

- **Faixa de status (`.status`):** quatro campos com informação real (foco, stack, base, contato). O indicador âmbar ao lado do e-mail é o único "ao vivo" sem dados por trás, e marca o canal de contato.
- **Painel ao vivo (`.panel`):** desenho da arquitetura atual sobre quadriculado discreto, com cantoneiras âmbar. "Rodar uma requisição" solta um pacote que percorre as setas; cada nó acende ao processar e o caminho percorrido fica marcado. Ao lado, o registro numerado de cada etapa.
- **Replay (`.replay`):** cada estudo de caso tem quatro marcos (Antes, Problema, Decisão, Depois) numa linha do tempo de losangos. O desenho muda de estado a cada marco: o que é problema acende no marco Problema, o que é novo entra tracejado na Decisão e fica destacado no Depois. Narração por marco, botão "Assistir" com pausa e resumo em texto sempre visível.
- **Carrossel de casos (`.carousel`):** um replay por vez, com abas nomeadas, contador e setas. No celular, vira lista vertical e cada desenho rola na horizontal.
- **Ampliar desenho (`dialog.zoom`):** abre o desenho no marco atual em tela cheia, com aumentar e diminuir.
- **Lista de servidores (`.servers`):** projetos em linhas com nome, tipo, descrição, stack e ano, e filtros por tema. No celular, cada linha vira um bloco.
- **Temporadas (`.seasons`):** experiência em cartões lado a lado, do mais recente ao mais antigo, com período em âmbar e faixa no topo.
- **Retrato (`.portrait`) e contato (`.contact-box`):** mesmas cantoneiras do painel. O e-mail é a ação principal da página.
- **Favicon (`favicon.svg`, `apple-touch-icon.png`):** a inicial H em branco entre duas cantoneiras âmbar, sobre o fundo escuro. Legível em 16 px e repetindo as cantoneiras do painel. O ícone de 180 px para a tela inicial do celular não tem cantos arredondados, porque o sistema aplica a própria máscara.
- **Tema (`.theme-btn`):** escuro por padrão; alterna para claro e lembra a escolha.

btn`):** alterna entre escuro e claro e lembra a escolha.

## Regras

- Sentença normal em títulos e rótulos; nada de caixa-alta.
- Sem sombras, gradientes, brilho ou cantos arredondados.
- Botões: contorno âmbar; preenchidos só na ação principal e no estado ativo.
- Sem animação de entrada. Transições só respondem a ação do visitante e são desligadas com `prefers-reduced-motion`.
- JavaScript só como melhoria: sem ele, tudo continua navegável.
- Foco do teclado sempre visível, em âmbar.
- Nenhum recurso de terceiros além das métricas opcionais da Cloudflare: fontes, imagens e estilos saem do próprio domínio.
