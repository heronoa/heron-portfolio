# heron-portfolio

Portfólio pessoal em https://heronoa.com.br. Uma página única em HTML e CSS, com JavaScript só como melhoria (o site funciona sem ele), servida pelo Cloudflare Workers Static Assets no plano gratuito.

## Estrutura

```
site/
  index.html                  a página (gerada por tools/build.py)
  styles.css                  tokens e componentes do design system arena
  theme.js                    aplica o tema salvo antes de pintar a página
  site.js                     requisição ao vivo, replays, ampliar desenho, carrosséis, filtros, tema e métricas
  404.html
  fonts/                      Chakra Petch e Atkinson Hyperlegible, servidas pelo próprio site (licença OFL)
  foto.jpg                    sua foto, 800 x 1000 px (4:5)
  heron-amaral-curriculo.pdf  currículo público, sem telefone
  og.png                      imagem de prévia ao compartilhar o link
  favicon.svg, apple-touch-icon.png, robots.txt, sitemap.xml
  _headers                    CSP, HSTS e afins
tools/
  build.py                    conteúdo do site (casos, projetos, experiência) e montagem do index.html
  replays.py                  desenhos dos estudos de caso, marco a marco
  diagrams.py                 desenho principal da arquitetura (versões desktop e celular)
DESIGN-SYSTEM.md              design system arena: cores, tipografia, componentes e regras
wrangler.jsonc                Worker e domínio próprio
.github/workflows/deploy.yml  deploy a cada push em main
```

## Editar o conteúdo

Textos de casos, projetos e experiência ficam em `tools/build.py`; os desenhos de cada marco dos casos, em `tools/replays.py`. Depois de editar:

```bash
python3 tools/build.py   # regenera site/index.html
```

Cada elemento de um replay declara em quais marcos aparece (`show="0 1"`, onde 0 é Antes, 1 Problema, 2 Decisão e 3 Depois) e em quais fica esmaecido (`dim`). Sem JavaScript, o caso mostra o estado final e a narração completa em lista.

Os textos de "Rodar uma requisição" ficam no array `STEPS` em `site/site.js`; cada etapa percorre uma seta (`data-edge`) e acende um nó (`data-node`) do desenho principal.

## Métricas de visita

O site usa o Cloudflare Web Analytics (gratuito, sem cookies), mas só carrega o script quando há um token configurado:

1. No painel da Cloudflare, em Analytics e Logs > Web Analytics, adicione o site `heronoa.com.br` e copie o token.
2. Cole o token em `<meta name="cf-analytics-token" content="">` no `index.html`.

Sem token, nenhum script de terceiros é carregado. A CSP em `_headers` já libera `static.cloudflareinsights.com` (script) e `cloudflareinsights.com` (envio dos dados).

## Rodar localmente

```bash
npx wrangler dev
```

## Primeira subida

1. Adicione `heronoa.com.br` como site no painel da Cloudflare (plano Free) e troque os servidores DNS no Registro.br pelos dois nameservers indicados.
2. Espere a zona ficar ativa (`dig NS heronoa.com.br +short` deve mostrar os servidores `*.ns.cloudflare.com`).
3. Rode `npx wrangler login` e `npx wrangler deploy`. A rota `custom_domain` cria o registro DNS e o certificado.

## Deploy contínuo

Crie um API token com o template "Edit Cloudflare Workers", restrito à sua conta e à zona `heronoa.com.br`, e cadastre os secrets `CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID` no repositório.

## Ao atualizar o conteúdo

- Substitua `site/foto.jpg` pela sua foto antes da primeira publicação (proporção 4:5, idealmente 800 x 1000 px).

- Troque a data em "Revisão de" no carimbo e o `lastmod` do `sitemap.xml`.
- Ao trocar o currículo, gere a versão pública sem telefone.
- Se alguma página passar a fazer requisições (o `/health` do Crash Arena, por exemplo), libere o domínio em `connect-src` no `_headers`.
