import * as Phaser from 'phaser';
import { JOGADOR as J } from '../config.js';

// Aladdin do jogo (design original e provisório: ver src/art/jogador.js).
//
// Física (CLAUDE.md, seção 9):
// - aceleração e freio, em vez de velocidade instantânea, para não ficar "duro";
// - pulo variável: soltar o botão durante a subida corta o pulo;
// - coyote time: dá para pular até 100 ms depois de sair da beirada;
// - buffer de pulo: apertar pular até 100 ms antes de pousar também vale;
// - cai mais rápido do que sobe.
export class Jogador extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y) {
    super(scene, x, y, 'jogador', 0);
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.setOrigin(0.5, 1); // x,y = pé do personagem
    this.body.setSize(J.corpo.largura, J.corpo.altura).setOffset(J.corpo.x, J.corpo.y);
    this.body.setMaxVelocity(1000, J.quedaMaxima);
    this.body.setCollideWorldBounds(true);

    this.olhandoDireita = true;
    this.ultimoNoChao = -Infinity; // momento (ms) em que esteve no chão pela última vez
    this.ultimoPedidoPulo = -Infinity; // momento em que apertou pular pela última vez
    this.subindoComBotao = false; // está no meio de um pulo com o botão apertado
    this.arremessandoAte = 0;
    this.vida = J.coracoes;
    this.invencivelAte = 0; // até quando (ms) está piscando e não leva dano
    this.atordoadoAte = 0; // até quando (ms) está sem controle, logo depois do dano
    this.play('parado');
  }

  estaInvencivel(agora) {
    return agora < this.invencivelAte;
  }

  // Leva 1 de dano vindo de "deOndeX" (empurra para o lado oposto). Devolve a vida que sobrou.
  levarDano(deOndeX, agora) {
    if (this.estaInvencivel(agora)) return this.vida;
    this.vida = Math.max(0, this.vida - 1);
    this.invencivelAte = agora + J.invencivelMs;
    this.atordoadoAte = agora + J.atordoadoMs;
    const dir = this.x < deOndeX ? -1 : 1;
    this.body.setVelocity(J.recuoDano.x * dir, -J.recuoDano.y);
    this.subindoComBotao = false;
    this.play('dano', true);
    return this.vida;
  }

  // Quique ao pisar num inimigo (segurando PULAR vai um pouco mais alto).
  quicar(forca) {
    this.body.setVelocityY(-forca);
    this.subindoComBotao = false;
    this.ultimoNoChao = -Infinity;
  }

  // Chamar todo quadro. entrada = ui/Entrada.js; temMaca = ainda há maçãs para arremessar.
  // Devolve true no quadro em que soltou uma maçã.
  atualizar(entrada, agora, delta, temMaca = true) {
    const corpo = this.body;
    const dt = delta / 1000;
    const noChao = corpo.blocked.down || corpo.touching.down;
    if (noChao) this.ultimoNoChao = agora;

    // pisca enquanto está invencível
    this.setAlpha(this.estaInvencivel(agora) && Math.floor(agora / 70) % 2 === 0 ? 0.35 : 1);

    // logo depois do dano: sem controle, só o recuo e a gravidade
    if (agora < this.atordoadoAte) {
      corpo.setGravityY(corpo.velocity.y > 0 ? J.gravidadeQuedaExtra : 0);
      this.setFlipX(!this.olhandoDireita);
      return false;
    }

    // --- andar ---
    const alvo = entrada.esquerda ? -J.velocidade : entrada.direita ? J.velocidade : 0;
    if (alvo !== 0) this.olhandoDireita = alvo > 0;
    const acel = alvo === 0 ? J.freio : noChao ? J.aceleracaoChao : J.aceleracaoAr;
    corpo.setVelocityX(aproximar(corpo.velocity.x, alvo, acel * dt));

    // --- pular (com buffer e coyote time) ---
    if (entrada.pularApertou) this.ultimoPedidoPulo = agora;
    const pediuHaPouco = agora - this.ultimoPedidoPulo <= J.bufferPuloMs;
    const podePular = agora - this.ultimoNoChao <= J.coyoteMs;
    if (pediuHaPouco && podePular) {
      corpo.setVelocityY(-J.forcaPulo);
      this.ultimoPedidoPulo = -Infinity;
      this.ultimoNoChao = -Infinity; // não deixa pular duas vezes no mesmo coyote
      this.subindoComBotao = true;
    }
    // pulo variável: soltou o botão ainda subindo => corta a subida (uma vez só)
    if (this.subindoComBotao && (!entrada.pular || corpo.velocity.y >= 0)) {
      if (corpo.velocity.y < 0) corpo.setVelocityY(corpo.velocity.y * J.cortePulo);
      this.subindoComBotao = false;
    }
    // queda mais pesada que a subida
    corpo.setGravityY(corpo.velocity.y > 0 ? J.gravidadeQuedaExtra : 0);

    // --- maçã ---
    let soltouMaca = false;
    if (entrada.macaApertou && temMaca && agora >= this.arremessandoAte) {
      this.arremessandoAte = agora + 160;
      this.play('arremessando', true);
      soltouMaca = true;
    }

    this.escolherAnimacao(noChao, agora);
    return soltouMaca;
  }

  escolherAnimacao(noChao, agora) {
    this.setFlipX(!this.olhandoDireita);
    if (agora < this.arremessandoAte) return; // deixa a animação de arremesso terminar
    const v = this.body.velocity;
    let anim;
    if (!noChao) anim = v.y < 0 ? 'pulando' : 'caindo';
    else anim = Math.abs(v.x) > 12 ? 'correndo' : 'parado';
    this.play(anim, true);
  }

  // Volta a um ponto (checkpoint), parado e com vida cheia.
  reposicionar(x, y, agora = 0) {
    this.body.reset(x, y);
    this.subindoComBotao = false;
    this.ultimoPedidoPulo = -Infinity;
    this.atordoadoAte = 0;
    this.vida = J.coracoes;
    this.invencivelAte = agora + J.invencivelMs; // um respiro ao voltar
  }
}

// Move "atual" em direção a "alvo" no máximo "passo".
function aproximar(atual, alvo, passo) {
  if (atual < alvo) return Math.min(atual + passo, alvo);
  if (atual > alvo) return Math.max(atual - passo, alvo);
  return atual;
}
