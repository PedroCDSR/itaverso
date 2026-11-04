# ITAMANIA: documento de design

(Texto enviado pelo Pedro em 04/11/2026. Fonte de verdade da história. Decisões tomadas durante a construção ficam
no `STATUS.md`.)

Jogo de plataforma 2D para celular sobre Itajubá/MG, com a jogabilidade e a linguagem visual de um jogo de plataforma
de 16 bits.

Responda sempre em português do Brasil, simples e direto. Não use travessões nos textos (nem no jogo, nem nas
respostas).

## Direção atual aprovada pelo Pedro (04/11/2026)

A protagonista passa a ser uma **capivara exploradora**, quadrúpede, caramelo, com mochila verde e lenço amarelo
(proposta visual 1). Esta entrega de desenvolvimento permite explorar a praça com ela. A adaptação das fases de
plataforma e da progressão antiga de Geraldo/Helena será feita nas próximas entregas; o roteiro abaixo permanece
como referência dessas fases, sem apresentá-las como já convertidas.

## Visão geral

- Roda no navegador do celular, é curto e **não tem game over**: cada fase tem ponto de retorno.
- 14 fases e 1 fase secreta, num mapa-múndi em pé (pixel art, já pronto), de baixo para cima.
- Público inclui crianças. Tom leve, sem nada assustador de verdade.
- Lado educativo: cada fase termina com um cartão de curiosidade real sobre a cidade.

## Regras fixas

1. **Estilo do gênero pode, elementos da Nintendo não.** Nada de Mario, Goomba, Koopa, planta carnívora, cogumelo,
   canos verdes, blocos "?", morros ou nuvens com olhos. Mecânicas do gênero (crescer com item, arremessar) podem,
   com visual e sons próprios.
2. **Sem violência.** Inimigo atingido não morre: pega o item, come e vai embora feliz.
3. **Sem piada com droga.**
4. **Pessoas reais só com OK delas**, sempre em versão carinhosa. Tudo que é real entra como "vaga" (ver abaixo): o
   jogo sempre funciona com a versão genérica.
5. **Marcas não aparecem escritas** (fábrica, lojas, planos de saúde, postos etc.). *(Exceção autorizada pelo Pedro
   em 04/11/2026 para os comércios de Itajubá: ver STATUS.md.)*
6. **Política:** nada de partido, campanha, urna ou propaganda. O prefeito do jogo não pode lembrar políticos reais.
   Se a Prefeitura for dona do jogo, isso é obrigatório: a Constituição (art. 37, §1º) proíbe publicidade oficial que
   promova autoridades.
7. **Sem coleta de dados.** Nada de servidor, cadastro ou LGPD dentro do jogo.
8. **Fatos só com fonte.** O que não foi confirmado fica marcado "(confirmar)" e não vai para o jogo assim.

## Personagens

- **Geraldo ou Helena** (homenagem aos avós do autor), escolhidos na tela inicial. Cada partida é só a história de
  quem foi escolhido; o outro não aparece.
- Uma criança que acabou de chegar a Itajubá, animada e feliz com a vida nova, que não conhece a cidade e quer
  conhecer.
- Visual: mochila e tênis. O **boné amarelo** só aparece a partir da fase 3.
- **Arte:** mesmo corpo e mesmas animações para os dois, mudando cabelo e cores das roupas. São quatro conjuntos:
  Geraldo e Helena criança, Geraldo e Helena adultos. Para economizar, o adulto pode ter uma forma só, e o café com
  leite vira um escudo.
- **Falas com marcação de gênero**, trocadas pelo jogo conforme a escolha: `Estou {animado|animada}!`,
  `{engenheiro|engenheira}`, `{prefeito|prefeita}`.
- **Créditos:** dedicatória a Geraldo e Helena.

## Itens, moeda e poderes

| Item | Onde aparece | O que faz |
|---|---|---|
| Itacoins | Desde a fase 2 | Moeda (pedrinhas amarelas, a "pedra amarela" do nome da cidade) |
| Boné amarelo | Fase 3, comprado na loja | Identidade visual do herói |
| Café com leite | Fase 4 em diante (vem do café da praça) | Cresce e aguenta um toque a mais |
| Pão de queijo | Fase 4 em diante (vem da lanchonete da praça) | Arremesso: o inimigo pega, come e vai embora |
| Peças do quebra-cabeça | Fases 5, 6 e 7 | Pistas do mistério da Mulher de Bronze |
| Mochila-hélice | Fase 9 (invenção do TCC) | Planar e subir |
| Helicóptero | Fase 13 | Voo: segurar sobe, soltar desce |

**Evolução do herói:** sem boné → boné (3) → café com leite e pão de queijo (4) → mochila-hélice (9) → helicóptero
(13) → prefeito ou prefeita (14).

**Inimigos (todos leves):** capivaras, pombos da praça, morcegos fofos no cemitério, provas voadoras na UNIFEI. Os de
cada fase serão definidos na construção.

## Estrutura de cada fase

Chegada → missão curta do lugar → plataforma até o fim → cartão de curiosidade (uma frase, uns cinco segundos de
leitura).

## A história

**Ato 1, o sonho (fases 1 a 4).** A criança chega de ônibus, vê um helicóptero no céu e quer ser piloto. Descobre que
o helicóptero é feito ali mesmo, na fábrica da cidade, e que quem estuda na UNIFEI trabalha lá. Ganha o boné e os
poderes e aprende como nasceu a escola de engenharia.

**Ato 2, o encanto (fases 5 a 8).** Vê a cidade do alto e acha tudo lindo. Ouve falar de uma mulher de bronze que
ninguém sabe quem é e junta as pistas. No Coroados, decide: estudar na UNIFEI vira o sonho. No cemitério, descobre a
história da estátua.

**Ato 3, a UNIFEI (fase 9).** Escolhe o curso, atravessa os anos de faculdade numa fase só, apresenta o TCC e se forma.
Salto no tempo: "anos depois...".

**Ato 4, do engenheiro ao prefeito (fases 10 a 14).** Mora no Pinheirinho e vira um engenheiro ou engenheira de
sucesso. Decide cuidar da cidade, voa no helicóptero que ajudou a construir e, anos depois, a cidade o escolhe para
prefeito ou prefeita. Quem chegou sem conhecer a cidade termina cuidando dela.

## As fases

| # | Lugar | O que acontece | Novidade de jogo | Curiosidade |
|---|---|---|---|---|
| 1 | Rodoviária e trem-museu | Desce do ônibus. O trem parado em frente (peça de museu, não funciona) é o tutorial: subir na locomotiva e pular entre os vagões. Lá de cima, vê o helicóptero cruzando o céu | Correr e pular | Em 1932 foi aprovada a construção de uma nova estação em Itajubá, na Linha Sapucaí da Rede Mineira de Viação. História da locomotiva: a pesquisar |
| 2 | Praça do Soldado | Vê o helicóptero da praça e decide ser piloto | Itacoins | Itajubá tem a primeira e única fábrica de helicópteros da América Latina. Origem do helicóptero da praça: (confirmar) |
| 3 | Rua Nova | Compra o boné com itacoins na loja. Descobre que o helicóptero é feito na cidade | Loja | Uma das explicações para o nome Itajubá é "pedra amarela", ou seja, ouro. Há outras versões, como "braço de pedra" |
| 4 | Praça central (Theodomiro Santiago) | Conhece a lanchonete e o café. Descobre que quem estuda na UNIFEI trabalha na fábrica e aprende a história de Theodomiro Santiago | Café com leite (cresce) e pão de queijo (arremesso) | Theodomiro fundou em 1913 o Instituto Eletrotécnico e Mecânico de Itajubá (IEMI), a 10ª escola de engenharia do Brasil, com recursos da própria família ("vendeu tudo": confirmar). Nomes: IEMI (1913) → IEI (1936) → EFEI (1968) → UNIFEI (2002) |
| 5 | Alameda até o Morro Chic | Sobe ao Morro Chic e acha a cidade linda. Moradores falam da mulher de bronze. Peça 1: "dizem que ela veio da França" | Subida | Itajubá fica nas encostas da Serra da Mantiqueira |
| 6 | Coroados (hotel que cobre a rua no alto do morro) | Encantado, decide estudar na UNIFEI. Peça 2: "dizem que foi presente de um filho" | Fase vertical no prédio | A pesquisar |
| 7 | Praçonha (beira da Av. BPS) | Rio Sapucaí e pontes. Peça 3: "dizem que tudo começou com uma foto" | Pontes, rio e capivaras | A pesquisar (as 7 pontes da Av. BPS) |
| 8 | Cemitério (alto do Cruzeiro, à noite) | Encontra a estátua e monta o quebra-cabeça: a imagem é a mesma mulher. O cartão conta a história verdadeira. A lua ilumina a estátua e revela a saída secreta | Fase noturna, morcegos fofos, saída secreta | A Mulher de Bronze foi encomendada por Eucides de Moura Fonseca ao artista francês Antoine Sartori, inspirada numa foto que ele tirou de surpresa da mãe, Gabriela, em 1918 (ela não gostava de ser fotografada). Chegou ao Brasil em 1925, é patrimônio tombado desde 2012 e foi restaurada em 2023 |
| Secreta | Céu estrelado | Fase bônus para quem acha a saída do cemitério | A definir | Itajubá é sede do Laboratório Nacional de Astrofísica |
| 9 | UNIFEI | Escolhe o curso. Fase longa em cinco trechos, um por ano. Chefe leve: a apresentação do TCC. Formatura e salto no tempo | Ganha a mochila-hélice | UNIFEI e a fábrica assinaram acordo de cooperação em 2013 |
| 10 | Pinheirinho | Casa nova. Primeiro dia como {engenheiro\|engenheira} na fábrica | Planar com a mochila-hélice | A pesquisar |
| 11 | Agonia (santuário de vidro azul no morro) | Do ponto mais alto, vê a cidade inteira e decide cuidar dela. Ilumina o morro para a festa da cidade | Subida com a hélice | A pesquisar |
| 12 | Kart | Corrida da festa da cidade | Fase de velocidade | A pesquisar |
| 13 | Lago (Parque da Cidade) | Primeiro voo do helicóptero que ajudou a construir. Resgata uma capivara ilhada | Pilotar | Oito em cada dez helicópteros de serviço público no Brasil saem da fábrica de Itajubá |
| 14 | Prefeitura | "Anos depois", a cidade escolhe Geraldo ou Helena (cena curta, sem campanha). Fase curta até a posse e tela final | Final | Itajubá foi fundada em 19 de março de 1819 |

### Detalhes

- **Escolha do curso (fase 9):** não muda o caminho, só o diploma e uma fala do final. A mensagem é que a fábrica
  precisa de vários tipos de engenheiro (vagas de lá pedem engenharia mecânica, aeronáutica ou civil). A UNIFEI tem o
  curso de Engenharia Mecânica Aeronáutica, aprovado em 2010.
- **Mulher de Bronze (fase 8):** a estátua não fala nem se mexe, porque é o memorial de uma família real. Quem conta a
  história são os moradores e o cartão. O momento mágico fica com a lua e a luz. Mostrar a fase ao conselho de
  patrimônio da cidade (CODPHAI) ou à família antes de publicar.

### Curiosidades de reserva

- A fábrica de helicópteros nasceu em 1978, em São José dos Campos, e veio para Itajubá em 1980.
- Há um projeto de lei de 2022 para dar a Itajubá o título de Capital Nacional da Produção de Helicópteros (confirmar
  se virou lei).

## Vagas (pessoas e lugares reais)

O jogo funciona sempre com a versão genérica. A real só entra com autorização.

| Onde | Versão genérica | Versão real (só com OK) |
|---|---|---|
| Fase 3 | A loja de bonés | Casa Joka |
| Fase 4 | A lanchonete da praça | Cesar Burg |
| Fase 4 | O café da praça | Café do Vadinho |
| Fases 2 a 4 e 9 a 13 | A fábrica de helicópteros | Helibras (possível parceira ou patrocinadora) |
| Fase 8 | Uma estátua antiga | Mulher de Bronze (CODPHAI ou família) |
| Fase 4 | Narração e cartão | Theodomiro Santiago (personagem histórico, em versão respeitosa) |

Outros "figurões da cidade" entram do mesmo jeito: personagem genérico que funciona sozinho e ganha nome e rosto reais
só com o OK da pessoa.

## Mapa-múndi

- Imagem pronta, em pé, em pixel art. O marcador 1 pode continuar "TREM", já que o trem segue na frente da rodoviária.
- Outros marcos: Av. BPS com o Rio Sapucaí no meio e 7 pontes, Santa Casa, Câmara, pracinha (sem marca escrita),
  rotatória e o Rio Sapucaí no sul. Bairros: Centro, BPS, Cruzeiro e Varginha.

## Pendências (não travam o começo)

- **Dono do jogo** (Prefeitura, projeto próprio, escolas): define só a tela final.
- **Orientação das fases:** em pé como o mapa ou deitado.
- **Curiosidades a pesquisar:** fases 6, 7, 10, 11 e 12; história da locomotiva da rodoviária; origem do helicóptero
  da Praça do Soldado; se Theodomiro "vendeu tudo"; se o projeto da Capital Nacional dos Helicópteros virou lei.
- **Autorizações:** donos das lojas, a fábrica, CODPHAI ou família da Mulher de Bronze.
- **Inimigos de cada fase** e o que acontece ao levar um toque na forma pequena.
- **Epílogo opcional:** uma nova criança desce do ônibus na rodoviária e olha para o céu.

## Ordem de construção

1. Esqueleto: personagem correndo e pulando no celular, controles de toque, fase 1 com retângulos no lugar da arte.
2. Sistema de fase: missão, itacoins, ponto de retorno e cartão de curiosidade.
3. Escolha entre Geraldo e Helena e falas com marcação de gênero.
4. Poderes na ordem da história: boné, café com leite, pão de queijo.
5. Fase de voo (13) cedo, porque é a mecânica mais diferente.
6. Demais fases, uma a uma, e o mapa-múndi navegável.
7. Arte, sons e textos por último.

## Fontes

- UNIFEI, história: https://international.unifei.edu.br/about-unifei/history/
- IEMI, IEI e EFEI (BOCEHM): https://revistas.uece.br/index.php/BOCEHM/article/download/987/848/3672
- Fundação da cidade, LNA e UNIFEI em 2002 (Estado de Minas): https://www.em.com.br/emfoco/?p=268307
- Histórico de Itajubá e o nome "pedra amarela" (IBGE): https://biblioteca.ibge.gov.br/visualizacao/dtb/minasgerais/itajuba.pdf
- Federalização da UNIFEI, recursos da família de Theodomiro (Fundação FHC): https://fundacaofhc.org.br/files/artigo/1424.pdf
- Única fábrica de helicópteros da América Latina (Rádio Senado): https://www12.senado.leg.br/noticias/audios/2022/10/itajuba-pode-ser-a-capital-nacional-da-producao-de-helicopteros
- PL 2.653/2022 (Senado): https://www25.senado.leg.br/en/web/atividade/materias/-/materia/154929
- Fábrica: 1978, Itajubá em 1980 (Defesa Aérea & Naval): https://defesaaereanaval.com.br/aviacao/ministro-da-defesa-visita-fabrica-da-helibras-em-itajuba
- Acordo UNIFEI e fábrica em 2013 (HeliHub): https://www.helihub.com/?p=86373
- Engenharia Mecânica Aeronáutica da UNIFEI (Abenge): https://abenge.org.br/cobenge/legado/arquivos/5/Artigos/129027.pdf
- Vaga da fábrica (Jobijoba): https://www.jobijoba.com.br/detail/97/1f7f7541ed108bf1d90bf13acb63eb83
- Mulher de Bronze (Conexão Itajubá): https://conexaoitajuba.com.br/noticia/cultura-prefeitura-realiza-restauracao-da-mulher-de-bronze-82531
- Decreto de 1932, nova estação de Itajubá (Senado): https://legis.senado.leg.br/norma/440683
- Itajubá e a Serra da Mantiqueira (Wikipedia): https://kiwix.lema.org/wikipedia_en_all_mini_2024-02/A/Itajub%C3%A1
