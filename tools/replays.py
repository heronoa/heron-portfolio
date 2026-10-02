# Desenhos dos replays: cada elemento declara em quais marcos (0 a 3) aparece.
from html import escape as e

class R:
    def __init__(s, title):
        s.title, s.parts = title, []
    @staticmethod
    def _init(show, dim):
        c = ''
        if show is not None and '3' not in show.split(): c += ' off'
        if dim is not None and '3' in dim.split(): c += ' dim'
        return c
    def _attrs(s, show, dim):
        a = ''
        if show is not None: a += f' data-show="{show}"'
        if dim is not None: a += f' data-dim="{dim}"'
        return a
    def box(s, x, y, w, h, t, sub=None, cls='', show=None, dim=None):
        s.parts.append(f'<g class="r-node {cls}{s._init(show, dim)}"{s._attrs(show, dim)}><rect class="r-box" x="{x}" y="{y}" width="{w}" height="{h}"/>')
        if sub:
            s.parts.append(f'<text class="r-t" x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle">{e(t)}</text>'
                           f'<text class="r-s" x="{x+w/2}" y="{y+h/2+17}" text-anchor="middle">{e(sub)}</text>')
        else:
            s.parts.append(f'<text class="r-t" x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle">{e(t)}</text>')
        s.parts.append('</g>')
    def listbox(s, x, y, w, h, title, items, cls='', show=None, dim=None):
        s.parts.append(f'<g class="r-node {cls}{s._init(show, dim)}"{s._attrs(show, dim)}><rect class="r-box" x="{x}" y="{y}" width="{w}" height="{h}"/>'
                       f'<text class="r-t" x="{x+16}" y="{y+30}">{e(title)}</text>')
        for i, it in enumerate(items):
            s.parts.append(f'<text class="r-s" x="{x+16}" y="{y+62+i*28}"><tspan class="r-num">{i+1}</tspan>  {e(it)}</text>')
        s.parts.append('</g>')
    def arrow(s, pts, show=None, dim=None, dashed=False):
        p = ' '.join(f'{a},{b}' for a, b in pts)
        cls = ('r-arrow r-dash' if dashed else 'r-arrow') + s._init(show, dim)
        s.parts.append(f'<polyline class="{cls}"{s._attrs(show, dim)} points="{p}" marker-end="url(#mk-ink)"/>')
    def event(s, x, y, lines, show, anchor='start'):
        ts = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else 20}">{e(l)}</tspan>' for i, l in enumerate(lines))
        s.parts.append(f'<text class="r-ev{s._init(show, None)}" data-show="{show}" x="{x}" y="{y}" text-anchor="{anchor}">{ts}</text>')
    def svg(s, idx):
        return (f'<svg class="replay-svg state-3" viewBox="0 0 760 340" role="img" aria-labelledby="rt-{idx}">'
                f'<title id="rt-{idx}">{e(s.title)}</title>' + ''.join(s.parts) + '</svg>')

def sso():
    d = R('Login único com Keycloak: dos logins próprios à fachada com migração no primeiro acesso')
    d.box(20, 140, 160, 62, 'Clientes', 'web e mobile')
    d.arrow([(180, 171), (224, 171)])
    d.box(230, 140, 180, 62, 'API NestJS', 'login próprio', cls='n-prob', show='0 1')
    d.box(230, 140, 180, 62, 'API NestJS', 'fachada de login', show='2 3')
    d.box(230, 266, 180, 62, 'Base legada', 'usuários e senhas')
    d.arrow([(320, 202), (320, 260)], show='0 1')
    d.box(450, 140, 170, 62, 'Keycloak', 'intermediador', cls='n-new', show='2 3')
    d.arrow([(410, 171), (444, 171)], show='2 3')
    d.arrow([(410, 297), (535, 297), (535, 208)], show='2 3', dashed=True)
    d.box(650, 60, 100, 56, 'Secretaria', 'realm', show='3')
    d.box(650, 226, 100, 56, 'Escolas', 'realm', show='3')
    d.arrow([(620, 160), (635, 160), (635, 88), (644, 88)], show='3')
    d.arrow([(620, 182), (635, 182), (635, 254), (644, 254)], show='3')
    d.event(440, 70, ['edital: login único em 14 dias,', 'sem quebrar nenhum cliente'], '1')
    d.event(230, 110, ['a fachada mantém o contrato dos clientes'], '2')
    d.event(20, 270, ['migração no primeiro login,', 'sem reset de senha'], '3')
    return d

def email():
    d = R('Vínculo de contas por e-mail: da busca ingênua à regra em quatro passos')
    d.box(20, 140, 160, 62, 'E-mail Google', 'login social')
    d.arrow([(180, 171), (234, 171)])
    d.box(240, 140, 200, 62, 'Busca por e-mail', 'primeiro que bater', show='0 1')
    d.listbox(240, 50, 240, 170, 'Regra de resolução', ['normalizar', 'descartar sentinelas', 'dono do e-mail', 'desempate por contagem'], cls='n-new', show='2 3')
    d.arrow([(440, 171), (514, 171)], show='0 1')
    d.arrow([(480, 135), (514, 135)], show='2 3')
    d.box(520, 140, 210, 62, 'Usuário', 'vinculado', show='0')
    d.box(520, 140, 210, 62, 'Aluno', 'conta errada', cls='n-prob', show='1')
    d.box(520, 104, 210, 62, 'Responsável', 'a própria conta', cls='n-ok', show='2 3')
    d.event(240, 258, ['o e-mail do responsável estava', 'no cadastro do aluno'], '1')
    d.event(240, 258, ['escrita depois de consultar', 'os dados reais'], '2')
    d.event(520, 210, ['responsável nunca resolve', 'para o cadastro de uma criança'], '3')
    return d

def k6():
    d = R('Teste de carga: da hipótese de falta de máquina aos gargalos no código')
    d.box(20, 140, 140, 62, 'k6', 'rampa de usuários', cls='n-new', show='2 3')
    d.arrow([(160, 171), (204, 171)], show='2 3', dashed=False)
    d.box(210, 140, 160, 62, 'API NestJS', cls='n-hot')
    d.box(405, 140, 165, 62, 'Interceptor', 'auditoria', cls='n-hot')
    d.box(605, 140, 145, 62, 'PostgreSQL', cls='n-hot')
    d.arrow([(370, 171), (399, 171)])
    d.arrow([(570, 171), (599, 171)])
    d.event(210, 100, ['pedido no ar: mais máquina'], '1')
    d.event(405, 100, ['custo extra em toda requisição'], '3')
    d.event(210, 240, ['saturação de CPU cedo'], '3')
    d.event(750, 240, ['consultas N+1'], '3', anchor='end')
    return d

def ranking():
    d = R('Ranking do jogo: do recálculo em Lambda ao sorted set no Redis')
    d.box(20, 140, 150, 62, 'Pontuação', 'fim da partida')
    d.box(290, 40, 190, 62, 'AWS Lambda', 'recalcula tudo', cls='n-prob', show='0 1 2', dim='2')
    d.box(590, 40, 150, 62, 'Banco', show='0 1 2', dim='2')
    d.box(590, 236, 150, 62, 'Ranking', 'lido pelo jogo')
    d.box(290, 236, 190, 62, 'Redis', 'sorted set', cls='n-new', show='2 3')
    d.arrow([(170, 160), (230, 160), (230, 71), (284, 71)], show='0 1 2', dim='2')
    d.arrow([(480, 71), (584, 71)], show='0 1 2', dim='2')
    d.arrow([(665, 102), (665, 230)], show='0 1')
    d.arrow([(170, 182), (230, 182), (230, 267), (284, 267)], show='2 3')
    d.arrow([(480, 267), (584, 267)], show='3')
    d.event(300, 140, ['a cada partida, o ranking', 'inteiro é recalculado'], '1')
    d.event(300, 140, ['a ordem é mantida', 'a cada pontuação nova'], '2')
    d.event(300, 140, ['leitura direta do topo,', 'cerca de US$ 300 a menos por mês'], '3')
    return d
