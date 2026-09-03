---
sigla: MES / MOM · Manufacturing Execution System
titulo: Execução de manufatura
plataforma: Opcenter Execution Discrete — Siemens
dominio: Manufatura
cor: fab
resumo: O sistema que registra o que a fábrica realmente fez, evento por evento, entre a liberação da ordem e a conclusão do produto.
---

## O problema numa operação real

Uma fábrica de componentes usinados, três turnos, 180 pessoas, 42 máquinas. Cliente automotivo, o que significa IATF 16949 e rastreabilidade por número de série: dado um componente que falhou em campo dois anos depois, a fábrica precisa dizer em qual máquina ele foi usinado, com qual ferramenta, por quem, com que torque de aperto e a partir de qual lote de matéria-prima.

Sem MES, a operação funciona assim. O PCP imprime a ordem e leva ao supervisor. O operador anota quantidade e refugo numa folha. No fim do turno, alguém digita a folha no ERP. O apontamento entra no sistema entre 12 e 36 horas depois do fato, já agregado por turno, sem vínculo com máquina, sem parâmetro de processo e sem lote de origem.

O que isso custa, em ordem de gravidade:

**A rastreabilidade não existe de verdade.** Ela existe no papel, dentro de caixas no arquivo morto. Um recall que poderia atingir 400 peças atinge 40.000, porque ninguém consegue provar quais 400 vieram do lote suspeito. Já vi esse número — a diferença entre os dois cenários é o custo de dois anos de MES.

**O custo do produto é uma média.** Como o apontamento é agregado, não há como saber que a máquina 12 refuga três vezes mais que a 14 no mesmo item. A engenharia de processo trabalha com hipótese.

**O estoque em processo é ficção.** O ERP sabe o que foi baixado e o que foi entregue; o que está no meio é estimado. Em inventário, a diferença aparece como ajuste, e o ajuste vira discussão.

**A causa do refugo se perde no intervalo.** Quando o refugo é digitado 30 horas depois, ninguém consegue mais associá-lo ao lote de matéria-prima, à troca de ferramenta ou à parada de manutenção que aconteceram naquele turno.

O MES existe para eliminar esse intervalo. Ele não é um sistema de gestão que a fábrica consulta — é o sistema com o qual a fábrica trabalha, no posto, no momento em que a coisa acontece.

::: nota
**Distinção que confunde muita gente.** MES não é SCADA e não é ERP. O SCADA fala com a máquina e trata de sinal e alarme em segundos. O ERP fala com o negócio e trata de ordem e custo em dias. O MES fala com a *execução* e trata de operação, unidade e evento em minutos. Quem tenta cobrir MES com SCADA acaba com um sistema que sabe tudo da máquina e nada da ordem. Quem tenta cobrir com ERP acaba com apontamento de fim de turno — que é exatamente o problema descrito acima.
:::

## Anatomia funcional

O MES se organiza em blocos com responsabilidades distintas. Vale conhecê-los separadamente porque, numa implantação, eles entram em fases — e porque numa construção interna eles são módulos de código diferentes.

### Gestão de ordens e roteiros

Recebe do ERP a ordem de produção com item, quantidade e data, e a enriquece com o roteiro: a sequência de operações que transforma matéria-prima em produto. Cada operação tem recurso previsto, tempo padrão, parâmetros aplicáveis e materiais consumidos.

Quem usa: PCP e supervisão. O que exige de cadastro: roteiro por item, com operações e recursos habilitados. É o cadastro mais trabalhoso de toda a implantação, e o mais frequentemente subestimado.

### Terminal do operador

A tela do posto de trabalho. Mostra a fila de operações daquele recurso, recebe a identificação do operador, apresenta a instrução, coleta o apontamento e valida cada passo. É o módulo que define se o MES é adotado ou sabotado — se o operador leva mais de 20 segundos para apontar, ele vai apontar em lote no fim do turno e o sistema volta a ser uma folha de papel eletrônica.

Quem usa: operador, com as mãos ocupadas e às vezes com luva. Restrição de projeto: poucos toques, alvos grandes, funciona com leitor de código de barras como entrada principal.

### Rastreamento de unidades e genealogia

Mantém a identidade de cada unidade em processo — lote, número de série ou container — e registra o vínculo entre unidade filha e unidades pai. É o coração da rastreabilidade e a parte mais difícil de acertar depois, porque exige decidir cedo qual é a granularidade rastreável.

### Coleta de dados de processo

Recebe parâmetros do equipamento: torque, pressão, temperatura, tempo de ciclo, medida dimensional, resultado de sistema de visão. Cada valor é gravado vinculado à operação, ao recurso e à unidade em execução — o que transforma um número solto em evidência.

### Qualidade em processo

Planos de inspeção amarrados a pontos do roteiro, com frequência, característica medida e limite. Registra resultado, aprova ou reprova, e abre não conformidade quando reprova. Inclui inspeção de primeira peça, controle estatístico e verificação de setup.

### Não conformidade, contenção e retrabalho

Trata o que deu errado: registra o defeito, bloqueia a unidade, encaminha para decisão de disposição — usar como está, retrabalhar, refugar, devolver ao fornecedor — e conduz o roteiro de retrabalho quando houver.

### Gestão de recursos

Máquinas, ferramentas, dispositivos e moldes, com seus limites: número de ciclos até afiação, validade de calibração, capacidade. Bloqueia o uso de ferramenta vencida.

### Mão de obra e competências

Quem é o operador, para qual operação ele é habilitado, com qual certificação e até quando. É o cadastro que sustenta a validação mais importante do sistema em operação regulada.

### Paradas e desempenho

Registra parada com motivo, calcula disponibilidade, performance e qualidade — os três fatores do OEE — e apresenta o indicador por recurso, turno e período.

## Modelo de dados essencial

Esta é a seção que quase nenhuma documentação de fornecedor traz, e é a que mais explica o sistema. Um MES não é um CRUD de estado: é um **registro de eventos append-only** com um modelo de identidade em cima.

<figure>
<div class="figwrap">
<svg viewBox="0 0 920 480" role="img" aria-label="Modelo de dados do MES: a ordem se decompõe em operações; a unidade de rastreamento carrega a identidade do produto e se liga a unidades pai por genealogia; o apontamento é o evento central que amarra unidade, operação, recurso e pessoa num instante, e dele derivam parâmetros, inspeções e não conformidades.">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="20"  y="24"  width="180" height="62" rx="2"/>
    <rect x="20"  y="130" width="180" height="62" rx="2"/>
    <rect x="370" y="24"  width="180" height="62" rx="2"/>
    <rect x="720" y="24"  width="180" height="62" rx="2"/>
    <rect x="720" y="130" width="180" height="62" rx="2"/>
    <rect x="720" y="236" width="180" height="62" rx="2"/>
  </g>
  <rect x="330" y="196" width="260" height="86" rx="2" fill="none" stroke="currentColor" stroke-width="2.4"/>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="150" y="336" width="180" height="62" rx="2"/>
    <rect x="370" y="336" width="180" height="62" rx="2"/>
    <rect x="590" y="336" width="180" height="62" rx="2"/>
  </g>

  <g font-family="Archivo, sans-serif" font-size="13" font-weight="700" fill="currentColor">
    <text x="34" y="48">Ordem de produção</text>
    <text x="34" y="154">Operação</text>
    <text x="384" y="48">Unidade rastreável</text>
    <text x="734" y="48">Recurso</text>
    <text x="734" y="154">Pessoa</text>
    <text x="734" y="260">Ferramenta</text>
    <text x="344" y="222">Apontamento</text>
    <text x="164" y="360">Parâmetro</text>
    <text x="384" y="360">Inspeção</text>
    <text x="604" y="360">Não conformidade</text>
  </g>
  <g font-family="IBM Plex Mono, monospace" font-size="10" fill="currentColor" opacity=".6">
    <text x="34" y="66">nº · item · qtd · datas</text>
    <text x="34" y="76">origem: ERP</text>
    <text x="34" y="172">sequência · tempo padrão</text>
    <text x="34" y="182">recurso previsto</text>
    <text x="384" y="66">lote | série | container</text>
    <text x="384" y="76">estado · localização</text>
    <text x="734" y="66">máquina · posto</text>
    <text x="734" y="172">habilitação · validade</text>
    <text x="734" y="278">vida útil · calibração</text>
    <text x="344" y="240">quando · o quê · quanto</text>
    <text x="344" y="254">aprovado | refugo | retrabalho</text>
    <text x="344" y="268">imutável — corrige-se por estorno</text>
    <text x="164" y="378">valor · limite · fonte</text>
    <text x="384" y="378">característica · resultado</text>
    <text x="604" y="378">defeito · disposição</text>
  </g>

  <g stroke="currentColor" stroke-width="1.3" marker-end="url(#a)">
    <line x1="110" y1="86"  x2="110" y2="128"/>
    <line x1="200" y1="161" x2="328" y2="215"/>
    <line x1="460" y1="86"  x2="460" y2="194"/>
    <line x1="718" y1="55"  x2="592" y2="205"/>
    <line x1="718" y1="161" x2="592" y2="225"/>
    <line x1="718" y1="267" x2="592" y2="245"/>
    <line x1="420" y1="282" x2="300" y2="334"/>
    <line x1="460" y1="282" x2="460" y2="334"/>
    <line x1="500" y1="282" x2="620" y2="334"/>
  </g>
  <path d="M 550 40 C 620 6 660 6 636 34" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#a)"/>

  <g font-family="IBM Plex Mono, monospace" font-size="10" fill="currentColor" opacity=".8">
    <text x="118" y="112">1 : N</text>
    <text x="232" y="182">executa</text>
    <text x="468" y="150">sofre</text>
    <text x="648" y="120">em</text>
    <text x="648" y="196">por</text>
    <text x="648" y="262">com</text>
    <text x="596" y="22">genealogia (N : N)</text>
    <text x="288" y="316">gera</text>
    <text x="468" y="316">gera</text>
    <text x="628" y="316">gera</text>
  </g>
</svg>
</div>
<figcaption>O apontamento é a entidade central: ele amarra <em>o quê</em> (unidade), <em>em qual passo</em> (operação), <em>onde</em> (recurso), <em>por quem</em> (pessoa) e <em>quando</em>. Tudo o mais — parâmetro, inspeção, não conformidade — pendura nele. A seta que volta sobre a unidade rastreável é a genealogia: a relação entre uma unidade e as unidades que a compõem.</figcaption>
</figure>

Três decisões de modelagem definem o destino do projeto:

**A granularidade da unidade rastreável.** Lote, série ou container? Série dá rastreabilidade perfeita e multiplica o volume de dados por mil. Lote é barato e responde à maior parte das perguntas regulatórias. A escolha certa depende do que o cliente exige e do que a operação consegue identificar fisicamente — não adianta escolher série se a peça não tem onde gravar a marcação.

**Apontamento imutável.** O evento nunca é editado. Erro se corrige por evento de estorno, que também fica registrado. Isso parece burocrático e é o que torna o sistema auditável — um MES com `UPDATE` no apontamento não serve como evidência, porque não há como provar que o número de hoje é o número de ontem.

**Estado é derivado, não armazenado.** A quantidade produzida de uma ordem é a soma dos apontamentos, não um campo que alguém incrementa. Guardar o estado como campo cria a divergência clássica entre o total e a soma dos lançamentos, que ninguém consegue explicar seis meses depois. Onde a performance exigir, guarda-se um agregado — mas como cache reconstruível, nunca como verdade.

## Jornadas passo a passo

### A. Início de turno e liberação de operação

::: jornada
1. **Operador** aproxima o crachá ou bipa seu código no terminal do posto.
2. **Sistema** identifica a pessoa, verifica se ela está habilitada para aquele recurso e se as certificações estão válidas. Se alguma venceu, bloqueia e notifica o líder do turno.
3. **Sistema** apresenta a fila de operações daquele recurso, na sequência definida pelo planejamento, com a próxima destacada.
4. **Operador** seleciona a operação e bipa a etiqueta da ordem.
5. **Sistema** verifica pré-condições: a operação anterior do roteiro está concluída? A ferramenta montada é a prevista e está dentro da vida útil? O material apresentado corresponde ao componente da lista? Se qualquer uma falha, bloqueia com a mensagem específica — nunca com "erro".
6. **Sistema** apresenta a instrução eletrônica de trabalho na versão vigente para aquele item, incluindo desenho e parâmetros.
7. **Operador** confirma o setup. Em item crítico, o sistema exige inspeção de primeira peça antes de liberar a produção seriada.
8. **Sistema** registra o evento de início e passa a operação para o estado em execução.
:::

### B. Execução e apontamento

::: jornada
1. **Operador** produz a peça.
2. **Máquina** envia o contador de ciclo e os parâmetros do processo pela camada de automação, ou o operador informa a quantidade no terminal quando não há coleta automática.
3. **Sistema** vincula cada parâmetro à operação, ao recurso e à unidade corrente, e compara com a faixa especificada.
4. **Sistema** bloqueia e alerta se o valor sai da faixa: a peça não avança e o supervisor é notificado. Este é o mecanismo que impede o lote inteiro fora de especificação.
5. **Operador** informa a quantidade aprovada e, separadamente, a refugada, escolhendo o motivo numa lista curta e específica — motivo genérico destrói o valor do dado.
6. **Sistema** grava o apontamento como evento imutável, atualiza o WIP, consome os componentes da lista de materiais na proporção produzida e registra a genealogia entre a unidade produzida e os lotes consumidos.
7. **Sistema** imprime a etiqueta de identificação com o código da unidade, se o processo exigir.
8. **Operador** encerra a operação; a unidade fica disponível para a operação seguinte do roteiro.
:::

### C. Não conformidade e disposição

::: jornada
1. **Operador** ou **inspetor** registra o defeito, com foto e medida quando aplicável.
2. **Sistema** coloca a unidade em contenção: ela não avança no roteiro e não pode ser consumida por nenhuma outra ordem.
3. **Sistema** identifica automaticamente, pela genealogia, quais outras unidades compartilham o lote de origem, o mesmo recurso ou a mesma janela de tempo — a base para decidir a abrangência da contenção.
4. **Qualidade** analisa e decide a disposição: usar como está, retrabalhar, refugar ou devolver ao fornecedor.
5. **Sistema** encaminha conforme a decisão. Em retrabalho, abre o roteiro de retrabalho e mantém o vínculo com a ordem original — a peça retrabalhada continua sendo a mesma peça, com histórico acrescido.
6. **Sistema** mantém o registro completo: quem identificou, quem decidiu, com que fundamento e quando.
:::

### D. Encerramento e devolução ao ERP

::: jornada
1. **Sistema** detecta que a quantidade da última operação atingiu a quantidade da ordem, ou o supervisor encerra manualmente com quantidade menor.
2. **Sistema** consolida os apontamentos e envia ao ERP a confirmação de produção, o consumo real de componentes e o refugo por motivo.
3. **ERP** baixa o estoque de componentes, entra com o produto acabado e apura o custo real da ordem.
4. **Sistema** fecha a ordem e mantém a genealogia disponível para consulta pelo prazo definido — que em automotivo costuma ser quinze anos.
:::

## Regras de negócio e casos de borda

O que separa um MES que funciona de uma prova de conceito é o tratamento destas situações. Todas acontecem toda semana.

| Situação | Tratamento esperado |
|---|---|
| Falta componente no meio da ordem | A operação é suspensa com motivo específico, o WIP permanece onde está e o tempo de espera é contabilizado como parada por falta de material — não como produção lenta. Requisição ao WMS é disparada. |
| Operador sem certificação válida | Bloqueio na identificação, antes de qualquer produção. Permitir e avisar depois anula o propósito do controle. |
| Parâmetro fora da faixa | Peça bloqueada, alerta ao supervisor, e a decisão de continuar exige aprovação de alçada superior — registrada. |
| Máquina para no meio da operação | A operação fica em execução com parada aberta. O tempo de parada é atribuído ao motivo, não ao tempo de ciclo, senão o OEE mente. |
| Refugo descoberto depois do apontamento | Evento de estorno, não edição. O apontamento original permanece, e a diferença fica visível. |
| Ordem cancelada com WIP no meio | O material em processo precisa de destino explícito: retorna ao estoque, transfere para outra ordem ou vira refugo. Cancelar sem tratar o WIP é a origem clássica de divergência de inventário. |
| Troca de turno com operação aberta | A operação transita de operador sem fechar. Os dois turnos aparecem no histórico, com produção atribuída a cada um. |
| Ordem dividida em dois recursos | O roteiro precisa suportar divisão e reunião de quantidade, mantendo a genealogia de cada fração. |
| Retrabalho | Decisão de modelagem: mesma ordem com operações adicionais, ou ordem de retrabalho vinculada. A primeira preserva o custo no produto; a segunda dá visibilidade do custo do retrabalho. A maioria das operações quer a segunda. |
| Rede cai no chão de fábrica | O terminal continua operando e sincroniza depois. Um MES que para quando a rede oscila é abandonado em duas semanas. |
| Relógio divergente entre terminais | Fonte única de tempo no servidor. Timestamp de terminal desincronizado inviabiliza a reconstrução da sequência de eventos. |
| Estorno de ordem já confirmada no ERP | Requer transação compensatória nos dois sistemas, nunca correção manual em um só. |

## Arquitetura de referência

Como esse tipo de sistema é construído, independentemente de fornecedor.

**Disponibilidade é requisito de produção, não de TI.** MES parado é fábrica parada — ou, pior, fábrica produzindo sem registro, o que depois exige reconstrução manual. Isso empurra o desenho para redundância no servidor e autonomia no terminal.

**O terminal precisa tolerar desconexão.** Armazenamento local com fila de eventos e sincronização assíncrona. O evento é gerado com identificador único na origem, para que o reenvio não duplique o apontamento — idempotência é requisito, não refinamento.

**Comunicação com máquina é uma camada à parte.** OPC UA é o padrão predominante em equipamento industrial moderno; MQTT aparece em cenários de IIoT e em retrofit; equipamento antigo entra por driver proprietário ou por leitura de sinal digital. Essa camada traduz o dado bruto do CLP para o evento de negócio, e é onde mora a maior parte do esforço de integração de qualquer projeto de MES.

**Volume é maior do que a intuição sugere.** Quarenta e duas máquinas, ciclo médio de 30 segundos, três turnos: são da ordem de 100 mil eventos por dia só de contagem, sem contar parâmetros de processo, que podem multiplicar isso por dez. O modelo append-only ajuda na escrita, mas exige estratégia de particionamento e de arquivamento desde o início.

**Latência percebida no terminal precisa ficar abaixo de um segundo.** Acima disso o operador contorna o sistema — aponta depois, aponta em lote, deixa a tela aberta. A validação síncrona deve consultar apenas o que é local ou cacheado; o que depende do ERP resolve-se de forma assíncrona.

**Integração com ERP é assíncrona e reconciliável.** Fila com garantia de entrega, e um processo periódico de reconciliação que compara o que o MES enviou com o que o ERP registrou. Sem reconciliação, a divergência acumula silenciosamente e aparece no inventário.

**Versionamento de roteiro e de instrução é obrigatório.** A ordem executada há seis meses precisa ser reconstituível com o roteiro e a instrução vigentes naquela data, não com os atuais. Isso é requisito de auditoria e implica guardar versão, não apenas o registro corrente.

::: nota
**A decisão comprar versus construir.** MES é a categoria em que construir internamente é mais tentador — o processo é específico da fábrica, e um pacote genérico sempre parece grande demais. O que costuma ser subestimado: a camada de integração com equipamento, o versionamento de roteiro e instrução, o comportamento offline do terminal e a reconstrução histórica. Nenhum dos quatro aparece na primeira versão, e os quatro são caros de acrescentar depois. Construir faz sentido quando o processo é realmente atípico e a fábrica tem time de software permanente; caso contrário, a conta vira manutenção eterna.
:::

## Especificidade brasileira

Há um requisito brasileiro que muda a conta de retorno do MES e que raramente aparece nas apresentações comerciais: o **Bloco K do SPED Fiscal**.

O Bloco K exige que a empresa informe ao fisco, mensalmente, a produção e o consumo de materiais por ordem — a lista de materiais praticada, o consumo real e a produção efetiva, incluindo a industrialização feita por terceiros. Sem MES, essa informação é montada por estimativa a partir do padrão de engenharia, o que gera duas exposições: a divergência entre o consumo declarado e a movimentação de estoque, e a ausência de lastro para o crédito de ICMS sobre o insumo.

Isso significa que, no Brasil, o MES tem um argumento de conformidade fiscal além do argumento de eficiência — e é frequentemente o que aprova o investimento.

Outros pontos com particularidade local:

**Industrialização por encomenda.** Material que sai para beneficiamento em terceiro e volta precisa manter identidade e rastreabilidade fora da fábrica, com vínculo à nota de remessa e ao retorno. O MES precisa reconhecer a operação externa como parte do roteiro.

**NR-12.** A norma de segurança em máquinas exige registro de quem operou cada equipamento e evidência de capacitação. O controle de habilitação do MES vira registro de conformidade, não apenas controle de processo.

**Rastreabilidade em setores regulados.** Alimentos e bebidas (RDC da Anvisa e instruções normativas do Mapa), farmacêutico e dispositivos médicos têm exigências próprias de lote e de recall que o MES sustenta diretamente.

## Como avaliar ou construir

Perguntas que separam um MES real de um sistema de apontamento com nome bonito:

- O apontamento é imutável, com correção por estorno? Se o registro é editável, o sistema não serve como evidência.
- A genealogia é consultável nos dois sentidos — de um lote de matéria-prima para os produtos afetados, e de um produto de volta aos seus insumos?
- O terminal opera com a rede caída e sincroniza depois sem duplicar evento?
- Roteiro e instrução de trabalho são versionados, com reconstituição histórica?
- A validação de habilitação e de ferramenta bloqueia, ou apenas registra?
- O tempo de parada é separado do tempo de ciclo no cálculo de desempenho?
- A integração com o ERP tem reconciliação periódica, ou confia no envio?
- Quantos toques o operador dá para apontar uma peça? Acima de cinco, a adoção corre risco.
- O sistema atende ao Bloco K com dado real, ou só exporta o padrão de engenharia?

::: interno
## O AMR aqui

O **AMR-Fábrica** ocupa hoje a camada de registro: fichas de produção, ordens por equipamento, estações de trabalho, tipos de operação com passos e parâmetros configuráveis, e a estrutura organizacional de filiais, departamentos e business units. Há integração com o Financeiro — saída de ficha gera ContaPagar, NF transmitida gera ContaReceber — e sincronização de pedidos com o Core por polling.

Traduzindo para o modelo desta página: existem **Ordem** e **Operação**, existe **Recurso** de forma simplificada, e existe um apontamento. Não existem **Unidade rastreável**, **genealogia**, **Parâmetro** vinculado ao evento, **Inspeção** nem **Não conformidade**.

### Lacunas, em ordem de dependência

| # | Lacuna | Por que importa | Depende de |
|---|---|---|---|
| 1 | Unidade rastreável (lote/série) como entidade | Sem ela não há genealogia, e sem genealogia não há rastreabilidade nem Bloco K com dado real | — |
| 2 | Apontamento imutável com estorno | Requisito para o registro valer como evidência; mexe no modelo atual | — |
| 3 | Genealogia — consumo vinculado à unidade produzida | O entregável de maior valor comercial do módulo | 1, 2 |
| 4 | Terminal do operador | Define adoção; hoje a interface é de cadastro, não de posto de trabalho | 1 |
| 5 | Validação bloqueante de material, ferramenta e habilitação | Transforma registro em controle | 1, 4 |
| 6 | Cadastro de competências e certificações com validade | Sustenta 5 e atende NR-12 | — |
| 7 | Inspeção em processo e não conformidade com disposição | Fecha o ciclo de qualidade | 1, 3 |
| 8 | Retrabalho estruturado | Hoje não há caminho para a peça que não passou | 7 |
| 9 | Parada com motivo e cálculo de OEE | O indicador que a diretoria pede | — |
| 10 | Coleta direta de máquina | Maior esforço, maior dependência de infraestrutura; faz sentido depois de 1 a 5 | 1, 4 |
| 11 | Instruções eletrônicas de trabalho versionadas | Requisito de auditoria em cliente automotivo | 4 |

### Recomendação de sequência

Os itens 1, 2 e 3 formam um bloco indivisível e deveriam ser tratados como uma única iniciativa — são mudança de modelo de dados, não funcionalidade nova, e ficam progressivamente mais caros conforme a base de dados cresce. O item 9 é o de melhor relação entre esforço e percepção de valor, e pode andar em paralelo por não depender dos demais. O item 10 é o mais visível em demonstração e o mais arriscado de puxar cedo: depende de infraestrutura de chão de fábrica que ainda não existe.

Os cards de BOM/OP v2 e Manutenção v2 no backlog tocam parte disso, mas nenhum endereça a unidade rastreável — que é a fundação de tudo o mais nesta lista.
:::
