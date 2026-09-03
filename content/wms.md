---
sigla: WMS · Warehouse Management System
titulo: Gestão de armazém
plataforma: Manhattan Active WM
dominio: Cadeia de suprimentos
cor: sup
resumo: O sistema que sabe onde cada item está fisicamente, quem o moveu e em que ordem separá-lo — e não apenas quanto existe no total.
---

## O problema numa operação real

Um centro de distribuição de 9.000 m², 8.000 SKUs ativos, 1.200 pedidos por dia, 40 separadores em dois turnos. Metade dos itens tem controle de lote e validade. O cliente maior exige entrega em 48 horas e aplica multa por divergência de nota.

Sem WMS, a operação funciona por conhecimento tácito. O separador experiente sabe que o item 4471 fica "lá no fundo, no corredor da esquerda, prateleira de cima". O ERP informa que existem 340 unidades no depósito 01 — número que está certo no total e é inútil na prática, porque não diz em quais três endereços elas estão nem qual lote vence primeiro.

O que isso produz:

**Tempo de deslocamento domina o custo.** Numa separação sem roteiro, o operador percorre o corredor na ordem em que os itens aparecem no pedido, não na ordem em que estão no armazém. Em operação de médio porte, deslocamento costuma responder por mais da metade do tempo de separação — e é a parcela que o WMS ataca diretamente.

**O inventário exige parar.** Sem endereçamento, contar significa contar tudo. A operação para um ou dois dias por ano, e o ajuste resultante entra na contabilidade como perda sem causa identificada.

**FEFO é uma intenção.** Com controle de validade só no papel, o separador pega o que está na frente. O lote que vence primeiro fica no fundo até vencer, e a perda aparece no inventário seguinte.

**O erro de separação só aparece no cliente.** Sem conferência sistêmica na saída, o item trocado viaja. Volta o frete de ida, o frete de volta, o retrabalho fiscal da devolução e uma ocorrência no indicador do cliente.

**A produtividade não é comparável.** Não há como saber se o separador A é melhor que o B, ou se a diferença é o mix que cada um pegou. Dimensionamento de equipe vira negociação em vez de cálculo.

O WMS existe para transformar o armazém de um espaço que as pessoas conhecem num espaço que o sistema conhece — e, com isso, tornar a operação independente de quem está no turno.

::: nota
**A confusão mais comum: "o ERP já controla o estoque".** Controla o saldo, que é uma pergunta contábil. O WMS responde perguntas físicas: em qual endereço, em qual unidade de manuseio, com qual lote, em qual status, e qual tarefa está pendente sobre ele. São modelos de dados diferentes, não profundidades diferentes do mesmo modelo. Tentar cobrir WMS com o módulo de estoque do ERP costuma terminar em planilha paralela de endereçamento — que é o sintoma clássico.
:::

## Anatomia funcional

### Estrutura física e endereçamento

O cadastro do armazém: prédios, áreas, corredores, ruas, módulos, níveis e posições, cada endereço com capacidade, restrição e perfil de uso. Define também as zonas — recebimento, reserva, separação, expedição, quarentena, avaria.

É o cadastro que sustenta tudo o mais. Quem usa: engenharia logística, na implantação e em cada mudança de layout.

### Recebimento e conferência

Recebe o aviso de embarque ou o pedido de compra, agenda a doca, confere a chegada contra o documento e gera as unidades de manuseio. A conferência cega — em que o conferente informa o que contou sem ver o esperado — é o que diferencia conferência de confirmação.

### Armazenagem

Decide o endereço de guarda por regra e dirige o operador até ele. Considera curva de giro, peso, volume, temperatura, incompatibilidade química e proximidade da área de separação.

### Separação

O núcleo operacional. Converte pedidos em tarefas, agrupa em ondas, define a estratégia — por pedido, por lote de pedidos, por zona com consolidação — e sequencia o percurso. Suporta separação por RF, por voz, por luz e por estação de consolidação.

### Reposição

Move material do estoque de reserva para a área de separação antes que ela zere. Roda por nível mínimo, por demanda da onda ou por previsão. É invisível quando funciona e paralisa a separação quando falta.

### Conferência de saída e expedição

Confere o separado antes de embarcar, por leitura, peso ou volume; consolida por carga; gera o romaneio; controla o carregamento e libera a saída vinculada ao documento fiscal.

### Inventário

Contagem rotativa por endereço, por curva ou por evento — sem parar a operação. Trata divergência com recontagem e ajuste com trilha.

### Gestão de mão de obra

Padrão de tempo por tipo de tarefa, medição do realizado, e comparação por operador, turno e atividade. Base para dimensionamento e para programa de produtividade.

### Doca, pátio e agendamento

Janela de chegada por fornecedor e transportadora, fila de veículos, ocupação de doca. Onde há volume, é o que impede o pátio de virar estacionamento.

### Logística reversa

Recebimento de devolução, triagem, decisão de destino — reintegrar, reparar, descartar — e retorno ao estoque com o status correto.

## Modelo de dados essencial

A diferença entre um WMS e um controle de estoque endereçado está em duas entidades que raramente aparecem quando alguém desenha o sistema pela primeira vez: a **unidade de manuseio** e a **tarefa**.

<figure>
<div class="figwrap">
<svg viewBox="0 0 920 470" role="img" aria-label="Modelo de dados do WMS: o saldo não é por item, e sim pela combinação de item, endereço, lote e status dentro de uma unidade de manuseio; a tarefa é a intenção de mover, e o movimento é o evento que a conclui.">
  <defs>
    <marker id="w" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="20"  y="24"  width="170" height="58" rx="2"/>
    <rect x="20"  y="130" width="170" height="58" rx="2"/>
    <rect x="20"  y="236" width="170" height="58" rx="2"/>
    <rect x="730" y="24"  width="170" height="58" rx="2"/>
    <rect x="730" y="150" width="170" height="58" rx="2"/>
    <rect x="380" y="366" width="170" height="58" rx="2"/>
    <rect x="600" y="366" width="170" height="58" rx="2"/>
  </g>
  <rect x="330" y="120" width="270" height="86" rx="2" fill="none" stroke="currentColor" stroke-width="2.4"/>
  <rect x="330" y="248" width="270" height="72" rx="2" fill="none" stroke="currentColor" stroke-width="2.4"/>

  <g font-family="Archivo, sans-serif" font-size="13" font-weight="700" fill="currentColor">
    <text x="34" y="46">Item</text>
    <text x="34" y="152">Endereço</text>
    <text x="34" y="258">Lote / validade</text>
    <text x="744" y="46">Unidade de manuseio</text>
    <text x="744" y="172">Documento</text>
    <text x="344" y="146">Saldo posicionado</text>
    <text x="344" y="274">Tarefa</text>
    <text x="394" y="388">Movimento</text>
    <text x="614" y="388">Ajuste</text>
  </g>
  <g font-family="IBM Plex Mono, monospace" font-size="10" fill="currentColor" opacity=".6">
    <text x="34" y="64">sku · unidade · giro</text>
    <text x="34" y="170">rua · nível · capacidade</text>
    <text x="34" y="276">fabricação · vencimento</text>
    <text x="744" y="64">palete · caixa · contêiner</text>
    <text x="744" y="76">a entidade esquecida</text>
    <text x="744" y="190">recebimento · pedido</text>
    <text x="344" y="164">item + endereço + lote +</text>
    <text x="344" y="178">status + unidade = quantidade</text>
    <text x="344" y="192">disponível | reservado | bloqueado</text>
    <text x="344" y="292">a intenção de mover</text>
    <text x="344" y="306">origem · destino · prioridade · quem</text>
    <text x="394" y="406">o evento que executa</text>
    <text x="614" y="406">divergência tratada</text>
  </g>

  <g stroke="currentColor" stroke-width="1.3" marker-end="url(#w)">
    <line x1="192" y1="53"  x2="328" y2="140"/>
    <line x1="192" y1="159" x2="328" y2="159"/>
    <line x1="192" y1="265" x2="328" y2="178"/>
    <line x1="728" y1="53"  x2="602" y2="150"/>
    <line x1="465" y1="208" x2="465" y2="246"/>
    <line x1="728" y1="179" x2="602" y2="272"/>
    <line x1="440" y1="322" x2="440" y2="364"/>
    <line x1="520" y1="322" x2="640" y2="364"/>
  </g>

  <g font-family="IBM Plex Mono, monospace" font-size="10" fill="currentColor" opacity=".8">
    <text x="240" y="88">o quê</text>
    <text x="240" y="150">onde</text>
    <text x="240" y="230">qual lote</text>
    <text x="640" y="92">dentro de</text>
    <text x="474" y="232">reserva</text>
    <text x="640" y="238">origina</text>
    <text x="448" y="348">conclui</text>
    <text x="576" y="348">corrige</text>
  </g>
</svg>
</div>
<figcaption>O saldo não pertence ao item: pertence à combinação de item, endereço, lote, status e unidade de manuseio. A tarefa é a intenção de mover — criada pela reserva, executada pelo movimento. Separar as duas é o que permite planejar trabalho sem ter executado nada ainda.</figcaption>
</figure>

Três decisões definem a qualidade do sistema:

**A unidade de manuseio é uma entidade, não um atributo.** Um palete identificado por etiqueta própria pode conter vários itens e vários lotes, mover-se inteiro numa tarefa e ser conferido por um único código. Sem essa entidade, cada movimentação de palete vira N movimentações de item, o volume de transações explode e a conferência deixa de ser possível numa leitura só. É a decisão que mais separa WMS de controle endereçado.

**Status faz parte da chave do saldo.** Disponível, reservado, em quarentena, bloqueado por qualidade, em avaria. Guardar status como campo booleano de bloqueio força consultas erradas: a pergunta "quanto tenho disponível para vender" tem resposta diferente de "quanto tenho fisicamente", e as duas precisam sair do mesmo modelo.

**Tarefa separada de movimento.** A tarefa é o trabalho planejado — origem, destino, prioridade, responsável, prazo. O movimento é o fato consumado. Modelar as duas como uma coisa só impede fila de trabalho, redistribuição de tarefa entre operadores e medição de produtividade, que são metade do valor do sistema.

## Jornadas passo a passo

### A. Recebimento e armazenagem

::: jornada
1. **Transportadora** chega; **portaria** registra a entrada e o veículo entra na fila do agendamento.
2. **Sistema** aloca a doca conforme a janela agendada e o tipo de carga.
3. **Conferente** abre o recebimento pelo coletor, informando o documento de entrada.
4. **Sistema** apresenta o esperado — ou não apresenta nada, se a política for conferência cega.
5. **Conferente** conta e informa item, quantidade, lote e validade. Em item com controle, o lote é obrigatório e a validade é validada contra o prazo mínimo aceito.
6. **Sistema** compara com o esperado e trata a divergência: aceita dentro da tolerância, ou abre ocorrência e segura o recebimento.
7. **Conferente** monta o palete e o sistema gera a **unidade de manuseio**, com etiqueta impressa e colada ali mesmo.
8. **Sistema** decide o endereço de guarda pela regra do item — giro, peso, temperatura, incompatibilidade — e cria a tarefa de armazenagem.
9. **Operador de empilhadeira** recebe a tarefa no coletor, leva o palete, bipa o endereço de destino e confirma.
10. **Sistema** valida se o endereço bipado é o dirigido; se não for, exige justificativa e registra o desvio.
:::

### B. Separação por onda

::: jornada
1. **Supervisor** ou o próprio sistema fecha uma onda: um conjunto de pedidos que serão separados juntos, agrupados por rota, transportadora ou horário de corte.
2. **Sistema** verifica disponibilidade, reserva o saldo por lote segundo a política — FEFO na maioria dos casos — e gera as tarefas de separação.
3. **Sistema** dispara as tarefas de reposição necessárias para que a área de separação suporte a onda, e as executa antes.
4. **Sistema** sequencia as tarefas por percurso, minimizando deslocamento, e as distribui por zona ou por operador.
5. **Separador** recebe a primeira tarefa no coletor: endereço, item, quantidade.
6. **Separador** vai ao endereço, bipa o endereço, bipa o item e informa a quantidade. As três leituras são o que garante que ele pegou o item certo no lugar certo.
7. **Sistema** valida e apresenta a próxima tarefa, já na sequência do percurso.
8. **Separador** conclui a rota e leva o volume à área de consolidação.
9. **Conferente** confere a saída — por leitura item a item, por peso do volume ou por amostragem, conforme a criticidade.
10. **Sistema** libera a expedição e vincula a carga ao documento fiscal.
:::

### C. Inventário rotativo

::: jornada
1. **Sistema** seleciona endereços para contagem por critério: curva A semanalmente, endereço zerado após a última retirada, endereço com divergência recente, ou amostragem aleatória.
2. **Sistema** bloqueia o endereço para movimentação e gera a tarefa de contagem.
3. **Contador** vai ao endereço, bipa e informa o que encontrou, sem ver o saldo esperado.
4. **Sistema** compara. Se bate, libera o endereço e encerra.
5. **Sistema** dispara recontagem quando diverge, preferencialmente com outro operador.
6. **Supervisor** analisa a divergência confirmada e aprova o ajuste, que registra responsável, motivo e valor.
7. **Sistema** envia o ajuste ao ERP para o efeito contábil e libera o endereço.
:::

### D. Devolução

::: jornada
1. **Sistema** recebe a autorização de devolução, vinda do OMS ou do atendimento.
2. **Conferente** recebe o volume, bipa a identificação e o sistema recupera o pedido de origem.
3. **Conferente** tria o material: íntegro, avariado, faltando peça, produto errado.
4. **Sistema** direciona por status — íntegro volta ao estoque disponível; avariado vai para a área de avaria; item com lote vencido é bloqueado para descarte.
5. **Sistema** informa ao ERP e ao fiscal o retorno, para o crédito e para a nota de entrada.
:::

## Regras de negócio e casos de borda

| Situação | Tratamento esperado |
|---|---|
| Endereço bipado diferente do dirigido | Permite com justificativa registrada, ou bloqueia — conforme a política. Bloquear sempre trava a operação em exceções legítimas; permitir sem registro destrói a acuracidade. |
| Saldo insuficiente no endereço durante a separação | Tarefa é replanejada para outro endereço com o mesmo lote, sem devolver o pedido para a fila. Se não houver, gera falta com registro, não silêncio. |
| Lote mais novo na frente do mais velho | O FEFO é aplicado na reserva, não na escolha do separador. Se o sistema dirigir para o endereço do lote correto, a política se cumpre sozinha. |
| Item sem endereço definido chega no recebimento | Vai para área de espera com tarefa de cadastro, nunca para um endereço genérico — o "endereço geral" é onde a acuracidade morre. |
| Unidade de manuseio parcialmente consumida | O palete permanece como unidade, com saldo reduzido. Fracionar não pode significar perder a identidade da unidade. |
| Pedido cancelado depois de separado | A reserva é liberada e é criada tarefa de retorno ao endereço. Sem essa tarefa, o material fica na consolidação e some do saldo disponível. |
| Divergência de inventário recorrente no mesmo endereço | Sinaliza causa sistêmica — endereço mal cadastrado, item parecido ao lado, leitura duplicada. Ajustar sem investigar reincidência é maquiagem. |
| Coletor sem rede no meio da rota | Continua operando com as tarefas já baixadas e sincroniza ao reconectar. A tarefa concluída offline não pode ser reatribuída a outro operador enquanto não sincroniza. |
| Dois operadores na mesma tarefa | Atribuição exclusiva com bloqueio. Sem isso, o mesmo endereço é separado duas vezes e a divergência aparece no fim do dia. |
| Nota fiscal emitida antes da conferência de saída | Inverte o risco: se a conferência acusar diferença, a nota já está autorizada e exige cancelamento ou nota complementar. A emissão deve seguir a conferência, não precedê-la. |
| Produto com validade curta na entrada | Regra de prazo mínimo de aceite no recebimento, recusando o que não sobrevive ao ciclo de venda. |
| Avaria identificada na separação | Bloqueia a unidade, gera tarefa de reposição do item para completar o pedido e abre ocorrência — três ações, não uma. |

## Arquitetura de referência

**O coletor é o cliente principal, e ele opera mal conectado.** A rede sem fio de um armazém tem sombras — estruturas metálicas, câmaras frias, corredores altos. O desenho precisa assumir desconexão momentânea: tarefas baixadas em bloco, confirmação em fila local, sincronização idempotente. Um WMS que exige conexão contínua é abandonado nas primeiras semanas.

**A tela do coletor tem restrições próprias.** Poucos campos, alvo grande, fluxo dirigido por leitura, nenhuma navegação livre. O operador está de luva, às vezes no frio, e a métrica que importa é leituras por tarefa — não cliques por página.

**Concorrência é o problema técnico central.** Quarenta operadores disputando o mesmo saldo exigem reserva atômica no momento de gerar a tarefa. Reservar por consulta e depois gravar produz separação dupla. Este é o ponto em que implementações internas costumam falhar sob carga real.

**Volume transacional é alto e desigual.** Mil e duzentos pedidos com média de seis linhas dão 7.200 tarefas de separação por dia, mais reposição, mais armazenagem, mais contagem — e tudo se concentra nas horas anteriores ao corte de transportadora. Dimensionar pela média subdimensiona o pico.

**Integração com o ERP é assíncrona, com reconciliação.** O WMS é a autoridade sobre a posição física; o ERP, sobre o saldo contábil. Divergem por alguns minutos por natureza. O que não pode é divergir por dias sem que ninguém perceba — daí a reconciliação periódica.

**Automação física entra por uma camada isolada.** Esteiras, separadores automáticos, AGVs e coletores de voz têm protocolos próprios e ciclos de vida diferentes do software. Acoplar direto significa reescrever o WMS quando o equipamento muda.

**A impressão é infraestrutura crítica.** Etiqueta de unidade de manuseio, etiqueta de volume, romaneio. Fila de impressão local, com reimpressão controlada — reimprimir etiqueta de unidade sem invalidar a anterior cria duas unidades com o mesmo código, que é um erro difícil de rastrear depois.

::: nota
**Onde o projeto costuma descarrilar.** Não é no software: é no cadastro do armazém e na disciplina de endereçamento. Um WMS implantado sobre um layout mal mapeado, com endereços que não correspondem à realidade física, produz dirigimento errado — e o operador aprende em uma semana a ignorar o sistema. A implantação é, na maior parte, um projeto de engenharia logística com um software no fim.
:::

## Especificidade brasileira

**A expedição é amarrada ao documento fiscal.** No Brasil a mercadoria não sai sem NF-e autorizada, e em transporte de carga sem CT-e e MDF-e. Isso torna a integração fiscal parte do fluxo de expedição, e não um passo administrativo posterior. O sequenciamento correto é conferência, depois emissão, depois carregamento — inverter cria o risco de nota autorizada para carga que não confere.

**Armazém geral e operador logístico têm regime próprio.** Mercadoria de terceiro guardada em nome do depositante exige controle de propriedade separado do controle físico, com CFOP e notas específicas de remessa e retorno. Um WMS usado por operador logístico precisa segregar estoque por cliente e emitir a documentação correspondente.

**Rastreabilidade sanitária.** Alimentos, bebidas, medicamentos e cosméticos têm exigência de lote e prazo de validade sob normas da Anvisa e do Mapa, com obrigação de recall rastreável. O controle de lote deixa de ser boa prática e vira requisito legal.

**Substituição tributária afeta o que se pode movimentar.** Mercadoria com ICMS-ST recolhido antecipadamente tem restrição de destino e de operação. O WMS não calcula tributo, mas precisa carregar o atributo que impede a expedição indevida.

**Bloco K, quando o armazém alimenta produção.** Se o mesmo armazém abastece uma fábrica, o consumo movimentado pelo WMS entra na declaração de consumo do Bloco K. O vínculo entre movimentação física e declaração fiscal precisa existir desde o começo.

## Como avaliar ou construir

- A unidade de manuseio existe como entidade própria, com identificação física e movimentação em bloco?
- O saldo é chaveado por item, endereço, lote e status — ou só por item e depósito?
- A reserva é atômica sob concorrência? Teste com quarenta separadores simultâneos, não com dois.
- O coletor opera desconectado e sincroniza sem duplicar movimento?
- Tarefa e movimento são entidades separadas?
- O roteiro de separação é otimizado por percurso, ou apenas ordenado por código de endereço?
- O inventário rotativo roda sem bloquear o armazém inteiro?
- A conferência de saída precede a emissão da nota?
- Há padrão de tempo por tipo de tarefa, permitindo medir produtividade de forma comparável?
- O sistema segrega estoque por proprietário, se houver operação para terceiros?

::: interno
## O AMR aqui

O **AMR-WMS** cobre localizações, recebimento, separação e movimentação de estoque, sobre .NET 10, EF Core e SQLite, com frontend React 19 e Bootstrap. A estrutura de Clean Architecture com CQRS está montada, e o domínio de armazém existe como módulo independente — o que é a parte difícil de começar.

Traduzindo para o modelo desta página: existem **Item**, **Endereço** e um saldo com movimentação. Não existem **Unidade de manuseio**, **Tarefa** como entidade separada do movimento, **Lote com validade** como parte da chave do saldo, nem **status** de estoque.

### Lacunas, em ordem de dependência

| # | Lacuna | Por que importa | Depende de |
|---|---|---|---|
| 1 | Status no saldo (disponível, reservado, bloqueado) | Sem isso não há reserva, e sem reserva não há separação confiável | — |
| 2 | Lote e validade como parte da chave do saldo | Requisito legal em setor sanitário e pré-condição do FEFO | — |
| 3 | Tarefa como entidade, separada do movimento | Habilita fila de trabalho, atribuição e medição — metade do valor do WMS | 1 |
| 4 | Unidade de manuseio | Reduz o volume de transações e viabiliza conferência por leitura única | 1 |
| 5 | Reserva atômica sob concorrência | O ponto onde implementação interna costuma quebrar em carga real | 1, 3 |
| 6 | Interface de coletor, com fluxo dirigido por leitura | A tela atual é de cadastro, não de operação | 3 |
| 7 | Onda de separação e sequenciamento por percurso | O ganho de produtividade mais direto da categoria | 3, 5 |
| 8 | FEFO na reserva | Consequência natural de 2 e 5, mas precisa ser explicitado como política | 2, 5 |
| 9 | Reposição automática de picking | Sem ela, a onda para por falta de material na área errada | 3, 7 |
| 10 | Inventário rotativo com recontagem e ajuste | Elimina a parada anual e dá acuracidade medida | 1, 3 |
| 11 | Conferência de saída antes da emissão fiscal | Ordem correta do fluxo; hoje não há conferência sistêmica | 3 |
| 12 | Operação offline no coletor | Requisito de campo, não refinamento | 6 |

### Recomendação de sequência

Os itens 1 e 2 são mudança de modelo de dados e deveriam vir juntos, antes de qualquer volume de dados relevante — o mesmo raciocínio da unidade rastreável no MES. O item 3 é o divisor: com tarefa modelada, 5, 6, 7 e 10 se tornam incrementos; sem ela, cada um vira uma gambiarra própria.

O item 4 pode esperar: unidade de manuseio compensa quando há paletização real e volume, e antes disso adiciona complexidade sem retorno. O item 12 é o mais fácil de subestimar e o que mais determina adoção em campo.

Vale notar a assimetria com o MES: o AMR-WMS é o módulo mais recente e o mais bem estruturado tecnicamente, mas o mais distante da operação real — ele modela um estoque endereçado, não um armazém. A distância entre as duas coisas é exatamente esta lista.
:::
