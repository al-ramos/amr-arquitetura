# Anatomia da Stack Corporativa

Referência de arquitetura de sistemas corporativos. Dezessete categorias, das máquinas do chão
de fábrica ao razão contábil, descritas por aquilo que produzem — não pelas siglas que carregam.

**Página publicada:** https://al-ramos.github.io/amr-arquitetura/

## Dois níveis de leitura

**O índice** (`index.html`) traz as 17 fichas, cada uma com propósito, capacidades, módulos,
automação, integrações e valor. É a visão comparável: as fichas têm tamanho semelhante de
propósito, para que ERP e WMS possam ser lidos lado a lado.

**Os dossiês** (`/mes/`, e demais conforme forem escritos) aprofundam um sistema por vez —
modelo de dados, jornadas passo a passo, casos de borda, arquitetura de referência e
especificidade brasileira. Cada ficha do índice linka para o seu dossiê.

## Estrutura

```
index.html          índice executivo com as 17 fichas
assets/style.css    estilo compartilhado por todas as páginas
content/*.md        fonte dos dossiês — um arquivo por sistema
build.py            gera as páginas dos dossiês a partir de content/
<slug>/index.html   dossiê publicado (gerado, não editar à mão)
```

## Como escrever um dossiê

Crie `content/<slug>.md` com o cabeçalho:

```yaml
---
sigla: WMS · Warehouse Management System
titulo: Gestão de armazém
plataforma: Manhattan Active WM
dominio: Cadeia de suprimentos
cor: sup          # fab | corp | sup | fin | ti
resumo: uma frase que descreve o sistema
---
```

Convenções no corpo:

| Marcação | Efeito |
|---|---|
| `## Título` | Seção, entra no índice lateral automaticamente |
| `::: nota` … `:::` | Caixa de destaque |
| `::: interno` … `:::` | Só aparece na versão interna |
| `{: .jornada }` após uma lista numerada | Vira jornada passo a passo, com numeração destacada |
| Tabela Markdown | Tabela formatada |
| `<figure>` com SVG inline | Diagrama |

Depois rode:

```bash
python build.py          # todos
python build.py wms      # só um
```

O script gera duas saídas por dossiê: a pública em `<slug>/index.html`, dentro do repositório,
e a interna em `../Arquitetura-<SLUG>-INTERNO.html`, **fora** do repositório — autocontida, com
o CSS embutido, contendo os blocos `::: interno`.

Dependência: `pip install markdown`.

## Publicação

GitHub Pages a partir da raiz do branch `main`. Qualquer push atualiza o site. Não há CI: rode
`build.py` antes de commitar quando alterar um `.md`.

## Nota

As plataformas citadas são referências de mercado de cada categoria, escolhidas por
representatividade e não por recomendação. O conteúdo descreve o funcionamento do tipo de
sistema; nomes de módulo, licenciamento e limites técnicos de produto devem ser conferidos na
documentação do fornecedor.
