# Gera os desenhos técnicos (SVG inline) do portfólio.
from html import escape as e
import itertools
_SEQ = itertools.count(1)

class D:
    def __init__(s, w, h, title, desc):
        s.w, s.h, s.title, s.desc, s.parts = w, h, title, desc, []
    def box(s, x, y, w, h, t, sub=None, dashed=False, node=None):
        cls = 'd-box d-dash' if dashed else 'd-box'
        if node:
            s.parts.append(f'<g class="d-node" data-node="{node}">')
        s.parts.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
        if sub:
            s.parts.append(f'<text class="d-t" x="{x+w/2}" y="{y+h/2-3}" text-anchor="middle">{e(t)}</text>')
            s.parts.append(f'<text class="d-s" x="{x+w/2}" y="{y+h/2+14}" text-anchor="middle">{e(sub)}</text>')
        else:
            s.parts.append(f'<text class="d-t" x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle">{e(t)}</text>')
        if node:
            s.parts.append('</g>')
    def arrow(s, pts, dashed=False, label=None, lx=None, ly=None, edge=None):
        p = ' '.join(f'{x},{y}' for x, y in pts)
        cls = 'd-arrow d-dash' if dashed else 'd-arrow'
        de = f' data-edge="{edge}"' if edge else ''
        s.parts.append(f'<polyline class="{cls}"{de} points="{p}" marker-end="url(#mk-ink)"/>')
        if label:
            s.parts.append(f'<text class="d-s" x="{lx}" y="{ly}" text-anchor="middle">{e(label)}</text>')
    def zone(s, x, y, w, h, label):
        s.parts.append(f'<rect class="d-zone" x="{x}" y="{y}" width="{w}" height="{h}"/>')
        s.parts.append(f'<text class="d-zl" x="{x+12}" y="{y+20}">{e(label)}</text>')
    def note(s, x, y, text, to=None, anchor='start'):
        if to:
            ex = x + 6 if anchor == 'start' else x - 6
            ey = y + 18 if to[1] > y + 12 else y - 1
            s.parts.append(f'<polyline class="d-lead" points="{to[0]},{to[1]} {ex},{ey}" marker-start="url(#mk-dot)"/>')
        s.parts.append(f'<text class="d-n" x="{x}" y="{y+12}" text-anchor="{anchor}">{e(text)}</text>')
    def rowlabel(s, x, y, text):
        s.parts.append(f'<text class="d-zl" x="{x}" y="{y}">{e(text)}</text>')
    def svg(s, cls='drawing'):
        n = next(_SEQ)
        return (f'<svg class="{cls}" viewBox="0 0 {s.w} {s.h}" role="img" aria-labelledby="t-{n} d-{n}">'
                f'<title id="t-{n}">{e(s.title)}</title><desc id="d-{n}">{e(s.desc)}</desc>'
                + ''.join(s.parts) + '</svg>')

DEFS = ('<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
        '<marker id="mk-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path class="d-head" d="M0,1 L9,5 L0,9 z"/></marker>'
        '<marker id="mk-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path class="d-head-red" d="M0,1 L9,5 L0,9 z"/></marker>'
        '<marker id="mk-dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">'
        '<circle class="d-dot" cx="5" cy="5" r="3.5"/></marker>'
        '</defs></svg>')

def hero():
    d = D(960, 380, 'Visão geral da plataforma educacional em que trabalho',
          'Painel web em Angular e app em Flutter passam pela Cloudflare até a API NestJS em Docker Swarm na GCP, que usa Keycloak, PostgreSQL e Redis, com alertas no Grafana.')
    d.box(20, 80, 160, 56, 'Painel web', 'Angular', node='web')
    d.box(20, 230, 160, 56, 'App', 'Flutter', node='app')
    d.box(240, 155, 160, 56, 'Cloudflare', 'proxy e Access', node='cf')
    d.zone(440, 20, 500, 340, 'GCP, provisionada com Terraform')
    d.box(470, 70, 180, 56, 'Keycloak', 'identidade e SSO', node='kc')
    d.box(470, 180, 180, 56, 'API NestJS', 'réplicas no Swarm', node='api')
    d.box(470, 290, 180, 56, 'Grafana', 'alertas por e-mail', node='graf')
    d.box(720, 130, 190, 56, 'PostgreSQL', 'Cloud SQL', node='pg')
    d.box(720, 240, 190, 56, 'Redis', 'cache', node='redis')
    d.arrow([(180, 108), (210, 108), (210, 175), (238, 175)], edge='web-cf')
    d.arrow([(180, 258), (210, 258), (210, 193), (238, 193)], edge='app-cf')
    d.arrow([(400, 194), (464, 208)], edge='cf-api')
    d.arrow([(560, 180), (560, 132)], edge='api-kc')
    d.arrow([(650, 200), (714, 165)], edge='api-pg')
    d.arrow([(650, 216), (714, 260)], edge='api-redis')
    d.arrow([(560, 290), (560, 242)], dashed=True, edge='graf-api')
    d.note(680, 60, 'login único entregue em 14 dias', to=(650, 82))
    d.note(462, 300, '110 testes e2e cobrem a API', to=(500, 238), anchor='end')
    return d.svg('drawing drawing-hero')

def sso():
    d = D(960, 330, 'Arquitetura do login único com Keycloak',
          'Clientes existentes chamam a fachada de login na API NestJS, que delega ao Keycloak com realms de secretaria e escolas. Usuários da base legada migram no primeiro login. Integração com gov.br prevista.')
    d.box(20, 130, 160, 56, 'Clientes atuais', 'web e mobile')
    d.box(240, 130, 180, 56, 'API NestJS', 'fachada de login')
    d.box(490, 130, 180, 56, 'Keycloak', 'intermediador')
    d.box(740, 60, 200, 50, 'Realm secretaria')
    d.box(740, 210, 200, 50, 'Realm escolas')
    d.box(490, 20, 180, 50, 'gov.br', 'previsto', dashed=True)
    d.box(240, 250, 180, 56, 'Base legada', 'usuários e senhas')
    d.arrow([(180, 158), (234, 158)])
    d.arrow([(420, 158), (484, 158)])
    d.arrow([(670, 150), (705, 150), (705, 85), (734, 85)])
    d.arrow([(670, 166), (705, 166), (705, 235), (734, 235)])
    d.arrow([(580, 70), (580, 124)], dashed=True)
    d.arrow([(420, 278), (580, 278), (580, 192)], dashed=True)
    d.note(600, 296, 'migrado no primeiro login, sem reset de senha')
    d.note(20, 206, 'nenhum cliente precisou mudar', to=(100, 188))
    return d.svg()

def email():
    d = D(960, 170, 'Regra de vínculo de contas por e-mail',
          'O e-mail vindo do Google é normalizado, valores de preenchimento são descartados, procura-se quem tem o e-mail como próprio e só então desempata-se por contagem antes de chegar ao usuário.')
    xs = [10, 170, 330, 490, 650, 810]
    labels = [('E-mail Google', None), ('Normalizar', 'caixa e espaços'), ('Sem sentinela', 'descarta lixo'),
              ('Dono do e-mail', 'identidade'), ('Desempate', 'por contagem'), ('Usuário', None)]
    for x, (t, s) in zip(xs, labels):
        d.box(x, 50, 140, 56, t, s)
    for x in xs[:-1]:
        d.arrow([(x + 140, 78), (x + 164, 78)])
    d.note(500, 132, 'responsável nunca resolve para aluno', to=(560, 108))
    d.note(170, 10, 'regra escrita depois de consultar os dados reais', to=(240, 48))
    return d.svg()

def k6():
    d = D(960, 230, 'Teste de carga que encontrou o gargalo no código',
          'O k6 gera carga na API NestJS; o interceptor de auditoria tem custo em toda requisição e o PostgreSQL recebe consultas N+1.')
    d.box(20, 90, 150, 56, 'k6', 'rampa de usuários')
    d.box(240, 90, 180, 56, 'API NestJS')
    d.box(490, 90, 190, 56, 'Interceptor', 'auditoria')
    d.box(750, 90, 190, 56, 'PostgreSQL')
    d.arrow([(170, 118), (234, 118)])
    d.arrow([(420, 118), (484, 118)])
    d.arrow([(680, 118), (744, 118)])
    d.note(490, 30, 'custo extra em toda requisição', to=(585, 88))
    d.note(750, 170, 'consultas N+1', to=(845, 148))
    d.note(240, 170, 'saturação de CPU cedo', to=(330, 148))
    return d.svg()

def ranking():
    d = D(960, 270, 'Ranking antes e depois da migração para Redis',
          'Antes, uma função Lambda recalculava o ranking inteiro a partir do banco. Depois, cada pontuação entra num sorted set do Redis e o ranking é lido direto.')
    for y, label, mid, msub, end, esub, note in [
        (45, 'Antes', 'AWS Lambda', 'recalcula tudo', 'Banco', None, 'custo cresce com os jogadores'),
        (175, 'Depois', 'Redis', 'sorted set', 'Ranking', 'leitura direta', 'cerca de US$ 300 a menos por mês')]:
        d.rowlabel(20, y - 15, label)
        d.box(20, y, 150, 56, 'Pontuação')
        d.box(230, y, 180, 56, mid, msub)
        d.box(470, y, 170, 56, end, esub)
        d.arrow([(170, y + 28), (224, y + 28)])
        d.arrow([(410, y + 28), (464, y + 28)])
        d.note(670, y + 21, note)
    return d.svg()

def hero_mobile():
    d = D(340, 440, 'Visão geral da plataforma educacional em que trabalho',
          'Painel web e app passam pela Cloudflare até a API NestJS na GCP, que usa Keycloak, PostgreSQL e Redis.')
    d.box(15, 15, 145, 52, 'Painel web', 'Angular', node='web')
    d.box(180, 15, 145, 52, 'App', 'Flutter', node='app')
    d.box(90, 110, 160, 52, 'Cloudflare', 'proxy e Access', node='cf')
    d.arrow([(87, 67), (87, 88), (140, 88), (140, 104)], edge='web-cf')
    d.arrow([(252, 67), (252, 88), (200, 88), (200, 104)], edge='app-cf')
    d.zone(5, 190, 330, 200, 'GCP, provisionada com Terraform')
    d.box(90, 225, 160, 52, 'API NestJS', 'réplicas no Swarm', node='api')
    d.arrow([(170, 162), (170, 219)], edge='cf-api')
    d.box(12, 320, 100, 52, 'Keycloak', 'SSO', node='kc')
    d.box(120, 320, 100, 52, 'PostgreSQL', 'Cloud SQL', node='pg')
    d.box(228, 320, 100, 52, 'Redis', 'cache', node='redis')
    d.arrow([(125, 277), (72, 314)], edge='api-kc')
    d.arrow([(170, 277), (170, 314)], edge='api-pg')
    d.arrow([(215, 277), (268, 314)], edge='api-redis')
    d.note(10, 402, 'login único entregue em 14 dias')
    return d.svg('drawing drawing-hero-m')
