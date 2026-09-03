---
sigla: Fiscal BR · Compliance tributário brasileiro
titulo: Emissão e escrituração fiscal
plataforma: TOTVS Fiscal · Sovos · Synchro
dominio: Financeiro e fiscal
cor: fin
resumo: A única camada da arquitetura em que a falha não gera ineficiência — gera multa, crédito perdido e caminhão parado na estrada.
---

## O problema numa operação real

Uma indústria com fábrica em Minas, centro de distribuição em São Paulo e vendas para dezoito estados. Quatrocentas notas por dia, mix de venda direta, transferência entre filiais, remessa para industrialização em terceiro e devolução. Regime de lucro real.

Cada uma dessas quatrocentas notas exige uma decisão tributária composta: qual CFOP, qual CST, qual alíquota de ICMS considerando a origem, o destino, o tipo de destinatário e o produto; se há substituição tributária e quem recolhe; se há diferencial de alíquota; qual o IPI; qual o regime de PIS e COFINS para aquele item. Errar não é uma questão de estilo — a nota é rejeitada pela SEFAZ na hora, ou é autorizada errada e vira passivo.

Sem sistema fiscal dedicado, isso acontece de três formas, todas ruins:

**Decisão no cadastro do item.** Alguém amarra o CFOP no produto e reza para que a operação seja sempre a mesma. Funciona até a primeira venda interestadual para consumidor final, a primeira transferência, a primeira devolução.

**Decisão no operador.** Uma tabela impressa ao lado do monitor. Nessa configuração, a taxa de rejeição fica alta e, pior, o erro que *passa* é o perigoso: nota autorizada com tributação errada só aparece na fiscalização, com multa e juros sobre anos.

**Decisão no consultor.** A empresa terceiriza a parametrização e fica dependente de alguém externo a cada mudança de legislação — que no Brasil acontece continuamente, em três esferas ao mesmo tempo.

O sistema fiscal existe para transformar essa decisão em **matriz de regras** — uma estrutura que, dada a combinação de produto, origem, destino, operação e regime, devolve a tributação correta sem intervenção humana. E para manter essa matriz atualizada com a legislação, que é o serviço que realmente se compra.

::: nota
**O argumento comercial real da categoria.** Ninguém compra sistema fiscal por eficiência. Compra por três motivos: parar de ser rejeitado pela SEFAZ, parar de perder crédito tributário que teria direito, e transferir para um fornecedor o acompanhamento da legislação. O terceiro é o mais valioso e o menos discutido — é a diferença entre ter um time acompanhando convênio, protocolo e ajuste SINIEF, ou receber isso como atualização.
:::

## Anatomia funcional

### Motor de cálculo tributário

O núcleo. Recebe o contexto da operação e devolve a tributação: CFOP, CST ou CSOSN, base de cálculo, alíquota, valor, e as reduções e benefícios aplicáveis, por tributo. Opera sobre uma matriz de regras parametrizada por produto ou NCM, origem, destino, tipo de operação, regime do emitente e perfil do destinatário.

### Emissor de documentos eletrônicos

Monta o arquivo XML no leiaute vigente, assina com o certificado digital e o transmite. Cada documento tem seu próprio leiaute, sua própria autoridade e suas próprias regras de validação.

### Comunicação com as autoridades

SEFAZ estadual para NF-e, NFC-e, CT-e e MDF-e; prefeitura para NFS-e, cada uma com padrão próprio; Receita Federal para as obrigações acessórias. Trata protocolo, autorização, rejeição, cancelamento, inutilização e carta de correção.

### Contingência

O plano para quando a autoridade não responde. Modalidades distintas conforme o documento e o estado, com regras próprias de prazo e de regularização posterior. É o módulo que ninguém testa e do qual tudo depende no pior dia do mês.

### Recepção e manifestação de entrada

Baixa do portal as notas emitidas contra o CNPJ da empresa, valida contra o pedido de compra e o recebimento físico, e registra a manifestação do destinatário dentro do prazo legal. É também a defesa contra nota fria emitida em nome da empresa.

### Escrituração e obrigações acessórias

Monta e transmite SPED Fiscal, SPED Contribuições, ECD, ECF e EFD-Reinf, além das obrigações estaduais e municipais. Cada uma com seu calendário, seu leiaute e suas validações.

### Apuração

Consolida débitos e créditos do período por tributo e por estado, aplica compensações, e gera a guia de recolhimento e os livros fiscais.

### Guarda de documentos

Armazenamento do XML e do protocolo pelo prazo prescricional, com índice consultável e integridade verificável. Obrigação legal, não conveniência.

## Modelo de dados essencial

O que distingue um sistema fiscal de um emissor de nota é que a tributação **não é um atributo do produto nem do cliente**: é o resultado de uma função sobre o contexto completo da operação.

<figure>
<div class="figwrap">
<svg viewBox="0 0 920 460" role="img" aria-label="Modelo de dados fiscal: o contexto da operação — produto, origem, destino, natureza e regime — entra na matriz de regras, que devolve a tributação por item; o documento fiscal agrega os itens, e cada mudança de estado é um evento imutável ligado a ele.">
  <defs>
    <marker id="f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="20" y="20"  width="150" height="46" rx="2"/>
    <rect x="20" y="86"  width="150" height="46" rx="2"/>
    <rect x="20" y="152" width="150" height="46" rx="2"/>
    <rect x="20" y="218" width="150" height="46" rx="2"/>
    <rect x="20" y="284" width="150" height="46" rx="2"/>
  </g>
  <rect x="300" y="118" width="230" height="118" rx="2" fill="none" stroke="currentColor" stroke-width="2.6"/>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="640" y="40"  width="250" height="72" rx="2"/>
    <rect x="640" y="150" width="250" height="72" rx="2"/>
    <rect x="640" y="260" width="250" height="62" rx="2"/>
    <rect x="300" y="350" width="230" height="72" rx="2"/>
  </g>

  <g font-family="Archivo, sans-serif" font-size="13" font-weight="700" fill="currentColor">
    <text x="32" y="40">Produto / NCM</text>
    <text x="32" y="106">Origem</text>
    <text x="32" y="172">Destino</text>
    <text x="32" y="238">Natureza da operação</text>
    <text x="32" y="304">Regime</text>
    <text x="314" y="146">Matriz de regras</text>
    <text x="654" y="64">Item do documento</text>
    <text x="654" y="174">Documento fiscal</text>
    <text x="654" y="284">Evento</text>
    <text x="314" y="376">Apuração do período</text>
  </g>
  <g font-family="IBM Plex Mono, monospace" font-size="10" fill="currentColor" opacity=".6">
    <text x="32" y="56">o que se move</text>
    <text x="32" y="122">UF · CNPJ · estabelecimento</text>
    <text x="32" y="188">UF · contribuinte? · uso final?</text>
    <text x="32" y="254">venda · transferência · remessa</text>
    <text x="32" y="320">real · presumido · simples</text>
    <text x="314" y="166">produto × origem × destino ×</text>
    <text x="314" y="180">operação × regime → tributação</text>
    <text x="314" y="200">atualizada pelo fornecedor</text>
    <text x="314" y="220">versionada por vigência</text>
    <text x="654" y="82">CFOP · CST · base · alíquota</text>
    <text x="654" y="96">valor por tributo</text>
    <text x="654" y="192">chave · série · número · XML</text>
    <text x="654" y="206">status: autorizada | rejeitada | cancelada</text>
    <text x="654" y="302">autorização · cancelamento · CC-e · manifestação</text>
    <text x="314" y="394">débito − crédito por tributo e UF</text>
    <text x="314" y="408">→ guia e livro</text>
  </g>

  <g stroke="currentColor" stroke-width="1.3" marker-end="url(#f)">
    <line x1="172" y1="43"  x2="298" y2="150"/>
    <line x1="172" y1="109" x2="298" y2="162"/>
    <line x1="172" y1="175" x2="298" y2="175"/>
    <line x1="172" y1="241" x2="298" y2="190"/>
    <line x1="172" y1="307" x2="298" y2="204"/>
    <line x1="532" y1="150" x2="638" y2="88"/>
    <line x1="770" y1="114" x2="770" y2="148"/>
    <line x1="770" y1="224" x2="770" y2="258"/>
    <line x1="638" y1="200" x2="532" y2="368"/>
  </g>

  <g font-family="IBM Plex Mono, monospace" font-size="10" fill="currentColor" opacity=".8">
    <text x="560" y="108">calcula</text>
    <text x="782" y="136">agrega</text>
    <text x="782" y="246">registra</text>
    <text x="548" y="300">alimenta</text>
  </g>
</svg>
</div>
<figcaption>A tributação é calculada, não cadastrada. Os cinco elementos à esquerda formam o contexto; a matriz de regras é a função; o item do documento guarda o resultado. Cada mudança de estado do documento — autorização, cancelamento, carta de correção — é um evento imutável, nunca uma edição.</figcaption>
</figure>

Três decisões estruturais:

**A tributação é calculada e congelada no documento, não referenciada.** O item guarda a alíquota e a base que valiam no momento da emissão. Se a matriz mudar amanhã, a nota de ontem continua reproduzindo os valores de ontem. Referenciar a regra em vez de gravar o resultado inviabiliza qualquer reapresentação histórica — e a fiscalização é sempre sobre o passado.

**A matriz é versionada por vigência.** Regra tributária tem data de início e de fim. O sistema precisa responder "qual era a alíquota em 14 de março do ano passado", não apenas "qual é hoje". Sem vigência, retificar uma obrigação acessória de período anterior é impossível.

**O documento é uma máquina de estados dirigida por eventos.** Em digitação, assinado, transmitido, autorizado, rejeitado, cancelado, denegado, inutilizado. Cada transição é um evento com protocolo, timestamp da autoridade e XML próprio. Modelar como campo de status editável perde o protocolo — que é justamente a prova.

## Jornadas passo a passo

### A. Emissão de uma NF-e de venda

::: jornada
1. **Faturamento** conclui o pedido: itens, quantidades, preços, destinatário e condição de entrega.
2. **Sistema** monta o contexto: estabelecimento emitente, UF de origem, UF e perfil do destinatário — contribuinte ou não, uso final ou revenda —, natureza da operação e regime tributário.
3. **Sistema** consulta a matriz para cada item e devolve CFOP, CST, bases, alíquotas e valores por tributo, aplicando redução de base, benefício e substituição quando cabíveis.
4. **Sistema** monta o XML no leiaute vigente, valida contra o schema e aplica as regras de negócio da SEFAZ antes de transmitir — validar localmente evita a maior parte das rejeições.
5. **Sistema** assina com o certificado digital do emitente.
6. **Sistema** transmite à SEFAZ da UF de origem e aguarda o retorno.
7. **SEFAZ** autoriza e devolve o protocolo, que passa a integrar o documento.
8. **Sistema** gera o DANFE, libera a impressão e informa a expedição de que a carga pode sair.
9. **Sistema** grava o XML na guarda legal e envia ao financeiro o título a receber vinculado à nota.
:::

### B. Rejeição e correção

::: jornada
1. **SEFAZ** rejeita com um código e uma descrição — quase sempre por cadastro: inscrição estadual inválida, NCM inexistente, CST incompatível com o CFOP, destinatário não contribuinte com CFOP de contribuinte.
2. **Sistema** classifica a rejeição: corrigível automaticamente, corrigível por cadastro, ou exige decisão humana.
3. **Sistema** reapresenta sozinho o que for automático — número já utilizado, duplicidade, indisponibilidade momentânea.
4. **Fiscal** corrige o cadastro quando a causa é ele, e a nota é retransmitida. A nota rejeitada não consome numeração.
5. **Sistema** acumula a estatística de rejeição por causa, que é o indicador que mostra onde o cadastro está furado.
:::

### C. Contingência

::: jornada
1. **Sistema** detecta indisponibilidade da SEFAZ, por timeout ou pelo serviço de status.
2. **Sistema** entra em contingência na modalidade permitida para aquele documento e aquela UF, e a operação continua — a mercadoria sai.
3. **Sistema** monitora o retorno do serviço.
4. **Sistema** transmite o que ficou pendente assim que a autoridade volta, respeitando a ordem e os prazos de regularização.
5. **Fiscal** confere o fechamento da contingência: toda nota emitida em contingência precisa terminar autorizada ou formalmente cancelada.
:::

### D. Entrada, manifestação e crédito

::: jornada
1. **Sistema** consulta periodicamente o portal e baixa as notas emitidas contra o CNPJ da empresa.
2. **Sistema** confronta cada nota com o pedido de compra e com o recebimento físico registrado no WMS.
3. **Sistema** registra a manifestação do destinatário dentro do prazo: ciência, confirmação, desconhecimento ou operação não realizada.
4. **Fiscal** trata as divergências — preço, quantidade, tributação incorreta pelo fornecedor — antes que virem crédito indevido.
5. **Sistema** escritura a entrada e apura o crédito a que a empresa tem direito.
:::

### E. Fechamento do período

::: jornada
1. **Sistema** consolida todos os documentos de saída e entrada do período, por estabelecimento e por UF.
2. **Sistema** apura débitos e créditos por tributo, aplica saldo anterior e compensações.
3. **Sistema** gera os livros fiscais e as guias de recolhimento.
4. **Sistema** monta os arquivos das obrigações acessórias, valida com o validador oficial e transmite.
5. **Fiscal** confere as divergências entre o escriturado e o apurado antes do envio — depois de transmitido, corrigir exige retificação.
:::

## Regras de negócio e casos de borda

| Situação | Tratamento esperado |
|---|---|
| Erro percebido depois da autorização | Depende do que está errado. Valor, item ou destinatário exigem cancelamento dentro do prazo legal, ou nota de devolução se o prazo passou. Dados acessórios admitem carta de correção. Confundir os dois casos é a origem clássica de passivo. |
| Prazo de cancelamento vencido com mercadoria não entregue | Não se cancela: emite-se nota de entrada para retorno, ou o destinatário emite devolução. O sistema precisa oferecer o caminho, senão alguém inventa um. |
| Numeração pulada | Exige inutilização formal da faixa perante a SEFAZ. Deixar buraco na sequência sem inutilizar é irregularidade. |
| Denegação por irregularidade cadastral do destinatário | A numeração é consumida e a nota não pode ser reaproveitada. O bloqueio de crédito comercial deveria acontecer antes, não na SEFAZ. |
| Venda interestadual para não contribuinte | Incide DIFAL, com recolhimento e obrigação acessória própria por UF de destino. Regra que muda com frequência e por estado. |
| Produto com substituição tributária | Quem recolhe depende do estado, do protocolo entre estados e da posição na cadeia. A mesma mercadoria muda de tratamento conforme o destino. |
| Remessa para industrialização e retorno | Operação com suspensão, prazo de retorno e CFOP próprio. O sistema precisa controlar o prazo — retorno fora do prazo perde a suspensão. |
| Transferência entre estabelecimentos da mesma empresa | Tratamento próprio, e tema que passou por mudança de entendimento nos tribunais. É um caso a confirmar com a assessoria tributária antes de parametrizar. |
| Fornecedor emite nota com tributação errada | O crédito aproveitado indevidamente é da empresa que recebeu. A manifestação de desconhecimento existe para isso e tem prazo. |
| Contingência não regularizada | Cada nota emitida em contingência precisa terminar autorizada ou cancelada. Pendência aberta aparece na malha fiscal meses depois. |
| Certificado digital vencendo | Bloqueia toda a emissão da empresa quando vence. Monitoramento com antecedência é requisito operacional, não lembrete. |
| Item sem NCM válido ou com NCM extinto | A tabela de NCM muda periodicamente. Item com NCM extinto rejeita na primeira emissão depois da mudança. |
| Nota emitida antes da conferência de saída | Se a conferência acusar diferença, a nota já está autorizada. A ordem correta é conferir, emitir, carregar. |

## Arquitetura de referência

**O certificado digital define o desenho.** Um certificado A1 é arquivo e pode ser usado por serviço, permitindo emissão automatizada e alta disponibilidade. Um A3 vive em token ou cartão e exige presença física, o que inviabiliza emissão desatendida. A escolha condiciona toda a arquitetura de emissão.

**A comunicação com a autoridade é externa, lenta e instável.** Isso obriga a tratar a emissão como processo assíncrono, com fila, repetição controlada e idempotência. Reenviar sem chave de idempotência gera nota duplicada — e nota duplicada é um problema com custo.

**Contingência é caminho principal, não exceção.** Precisa ser exercitada em ambiente de homologação regularmente. A modalidade disponível varia por documento e por estado, e as regras de prazo e regularização mudam — este é um ponto para confirmar na documentação vigente antes de implementar.

**O pico é previsível e brutal.** Fim de mês, véspera de feriado, corte de transportadora. O dimensionamento se faz pelo pico de emissão simultânea, e a fila precisa degradar com elegância: atrasar é aceitável, perder documento não é.

**A guarda tem requisito legal de prazo e integridade.** XML e protocolo pelo prazo prescricional, com índice consultável e verificação de integridade. Armazenar apenas o DANFE em PDF não cumpre a obrigação — o documento é o XML.

**O ambiente de homologação é obrigatório no ciclo de desenvolvimento.** As SEFAZ oferecem ambiente de teste, e emitir contra produção para validar mudança gera documento real com efeito real.

**A atualização legislativa é o custo recorrente.** Leiaute de documento, tabela de NCM, alíquotas, regras de validação e benefícios mudam por ato normativo em três esferas. Numa construção interna, isso é um time permanente; num produto, é o que se está comprando.

::: nota
**Construir versus comprar, nesta categoria.** É a categoria em que a resposta é mais assimétrica de toda esta arquitetura. Emitir uma NF-e é tecnicamente acessível — há bibliotecas maduras e a integração é documentada. Manter o motor tributário correto ao longo do tempo é que não é: a matriz de regras precisa acompanhar convênios, protocolos, ajustes SINIEF e legislação estadual e municipal, continuamente. Construir o emissor e comprar o motor de regras é um meio-termo comum e defensável. Construir os dois exige um time fiscal dedicado que não é de software.
:::

## Especificidade brasileira

Esta categoria **é** a especificidade brasileira — não há equivalente direto na maioria dos países, onde a nota fiscal é documento privado e a apuração é declaratória e periódica. Aqui o Estado valida cada transação em tempo real, antes de a mercadoria circular.

### O mapa das obrigações

| Documento | Para quê | Autoridade |
|---|---|---|
| NF-e (modelo 55) | Circulação de mercadoria entre empresas | SEFAZ estadual |
| NFC-e (modelo 65) | Venda ao consumidor final | SEFAZ estadual |
| NFS-e | Prestação de serviço | Prefeitura — padrão por município, com esforço de padronização nacional em curso |
| CT-e | Transporte de carga | SEFAZ estadual |
| MDF-e | Manifesto que agrupa a carga do veículo | SEFAZ estadual |
| SPED Fiscal (EFD ICMS/IPI) | Escrituração de entradas, saídas, apuração e estoque | Receita Federal e SEFAZ |
| SPED Contribuições | Escrituração de PIS e COFINS | Receita Federal |
| ECD e ECF | Escrituração contábil e fiscal do lucro | Receita Federal |
| EFD-Reinf | Retenções e informações previdenciárias | Receita Federal |

**O Bloco K**, dentro do SPED Fiscal, merece destaque por conectar esta camada à fábrica: exige informar a lista de materiais praticada, o consumo real e a produção efetiva por ordem, incluindo industrialização por terceiro. É o requisito que costuma justificar o investimento em MES — sem apontamento real, o consumo declarado é estimativa.

### A reforma tributária

A Emenda Constitucional 132/2023 substitui PIS, COFINS, IPI, ICMS e ISS por CBS federal e IBS estadual e municipal, com Imposto Seletivo, e prevê transição por vários anos, com período de convivência entre os dois sistemas.

Para a arquitetura, o efeito é direto e vale registrar agora: **durante a transição, o sistema precisa apurar os dois regimes em paralelo** — os tributos atuais e os novos —, com leiautes de documento e obrigações acessórias que mudam ao longo do período. Isso significa que a matriz de regras versionada por vigência, descrita no modelo de dados, deixa de ser boa prática e vira requisito de sobrevivência.

::: nota
**Verifique o calendário e as alíquotas antes de planejar.** O cronograma de transição, as alíquotas de referência e as regras de creditamento estão sendo definidos e ajustados por legislação complementar e regulamentação. Qualquer número específico que eu apresentasse aqui envelheceria rápido e poderia estar errado. O que é estável e planejável é a consequência arquitetural: convivência de dois regimes por um período longo, com necessidade de reprocessar períodos anteriores nas regras vigentes à época.
:::

### Outras particularidades

**Regime tributário muda tudo.** Simples Nacional usa CSOSN em vez de CST e tem apuração unificada; lucro presumido e lucro real diferem em PIS e COFINS, cumulativo ou não cumulativo, com efeito direto no crédito.

**Benefício fiscal é regional e temporário.** Programas estaduais de incentivo criam tratamentos específicos com vigência determinada, o que reforça a necessidade de versionamento por data.

**Municípios não são padronizados.** Cada prefeitura definiu seu próprio padrão de NFS-e. Há esforço de unificação nacional em andamento, mas operação multimunicipal ainda exige múltiplas integrações — e é o ponto onde projetos costumam estourar prazo.

## Como avaliar ou construir

- A tributação é resultado de uma matriz sobre o contexto, ou está amarrada no cadastro do produto?
- A matriz é versionada por vigência, permitindo reproduzir a tributação de um período passado?
- O valor calculado fica congelado no item do documento?
- Cada transição de estado do documento é um evento com protocolo, ou é um campo de status?
- A validação local roda antes da transmissão, evitando rejeição por schema?
- A contingência é testada com regularidade, e existe controle de fechamento?
- A recepção de notas de entrada com manifestação está automatizada, dentro do prazo?
- A guarda armazena XML e protocolo, com integridade verificável, pelo prazo legal?
- Existe monitoramento de vencimento de certificado digital?
- Quem mantém a matriz atualizada quando a legislação muda — e como isso chega ao sistema?
- Há ambiente de homologação separado no ciclo de desenvolvimento?
- O desenho comporta apuração paralela de dois regimes durante a transição da reforma?

::: interno
## O AMR aqui

O ecossistema tem **cadastro de notas fiscais** no AMR-Fábrica — com detalhamento e mensagens fiscais por tipo de operação — e no AMR-Financeiro, além da integração "NF transmitida gera ContaReceber". O que existe é o registro do documento e o seu efeito financeiro.

Traduzindo para o modelo desta página: existe uma representação de **Documento fiscal** e de **Item**. Não existem **matriz de regras**, **motor de cálculo**, **comunicação com a SEFAZ**, **eventos com protocolo**, **contingência**, **entrada e manifestação**, **apuração** nem **guarda legal**. O termo "transmitida" no fluxo atual é um estado interno, não uma autorização da SEFAZ.

Esta é a lacuna mais crítica do ecossistema para uso real no Brasil: sem emissão autorizada, nenhuma mercadoria circula legalmente. Nenhum outro módulo tem uma dependência tão binária.

### Lacunas, em ordem de dependência

| # | Lacuna | Por que importa | Depende de |
|---|---|---|---|
| 1 | Documento fiscal como máquina de estados com eventos e protocolo | Fundação; sem isso não há como registrar autorização | — |
| 2 | Certificado digital e assinatura do XML | Pré-condição técnica de qualquer transmissão | — |
| 3 | Geração do XML no leiaute vigente, com validação local | Evita a maior parte das rejeições antes de transmitir | 1 |
| 4 | Comunicação com a SEFAZ — autorização, rejeição, protocolo | O que transforma cadastro em documento válido | 1, 2, 3 |
| 5 | Matriz de regras versionada por vigência | O coração da categoria e o maior esforço isolado | — |
| 6 | Motor de cálculo sobre a matriz | Substitui a decisão humana por regra | 5 |
| 7 | Cancelamento, inutilização e carta de correção | Sem eles, todo erro vira passivo | 4 |
| 8 | Contingência | Sem ela, indisponibilidade da SEFAZ para a operação | 4 |
| 9 | Guarda de XML e protocolo pelo prazo legal | Obrigação legal, e barata de fazer desde o início | 4 |
| 10 | Recepção e manifestação de notas de entrada | Defesa contra nota fria e condição para o crédito | 1 |
| 11 | Apuração de período e livros | Fecha o ciclo | 6, 10 |
| 12 | SPED Fiscal, incluindo Bloco K | Depende de apontamento real de produção, no MES | 11, MES |

### Recomendação de sequência

Os itens 1 a 4 formam o caminho mínimo para emitir uma nota válida, e podem ser feitos com a matriz de regras simplificada — cobrindo apenas as operações que a empresa realmente pratica hoje, com parametrização manual. Isso permite emitir de verdade sem construir o motor completo.

Os itens 5 e 6 são o esforço maior e o candidato natural a **comprar em vez de construir**. Há provedores que oferecem o motor tributário como serviço, o que resolve também a manutenção legislativa — o custo recorrente que uma equipe interna não consegue sustentar.

O item 9 custa pouco e deveria entrar junto com o 4: guardar XML desde a primeira nota é trivial; recuperar notas não guardadas depois, não.

O item 12 é o único que depende de outro módulo: o Bloco K exige consumo e produção reais, que só existem se o MES estiver apontando de verdade. Vale registrar essa dependência no planejamento — são duas iniciativas com uma amarração entre elas.

Os cards AMR-FIN-23.x cobrem NF-e, boleto, CNAB, conciliação e DRE, e estão em revisão. Pelo escopo descrito, eles endereçam os itens 1 a 4; não vi nada que cubra 5, 6, 8 ou 12.
:::
