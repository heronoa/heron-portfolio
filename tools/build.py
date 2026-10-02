import diagrams as D, replays as RP
from html import escape as e

CASES = [
  dict(id='caso-sso', tab='Login único', title='Login único com Keycloak em 14 dias', ctx='Plataforma SaaS de ensino, backend', d=RP.sso(),
       narr=['Cada cliente fazia login contra a API, que validava senhas numa base própria da plataforma.',
             'Um edital passou a exigir login único, com 14 dias de prazo e sem poder quebrar os clientes web e mobile já em produção.',
             'A decisão: colocar o Keycloak como intermediador e manter na API uma fachada com o mesmo contrato de login.',
             'Secretaria e escolas ficaram em realms separados, e cada usuário migra para o Keycloak no primeiro login, sem reset de senha em massa.'],
       summary='Entregue dentro do prazo do edital. A auditoria do login antigo feita no caminho encontrou uma falha de acesso indevido entre perfis, corrigida antes da troca.'),
  dict(id='caso-email', tab='Vínculo por e-mail', title='Vincular contas por e-mail sem confiar no campo de e-mail', ctx='Plataforma SaaS de ensino, backend', d=RP.email(),
       narr=['O plano óbvio: quando o login com Google chega, procurar um cadastro com o mesmo e-mail e vincular.',
             'Os dados reais mostraram o risco: muitos e-mails eram texto de preenchimento, e o e-mail do responsável aparecia no cadastro do aluno.',
             'A decisão: uma regra em quatro passos, escrita depois de consultar o banco, que prioriza quem tem o e-mail como próprio.',
             'A conta de um responsável nunca resolve para o cadastro de uma criança, e quem teve o e-mail copiado em várias fichas entra como ele mesmo.'],
       summary='A regra normaliza o e-mail, descarta valores de preenchimento, procura quem tem aquele e-mail como próprio e só então desempata por contagem.'),
  dict(id='caso-carga', tab='Teste de carga', title='O teste de carga apontou para o código, não para a máquina', ctx='Plataforma SaaS de ensino, desempenho', d=RP.k6(),
       narr=['A plataforma atendia as redes de ensino com uma API NestJS, um interceptor de auditoria e o PostgreSQL.',
             'A sensação no time era de que faltava máquina, mas ninguém sabia em que carga o sistema começava a degradar.',
             'A decisão: medir antes de escalar, com um teste de carga em k6 contra produção, numa janela controlada.',
             'A saturação apareceu cedo e as causas estavam no código: consultas N+1 e um interceptor caro em toda requisição.'],
       summary='O relatório virou um plano de correção priorizado em vez de um pedido de orçamento para mais máquina.'),
  dict(id='caso-ranking', tab='Ranking em Redis', title='Ranking de jogo: de Lambda para Redis', ctx='Empresa de jogos Web3, backend', d=RP.ranking(),
       narr=['Cada pontuação disparava uma função Lambda que recalculava o ranking inteiro a partir do banco.',
             'O custo crescia junto com o número de jogadores: mais partidas, mais recálculos completos.',
             'A decisão: trocar o recálculo por sorted sets no Redis, que mantêm a ordem a cada pontuação nova.',
             'O ranking passou a ser lido direto do Redis, atualizado na hora, com cerca de US$ 300 a menos por mês.'],
       summary='Cada pontuação entra no sorted set e o topo do ranking é lido direto, sem recálculo.'),
]
MARKS = ['Antes', 'Problema', 'Decisão', 'Depois']

def replay(i, c):
    narr = ''.join(f'<li>{e(t)}</li>' for t in c['narr'])
    marks = ''.join(f'<div><button type="button" data-step="{j}">{m}</button></div>' for j, m in enumerate(MARKS))
    return f'''
      <article class="replay slide" id="{c['id']}" aria-roledescription="slide" aria-label="{i+1} de {len(CASES)}">
        <header class="replay-head">
          <div><h3>{e(c['title'])}</h3><p class="meta">{e(c['ctx'])}</p></div>
          <button type="button" class="zoom-btn">Ampliar desenho</button>
        </header>
        <figure class="replay-fig">{c['d'].svg(i)}</figure>
        <div class="timeline" role="group" aria-label="Marcos do caso"><span class="fill" aria-hidden="true"></span>{marks}</div>
        <ol class="narr-src">{narr}</ol>
        <p class="narration" aria-live="polite"></p>
        <div class="replay-controls">
          <button type="button" class="play">Assistir</button>
          <button type="button" class="prev">Marco anterior</button>
          <button type="button" class="next">Próximo marco</button>
        </div>
        <p class="summary">{e(c['summary'])}</p>
      </article>'''

PROJECTS = [
  dict(name='kanban-api', url='https://github.com/heronoa/kanban-api', kind='API REST', stack='NestJS, Prisma, PostgreSQL, GitHub Actions', year='2025', tags='nestjs testes',
       desc='API de quadro Kanban em casos de uso e repositórios, com JWT e papéis, Swagger e CI que roda testes de integração contra um PostgreSQL real antes do deploy.',
       origin='Nasceu como desafio técnico de um processo seletivo e foi o código que me levou à vaga.'),
  dict(name='ait-manager', url='https://github.com/heronoa/ait-manager', kind='API e filas', stack='NestJS, Prisma, PostgreSQL, AWS SQS', year='2024', tags='nestjs filas',
       desc='API para gestão de autos de infração de trânsito com produtor e consumidor de filas SQS.',
       origin='Escrito como desafio técnico de um processo seletivo.'),
  dict(name='turnbased-pvp-colyseus', url='https://github.com/heronoa/turnbased-pvp-colyseus', kind='Tempo real', stack='Node.js, Colyseus, WebSocket, Prisma', year='2024', tags='tempo-real jogos',
       desc='Servidor de batalha por turnos em tempo real, com matchmaking e um bot que entra se ninguém aparecer em 15 segundos. Cliente em Vue 3 com testes em Cypress.',
       origin='Escrito para estudar servidores de jogo em tempo real.'),
  dict(name='payments-api', url='https://github.com/heronoa/payments-api', kind='API e rotinas', stack='Express, MongoDB, AWS S3', year='2024', tags='filas',
       desc='API de cobranças com cálculo de juros, jobs agendados, upload de comprovantes para o S3 e avisos por e-mail e WhatsApp.',
       origin='Escrito para estudar rotinas agendadas e integrações de mensagem.'),
]
FILTERS = [('todos', 'Todos'), ('nestjs', 'NestJS'), ('tempo-real', 'Tempo real'), ('filas', 'Filas e rotinas'), ('jogos', 'Jogos')]

def project(p):
    return f'''
        <li class="server" data-tags="{p['tags']}">
          <div class="s-name"><a href="{p['url']}">{e(p['name'])}</a><span class="s-kind">{e(p['kind'])}</span></div>
          <p class="s-desc">{e(p['desc'])} <span class="s-origin">{e(p['origin'])}</span></p>
          <p class="s-stack">{e(p['stack'])}</p>
          <p class="s-year">{p['year']}</p>
        </li>'''

ROLES = [
  dict(title='Backend Pleno', when='09/2025 até hoje', org='Plataforma SaaS de gestão para redes públicas de ensino', items=[
    'Login único com Keycloak em 14 dias, exigido por edital, sem quebrar nenhum cliente.',
    'Auditoria do login existente, com uma falha de IDOR encontrada e corrigida via hotfix.',
    'Teste de carga com k6 que levou o gargalo até consultas N+1 e um interceptor de auditoria.',
    'Suíte de 110 testes e2e (cerca de 75% de cobertura) e estratégia de pirâmide de testes.',
    'Infraestrutura em Terraform na GCP, com Workload Identity Federation, state remoto com lock, Cloudflare Access e alertas no Grafana.']),
  dict(title='Backend e infraestrutura, autônomo', when='em andamento', org='Projeto para um cliente sob acordo de confidencialidade', items=[
    'Autenticação por código único (OTP) em NestJS e Redis, com WhatsApp e SMS, migrando para geração própria no backend.',
    'Infraestrutura on-premises com Proxmox, disco criptografado, NAS em RAID 1, backup criptografado com cópia externa e acesso remoto via Tailscale.']),
  dict(title='Desenvolvedor Full Stack, de júnior a pleno', when='04/2022 a 09/2025', org='Empresa de jogos e produtos Web3 em São Paulo', items=[
    'APIs REST em Node.js, Express, Prisma, Mongoose e PostgreSQL, com JWT e login social.',
    'Backend de um jogo de batalha por turnos em tempo real com WebSockets, Redis e PostgreSQL.',
    'Plataforma DeWi com processamento assíncrono via mensageria AMQP (LavinMQ).',
    'Ranking migrado de Lambda para Redis e cache que reduziu em 32% as consultas ao banco.',
    'Passagem por frontend, backend e infraestrutura, até virar referência técnica do time.']),
  dict(title='Desenvolvedor Flutter', when='08/2024 a 01/2025', org='Aplicativo de verificação de identidade para um cliente sob acordo de confidencialidade', items=[
    'Funcionalidades mobile com Provider e ViewModel, com testes unitários e de widget.',
    'Avaliação e integração de verificação facial e prova de vida.',
    'Problemas de arquitetura registrados como ADRs; a correção proposta foi adotada pelo time.']),
]

def role(r):
    lis = ''.join(f'<li>{e(i)}</li>' for i in r['items'])
    return f'''
        <li class="season">
          <p class="when">{e(r['when'])}</p>
          <h3>{e(r['title'])}</h3>
          <p class="org">{e(r['org'])}</p>
          <ul>{lis}</ul>
        </li>'''

ARROW_L = '<svg viewBox="0 0 20 20" aria-hidden="true"><polyline points="13,4 7,10 13,16"/></svg>'
ARROW_R = '<svg viewBox="0 0 20 20" aria-hidden="true"><polyline points="7,4 13,10 7,16"/></svg>'

def ctrl(target, prev_label, next_label, count=True):
    c = '<span class="car-count" aria-live="polite"></span>' if count else ''
    return (f'<div class="car-ctrl" data-for="{target}"><button type="button" class="car-btn" data-dir="-1" aria-label="{prev_label}">{ARROW_L}</button>'
            f'{c}<button type="button" class="car-btn" data-dir="1" aria-label="{next_label}">{ARROW_R}</button></div>')

def page(css_href='styles.css', js_head='<script src="theme.js"></script>', js_body='<script src="site.js" defer></script>', preload=True, photo='foto.jpg', pdf='heron-amaral-curriculo.pdf'):
    pre = ('<link rel="preload" href="fonts/chakra-petch-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>\n  '
           '<link rel="preload" href="fonts/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n  ') if preload else ''
    tabs = ''.join(f'<li><a href="#{c["id"]}">{e(c["tab"])}</a></li>' for c in CASES)
    filters = ''.join(f'<li><button type="button" data-filter="{k}" aria-pressed="{"true" if k=="todos" else "false"}">{e(v)}</button></li>' for k, v in FILTERS)
    return f'''<!doctype html>
<html lang="pt-BR" data-default-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Heron Amaral, backend e infraestrutura</title>
  <meta name="description" content="Desenvolvedor backend em Belém. NestJS, TypeScript, PostgreSQL, Redis e infraestrutura como código, com decisões documentadas e medidas.">
  <link rel="canonical" href="https://heronoa.com.br/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://heronoa.com.br/">
  <meta property="og:title" content="Heron Amaral, backend e infraestrutura">
  <meta property="og:description" content="NestJS, TypeScript, PostgreSQL e infraestrutura como código. Estudos de caso contados como replays, com os desenhos de arquitetura.">
  <meta property="og:image" content="https://heronoa.com.br/og.png">
  <meta property="og:locale" content="pt_BR">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#15131D">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  {pre}<meta name="cf-analytics-token" content="">
  {js_head}
  <link rel="stylesheet" href="{css_href}">
  {js_body}
</head>
<body>
{D.DEFS}
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<nav class="nav" aria-label="Seções">
  <div class="wrap">
    <a class="home" href="#topo">Heron Amaral</a>
    <ul>
      <li><a href="#casos">Estudos de caso</a></li>
      <li><a href="#projetos">Projetos</a></li>
      <li><a href="#experiencia">Experiência</a></li>
      <li><a href="#contato">Contato</a></li>
    </ul>
    <button type="button" class="theme-btn" aria-pressed="true" data-to-dark="Modo escuro" data-to-light="Modo claro">
      <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="M10 3a7 7 0 0 1 0 14z"/></svg>
      <span class="theme-label">Modo claro</span>
    </button>
  </div>
</nav>

<main id="conteudo">
  <header class="hero" id="topo">
    <div class="wrap">
      <h1>Heron Oliveira Amaral</h1>
      <p class="lede">Desenvolvedor backend. Escrevo APIs em NestJS e TypeScript, cuido da infraestrutura onde elas rodam e documento por que cada decisão foi tomada.</p>
      <dl class="status">
        <div><dt>Foco</dt><dd>Backend e infraestrutura</dd></div>
        <div><dt>Stack principal</dt><dd>NestJS, PostgreSQL, Redis</dd></div>
        <div><dt>Base</dt><dd>Belém, PA, trabalho remoto</dd></div>
        <div><dt>Contato</dt><dd class="live"><a href="mailto:heron.amaral@gmail.com">heron.amaral@gmail.com</a></dd></div>
      </dl>

      <div class="panel">
        <div class="stage">{D.hero()}{D.hero_mobile()}</div>
        <aside class="log" aria-labelledby="log-t">
          <div class="log-head"><span id="log-t">Registro da requisição</span><span class="log-count"></span></div>
          <ol aria-live="polite"><li class="empty">Rode uma requisição para ver cada etapa aparecer aqui, na ordem em que acontece no sistema da plataforma em que trabalho hoje.</li></ol>
          <button type="button" class="run">Rodar uma requisição</button>
        </aside>
      </div>
    </div>
  </header>

  <section class="section" id="sobre" aria-labelledby="sobre-t">
    <div class="wrap about">
      <div class="about-text">
        <h2 id="sobre-t">Como eu trabalho</h2>
        <p>Comecei numa empresa de jogos Web3 em São Paulo e passei por frontend, backend e infraestrutura até virar referência técnica do time. Hoje cuido do backend e da infraestrutura de uma plataforma usada por redes públicas de ensino.</p>
        <p>Antes de mudar código, eu meço. Antes de confiar num dado, consulto o banco. Quando tomo uma decisão que alguém vai questionar daqui a seis meses, escrevo um registro curto com o contexto, a alternativa descartada e o motivo. Uso IA todos os dias, e o que entra no código é decidido por teste e revisão.</p>
        <p><a class="cta" href="{pdf}">Baixar o currículo completo em PDF</a></p>
      </div>
      <figure class="portrait">
        <img src="{photo}" alt="Foto de Heron Oliveira Amaral" width="800" height="1000" loading="lazy" decoding="async">
        <figcaption>Heron Oliveira Amaral, Belém, PA</figcaption>
      </figure>
    </div>
  </section>

  <section class="section" id="casos" aria-labelledby="casos-t">
    <div class="wrap">
      <div class="section-head">
        <h2 id="casos-t">Estudos de caso</h2>
        {ctrl('car-casos', 'Caso anterior', 'Próximo caso')}
      </div>
      <p class="intro">Quatro decisões reais contadas como replay: percorra os marcos para ver o sistema mudar do problema ao resultado. Dados de clientes e detalhes internos foram omitidos.</p>
      <ol class="car-tabs" data-for="car-casos" aria-label="Ir para o caso">{tabs}</ol>
      <div class="carousel" id="car-casos" role="region" aria-roledescription="carrossel" aria-label="Estudos de caso" tabindex="0">{''.join(replay(i, c) for i, c in enumerate(CASES))}
      </div>
    </div>
  </section>

  <section class="section" id="projetos" aria-labelledby="projetos-t">
    <div class="wrap">
      <h2 id="projetos-t">Projetos com código aberto</h2>
      <p class="intro">Código público no <a href="https://github.com/heronoa">GitHub</a>. Os de 2024 foram escritos como estudo, sem assistência de IA.</p>
      <ul class="filters" aria-label="Filtrar projetos">{filters}</ul>
      <div class="servers-head" aria-hidden="true"><span>Projeto</span><span>Descrição</span><span>Stack</span><span>Ano</span></div>
      <ul class="servers">{''.join(project(p) for p in PROJECTS)}
      </ul>
      <p class="servers-empty" hidden>Nenhum projeto com esse filtro.</p>
    </div>
  </section>

  <section class="section" id="experiencia" aria-labelledby="experiencia-t">
    <div class="wrap">
      <div class="section-head">
        <h2 id="experiencia-t">Experiência</h2>
        {ctrl('strip-exp', 'Período anterior', 'Próximo período', count=False)}
      </div>
      <ol class="strip seasons" id="strip-exp" role="region" aria-label="Experiência, do mais recente ao mais antigo" tabindex="0">{''.join(role(r) for r in ROLES)}
      </ol>
    </div>
  </section>

  <section class="section" id="habilidades" aria-labelledby="habilidades-t">
    <div class="wrap">
      <h2 id="habilidades-t">Habilidades</h2>
      <dl class="skills">
        <div><dt>Backend</dt><dd>Node.js, TypeScript, NestJS, Express, REST, WebSockets, JWT, OIDC, Keycloak</dd></div>
        <div><dt>Dados</dt><dd>PostgreSQL, MongoDB, Redis, TypeORM, Prisma, Mongoose</dd></div>
        <div><dt>Mensageria</dt><dd>AWS SQS, RabbitMQ, LavinMQ</dd></div>
        <div><dt>Testes</dt><dd>Jest, Cypress, unitários, integração, e2e, k6</dd></div>
        <div><dt>Infraestrutura</dt><dd>Docker, Docker Swarm, Terraform, Proxmox, GCP, AWS, Cloudflare, Grafana</dd></div>
        <div><dt>CI/CD</dt><dd>GitHub Actions, GitLab CI, Woodpecker, Cloud Build</dd></div>
        <div><dt>Formação</dt><dd>Tecnólogo em Análise e Desenvolvimento de Sistemas pela Estácio, conclusão prevista em 2027. Antes, CS50 e Zero To Mastery.</dd></div>
        <div><dt>Idiomas</dt><dd>Português nativo, inglês avançado</dd></div>
      </dl>
    </div>
  </section>

  <section class="section contact" id="contato" aria-labelledby="contato-t">
    <div class="wrap">
      <div class="contact-box">
        <h2 id="contato-t">Contato</h2>
        <p>Para conversar sobre backend, infraestrutura ou algum projeto, o caminho mais rápido é o e-mail.</p>
        <p><a class="cta cta-big" href="mailto:heron.amaral@gmail.com">heron.amaral@gmail.com</a></p>
        <ul class="links">
          <li><a href="https://github.com/heronoa">github.com/heronoa</a></li>
          <li><a href="https://www.linkedin.com/in/heron-amaral-49a9a1179">linkedin.com/in/heron-amaral-49a9a1179</a></li>
          <li><a href="{pdf}">Currículo em PDF</a></li>
        </ul>
      </div>
    </div>
  </section>
</main>

<dialog class="zoom" aria-labelledby="zoom-title">
  <div class="zoom-bar">
    <p id="zoom-title" class="zoom-title"></p>
    <div class="zoom-actions">
      <button type="button" data-zoom="-1" aria-label="Diminuir">−</button>
      <button type="button" data-zoom="1" aria-label="Aumentar">+</button>
      <button type="button" class="zoom-close">Fechar</button>
    </div>
  </div>
  <div class="zoom-body"></div>
</dialog>

<footer class="footer">
  <div class="wrap">
    <p>Heron Oliveira Amaral, desenvolvedor backend em Belém, Pará.</p>
    <p>Este site também é código aberto: <a href="https://github.com/heronoa/heron-portfolio">veja como ele foi feito</a>.</p>
  </div>
</footer>
</body>
</html>
'''

if __name__ == '__main__':
    import os, sys
    here = os.path.dirname(os.path.abspath(__file__))
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'site', 'index.html')
    open(dest, 'w').write(page())
    print('gerado', os.path.normpath(dest))
