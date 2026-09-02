# Anatomia da Stack Corporativa

Referência executiva de arquitetura de sistemas corporativos. Dezessete categorias, das
máquinas do chão de fábrica ao razão contábil, descritas por aquilo que produzem — não pelas
siglas que carregam.

**Página publicada:** https://al-ramos.github.io/amr-arquitetura/

## O que o documento cobre

Cada ficha responde a seis perguntas sobre o sistema:

| Dimensão | Pergunta |
|---|---|
| Propósito | Por que este sistema existe? Que problema de negócio ele resolve? |
| Capacidades | O que as pessoas efetivamente fazem nele? |
| Módulos | De quais blocos ele é feito? |
| Automação | O que roda sem intervenção humana? |
| Integrações | Com quem ele conversa? |
| Valor | O que sobra de resultado tangível? |

## Os cinco domínios

| Domínio | Sistemas |
|---|---|
| **Manufatura** | MES |
| **Gestão corporativa** | ERP · CRM · HCM · MDM |
| **Cadeia de suprimentos** | SCM · WMS · OMS · P2P · PIM |
| **Financeiro e fiscal** | AP/AR · Fiscal BR |
| **Dados e TI** | BI · ETL · iPaaS · BPM · IAM |

O documento abre com um diagrama do trajeto de um pedido pela arquitetura — da oportunidade
comercial à nota fiscal autorizada — porque o que dá valor à arquitetura não são as caixas, e
sim o caminho entre elas.

## Estrutura

```
index.html   página completa, sem dependências além das fontes do Google Fonts
```

Nenhum build, nenhum framework. O arquivo é autocontido: todo o CSS e o JavaScript de navegação
estão inline, e o diagrama é SVG escrito à mão. Funciona em tema claro e escuro conforme a
preferência do sistema do leitor.

## Publicação

Servido por GitHub Pages a partir da raiz do branch `main`. Qualquer push atualiza a página.

## Nota

As plataformas citadas são as referências de mercado de cada categoria, escolhidas por
representatividade e não por recomendação. A opção certa em cada camada depende de porte, setor
regulatório e do que já existe instalado.
