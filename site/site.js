// Melhorias progressivas do portfólio. Sem este arquivo o site continua completo:
// casos mostram o estado final e a narração em lista, carrosséis rolam por toque e teclado,
// o tema segue o padrão escuro.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };

  /* ---------- tema ---------- */
  function setupTheme() {
    var btn = $('.theme-btn'); if (!btn) return;
    var root = document.documentElement, mq = window.matchMedia('(prefers-color-scheme: dark)');
    var fallback = root.getAttribute('data-default-theme');
    function eff() { return root.getAttribute('data-theme') || fallback || (mq.matches ? 'dark' : 'light'); }
    function render() {
      var dark = eff() === 'dark';
      btn.setAttribute('aria-pressed', String(dark));
      $('.theme-label', btn).textContent = dark ? btn.getAttribute('data-to-light') : btn.getAttribute('data-to-dark');
    }
    btn.addEventListener('click', function () {
      var next = eff() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      render();
    });
    render();
  }

  /* ---------- requisição ao vivo ---------- */
  var STEPS = [
    { node: 'web', text: 'O painel web envia o login.' },
    { edge: 'web-cf', node: 'cf', text: 'A Cloudflare encerra o HTTPS e aplica as regras de acesso.' },
    { edge: 'cf-api', node: 'api', text: 'Uma réplica da API NestJS no Swarm recebe a requisição.' },
    { edge: 'api-kc', node: 'kc', text: 'O Keycloak confere as credenciais e emite os tokens.' },
    { edge: 'api-kc', back: true, node: 'api', text: 'A API recebe os tokens.' },
    { edge: 'api-pg', node: 'pg', text: 'O PostgreSQL devolve perfil e permissões.' },
    { edge: 'api-pg', back: true, node: 'api' },
    { edge: 'api-redis', node: 'redis', text: 'O Redis guarda o que será lido de novo.' },
    { edge: 'api-redis', back: true, node: 'api' },
    { edge: 'cf-api', back: true, node: 'cf' },
    { edge: 'web-cf', back: true, node: 'web', text: 'A resposta chega ao painel.' },
    { node: 'graf', text: 'Latência e erros de cada etapa viram métrica no Grafana.' }
  ];
  function setupLive() {
    var btn = $('.run'); if (!btn) return;
    var list = $('.log ol'), count = $('.log-count'), n = 0, running = false;
    function svg() { return $$('.stage svg').filter(function (s) { return s.getBoundingClientRect().width > 0; })[0]; }
    function travel(s, poly, back) {
      return new Promise(function (done) {
        poly.classList.add('lit');
        poly.setAttribute('marker-end', 'url(#mk-red)');
        if (reduce) return done();
        var len = poly.getTotalLength(), c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('r', '6'); c.setAttribute('class', 'packet'); s.appendChild(c);
        var t0 = null, dur = 420;
        function frame(t) {
          if (!t0) t0 = t;
          var k = Math.min(1, (t - t0) / dur), p = poly.getPointAtLength((back ? 1 - k : k) * len);
          c.setAttribute('cx', p.x); c.setAttribute('cy', p.y);
          if (k < 1) requestAnimationFrame(frame); else { c.remove(); done(); }
        }
        requestAnimationFrame(frame);
      });
    }
    function log(text) {
      if (!text) return;
      var e = $('.empty', list); if (e) e.remove();
      n++;
      var li = document.createElement('li'), sp = document.createElement('span');
      sp.textContent = n; li.appendChild(sp); li.appendChild(document.createTextNode(text)); list.appendChild(li);
      count.textContent = n + (n === 1 ? ' evento' : ' eventos');
      list.scrollTop = list.scrollHeight;
    }
    btn.addEventListener('click', async function () {
      if (running) return;
      running = true; btn.disabled = true; btn.textContent = 'Requisição em andamento';
      var s = svg(); list.innerHTML = ''; n = 0; count.textContent = '';
      $$('.d-node', s).forEach(function (g) { g.classList.remove('hot', 'done'); });
      $$('[data-edge]', s).forEach(function (a) { a.classList.remove('lit'); a.setAttribute('marker-end', 'url(#mk-ink)'); });
      for (var i = 0; i < STEPS.length; i++) {
        var st = STEPS[i];
        if (st.edge) { var p = $('[data-edge="' + st.edge + '"]', s); if (p) await travel(s, p, st.back); }
        var g = $('[data-node="' + st.node + '"]', s);
        if (!g) continue;
        $$('.d-node.hot', s).forEach(function (h) { h.classList.remove('hot'); h.classList.add('done'); });
        g.classList.add('hot'); log(st.text);
        await wait(reduce ? 0 : (st.text ? 380 : 80));
      }
      running = false; btn.disabled = false; btn.textContent = 'Rodar de novo';
    });
  }

  /* ---------- replays ---------- */
  function setupReplay(rp) {
    var svg = $('.replay-svg', rp), marks = $$('.timeline button', rp), fill = $('.timeline .fill', rp);
    var narr = $('.narration', rp), texts = $$('.narr-src li', rp).map(function (li) { return li.textContent; });
    var prev = $('.prev', rp), next = $('.next', rp), play = $('.play', rp), last = marks.length - 1;
    var cur = 0, timer = null;
    function set(i) {
      cur = i;
      svg.setAttribute('class', 'replay-svg state-' + i);
      $$('[data-show], [data-dim]', svg).forEach(function (el) {
        var show = el.getAttribute('data-show'), dim = el.getAttribute('data-dim');
        el.classList.toggle('off', !!show && show.split(' ').indexOf(String(i)) < 0);
        el.classList.toggle('dim', !!dim && dim.split(' ').indexOf(String(i)) >= 0);
      });
      marks.forEach(function (b, j) { b.setAttribute('aria-current', j === i ? 'step' : 'false'); b.classList.toggle('past', j < i); });
      fill.style.width = (i / marks.length * 100) + '%';
      narr.textContent = texts[i] || '';
      prev.disabled = i === 0; next.disabled = i === last;
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } play.textContent = 'Assistir'; }
    marks.forEach(function (b) { b.addEventListener('click', function () { stop(); set(Number(b.getAttribute('data-step'))); }); });
    prev.addEventListener('click', function () { stop(); if (cur > 0) set(cur - 1); });
    next.addEventListener('click', function () { stop(); if (cur < last) set(cur + 1); });
    play.addEventListener('click', function () {
      if (timer) return stop();
      set(0); play.textContent = 'Pausar';
      timer = setInterval(function () { if (cur >= last) return stop(); set(cur + 1); }, reduce ? 4000 : 2600);
    });
    set(0);
  }

  /* ---------- ampliar ---------- */
  function setupZoom() {
    var dlg = $('dialog.zoom');
    if (!dlg || typeof dlg.showModal !== 'function') { $$('.zoom-btn').forEach(function (b) { b.remove(); }); return; }
    var body = $('.zoom-body', dlg), title = $('.zoom-title', dlg), scale = 1, base = 0, svg = null;
    function apply() { if (svg) svg.style.width = Math.round(base * scale) + 'px'; }
    $$('.zoom-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var rp = btn.closest('.replay'), src = $('.replay-svg', rp);
        svg = src.cloneNode(true);
        svg.removeAttribute('aria-labelledby');
        $$('[id]', svg).forEach(function (el) { el.removeAttribute('id'); });
        svg.setAttribute('aria-label', $('title', src).textContent);
        body.innerHTML = ''; body.appendChild(svg);
        var mark = $('.timeline [aria-current="step"]', rp);
        title.textContent = $('h3', rp).textContent + (mark ? ', ' + mark.textContent.toLowerCase() : '');
        scale = 1; dlg.showModal();
        var cs = getComputedStyle(body);
        base = Math.max(body.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), 720);
        apply();
      });
    });
    $$('[data-zoom]', dlg).forEach(function (b) {
      b.addEventListener('click', function () { scale = Math.min(3, Math.max(.6, scale * (b.getAttribute('data-zoom') === '1' ? 1.25 : .8))); apply(); });
    });
    $('.zoom-close', dlg).addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }

  /* ---------- carrosséis ---------- */
  function slides(t) { return Array.prototype.slice.call(t.children); }
  function current(t) {
    var best = 0, dist = Infinity;
    slides(t).forEach(function (s, i) { var d = Math.abs(s.offsetLeft - t.offsetLeft - t.scrollLeft); if (d < dist) { dist = d; best = i; } });
    return best;
  }
  function go(t, i) { var s = slides(t)[i]; if (s) t.scrollTo({ left: s.offsetLeft - t.offsetLeft, behavior: reduce ? 'auto' : 'smooth' }); }
  function setupCarousel(t) {
    var ctrl = $('.car-ctrl[data-for="' + t.id + '"]'), tabs = $('.car-tabs[data-for="' + t.id + '"]');
    var count = ctrl && $('.car-count', ctrl), prev = ctrl && $('[data-dir="-1"]', ctrl), next = ctrl && $('[data-dir="1"]', ctrl);
    var total = slides(t).length;
    function update() {
      var i = current(t);
      if (count) count.textContent = (i + 1) + ' de ' + total;
      if (prev) prev.disabled = t.scrollLeft <= 4;
      if (next) next.disabled = t.scrollLeft + t.clientWidth >= t.scrollWidth - 4;
      if (tabs) $$('a', tabs).forEach(function (a, j) { a.setAttribute('aria-current', j === i ? 'true' : 'false'); });
    }
    if (ctrl) ctrl.addEventListener('click', function (e) {
      var b = e.target.closest('.car-btn');
      if (b) go(t, Math.max(0, Math.min(total - 1, current(t) + Number(b.getAttribute('data-dir')))));
    });
    if (tabs) tabs.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      var i = slides(t).indexOf($(a.getAttribute('href')));
      if (i < 0 || getComputedStyle(t).overflowX === 'visible') return;
      e.preventDefault(); go(t, i);
    });
    t.addEventListener('keydown', function (e) {
      if (e.target !== t) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); go(t, Math.min(total - 1, current(t) + 1)); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(t, Math.max(0, current(t) - 1)); }
    });
    var tm; t.addEventListener('scroll', function () { clearTimeout(tm); tm = setTimeout(update, 60); }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- filtros de projetos ---------- */
  function setupFilters() {
    var btns = $$('.filters button'), rows = $$('.server'), empty = $('.servers-empty');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter'), shown = 0;
        btns.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        rows.forEach(function (r) {
          var ok = f === 'todos' || r.getAttribute('data-tags').split(' ').indexOf(f) >= 0;
          r.hidden = !ok; if (ok) shown++;
        });
        if (empty) empty.hidden = shown > 0;
      });
    });
  }

  /* ---------- métricas ---------- */
  function setupAnalytics() {
    var m = $('meta[name="cf-analytics-token"]'), token = m && m.getAttribute('content');
    if (!token) return;
    var s = document.createElement('script');
    s.defer = true; s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    s.setAttribute('data-cf-beacon', JSON.stringify({ token: token }));
    document.head.appendChild(s);
  }

  document.addEventListener('DOMContentLoaded', function () {
    setupTheme(); setupLive();
    $$('.replay').forEach(setupReplay);
    setupZoom();
    $$('.carousel, .strip').forEach(setupCarousel);
    setupFilters(); setupAnalytics();
  });
})();
