# -*- coding: utf-8 -*-
"""
Gera as páginas de aprofundamento a partir dos arquivos em content/.

Cada .md vira duas saídas:
  <slug>/index.html            versão pública, dentro do repositório
  ../Arquitetura-<SLUG>-INTERNO.html   versão interna, fora do repositório

Blocos ':::  interno ... :::' só entram na versão interna.

Uso:  python build.py [slug ...]     (sem argumento, gera todos)
"""
import os
import re
import sys
import html as H

try:
    import markdown
except ImportError:
    sys.exit("faltando dependência: pip install markdown")

RAIZ = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(RAIZ, "content")
INTERNO_DIR = os.path.abspath(os.path.join(RAIZ, ".."))

DOMINIOS = {
    "fab": "Manufatura",
    "corp": "Gestão corporativa",
    "sup": "Cadeia de suprimentos",
    "fin": "Financeiro e fiscal",
    "ti": "Dados e TI",
}

EXT = ["tables", "attr_list", "sane_lists", "md_in_html"]


def front_matter(txt):
    """Separa o cabeçalho --- ... --- do corpo."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m:
        raise ValueError("arquivo sem front matter")
    meta = {}
    for linha in m.group(1).split("\n"):
        if not linha.strip():
            continue
        k, _, v = linha.partition(":")
        meta[k.strip()] = v.strip()
    return meta, m.group(2)


def blocos(corpo, interno):
    """Trata ':::  tipo ... :::'. Remove os de tipo 'interno' na versão pública."""
    pat = re.compile(r"^::: *(\w+)\n(.*?)\n:::\s*$", re.M | re.S)

    def sub(m):
        tipo, dentro = m.group(1), m.group(2)
        if tipo == "interno":
            if not interno:
                return ""
            return '<div class="bloco-interno" markdown="1">\n%s\n</div>' % dentro
        return '<aside class="cx cx-%s" markdown="1">\n%s\n</aside>' % (tipo, dentro)

    anterior = None
    while anterior != corpo:
        anterior = corpo
        corpo = pat.sub(sub, corpo)
    return corpo


def indice(html):
    """Monta o índice lateral a partir dos <h2>, atribuindo id a cada um."""
    itens = []
    contador = [0]

    def sub(m):
        contador[0] += 1
        texto = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        slug = "s%d" % contador[0]
        itens.append((slug, texto))
        return '<h2 id="%s">%s</h2>' % (slug, m.group(1))

    html = re.sub(r"<h2>(.*?)</h2>", sub, html, flags=re.S)
    nav = "\n".join(
        '        <li><a href="#%s"><span class="num">%02d</span>%s</a></li>' % (s, i + 1, H.escape(t))
        for i, (s, t) in enumerate(itens)
    )
    return html, nav


TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{resumo_attr}">
<meta name="color-scheme" content="light dark">
<title>{titulo} — dossiê</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
{estilo}
</head>
<body class="dossie" style="--dom: var(--c-{cor})">

<header class="masthead">
  <div class="masthead-inner">
    <a class="voltar" href="{home}">&larr; Anatomia da Stack Corporativa</a>
    <div class="eyebrow">{dominio} &middot; dossiê de aprofundamento</div>
    <h1>{titulo}</h1>
    <p class="standfirst">{resumo}</p>
    <div class="dossie-meta">
      <span class="sigla">{sigla}</span>
      <span class="platform">{plataforma}</span>
    </div>
  </div>
</header>

<div class="shell">
  <nav class="rail" aria-label="Seções deste dossiê">
    <div class="rail-title">Neste dossiê</div>
    <ul class="rail-secoes">
{nav}
    </ul>
  </nav>

  <main class="prosa">
{corpo}
    <p class="note">{rodape}</p>
  </main>
</div>

<script>
  (function () {{
    var links = Array.prototype.slice.call(document.querySelectorAll('.rail-secoes a'));
    var map = {{}}, alvos = [];
    links.forEach(function (a) {{
      var el = document.querySelector(a.getAttribute('href'));
      if (el) {{ map[el.id] = a; alvos.push(el); }}
    }});
    if (!('IntersectionObserver' in window) || !alvos.length) return;
    var io = new IntersectionObserver(function (es) {{
      es.forEach(function (e) {{
        if (e.isIntersecting) {{
          links.forEach(function (l) {{ l.classList.remove('on'); }});
          map[e.target.id].classList.add('on');
        }}
      }});
    }}, {{ rootMargin: '-12% 0px -70% 0px', threshold: 0 }});
    alvos.forEach(function (t) {{ io.observe(t); }});
  }})();
</script>
</body>
</html>
"""

RODAPE_PUB = ("As plataformas citadas são referências de mercado da categoria, não recomendações. "
              "O conteúdo descreve o funcionamento do tipo de sistema; nomes de módulo, licenciamento "
              "e limites técnicos de produto devem ser conferidos na documentação do fornecedor.")
RODAPE_INT = ("Versão interna — contém a avaliação de posição do AMR Eco System. "
              "As plataformas citadas são referências de mercado da categoria. Nomes de módulo, "
              "licenciamento e limites de produto devem ser conferidos na documentação do fornecedor.")


def gerar(slug, interno):
    origem = os.path.join(CONTENT, slug + ".md")
    meta, corpo = front_matter(open(origem, encoding="utf-8").read())
    corpo = blocos(corpo, interno)
    html = markdown.markdown(corpo, extensions=EXT)
    html, nav = indice(html)
    html = "\n".join("    " + l for l in html.split("\n"))

    # a versão interna vive fora do repositório: embute o CSS para ficar autônoma
    if interno:
        css = open(os.path.join(RAIZ, "assets", "style.css"), encoding="utf-8").read()
        estilo = "<style>\n%s</style>" % css
    else:
        estilo = '<link rel="stylesheet" href="../assets/style.css">'

    pagina = TEMPLATE.format(
        estilo=estilo,
        titulo=H.escape(meta["titulo"]),
        sigla=meta["sigla"],
        plataforma=meta["plataforma"],
        dominio=DOMINIOS.get(meta.get("cor"), meta.get("dominio", "")),
        cor=meta.get("cor", "ti"),
        resumo=H.escape(meta["resumo"]),
        resumo_attr=H.escape(meta["resumo"], quote=True),
        corpo=html,
        nav=nav,
        home=("Arquitetura-AMR-Completo.html#" + slug) if interno else ("../index.html#" + slug),
        rodape=RODAPE_INT if interno else RODAPE_PUB,
    )

    if interno:
        destino = os.path.join(INTERNO_DIR, "Arquitetura-%s-INTERNO.html" % slug.upper())
    else:
        os.makedirs(os.path.join(RAIZ, slug), exist_ok=True)
        destino = os.path.join(RAIZ, slug, "index.html")
    open(destino, "w", encoding="utf-8", newline="\n").write(pagina)
    palavras = len(re.sub(r"<[^>]+>", " ", html).split())
    print("  %-8s %-9s %6d bytes  %5d palavras  %s"
          % (slug, "interno" if interno else "público", len(pagina), palavras, destino))
    return destino


if __name__ == "__main__":
    alvos = sys.argv[1:] or sorted(
        f[:-3] for f in os.listdir(CONTENT) if f.endswith(".md"))
    print("gerando %d dossiê(s):" % len(alvos))
    for slug in alvos:
        gerar(slug, interno=False)
        gerar(slug, interno=True)
