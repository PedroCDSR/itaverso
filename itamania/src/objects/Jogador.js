import * as Phaser from 'phaser';
import { JOGADOR as J } from '../config.js';
import { heroi } from '../genero.js';

// Herói (Geraldo ou Helena). Física herdada do motor do Aladdin:
// aceleração e freio, pulo variável, coyote time e buffer de pulo de 100 ms, queda mais pesada que a subida.
//
// Duas formas (DESIGN.md): 'normal' e 'turbinado' (café com leite: fica maior e aguenta um toque a mais).
// O boné amarelo (fase 3 em diante) usa os mesmos quadros com o boné desenhado (segunda metade da folha).
export class Jogador extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, { bone = false, turbinado = false } = {}) {
    super(scene, x, y, `heroi-${heroi()}-normal`, 0);
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.setOrigin(0.5, 1);
    this.body.setMaxVelocity(1000, J.quedaMaxima);
    this.body.setCollideWorldBounds(true);
    this.bone = bone;
    this.forma = turbinado ? 'turbinado' : 'normal';
    this.olhandoDireita = true;
    this.ultimoNoChao = -Infinity;
    this.ultimoPedidoPulo = -Infinity;
    this.subindoComBotao = false;
    this.arremessandoAte = 0;
    this.saiEm = 0;
    this.vida = J.coracoes;
    this.invencivelAte = 0;
    this.atordoadoAte = 0;
    this.animAtual = '';
    this.aplicarForma();
    this.tocar('parado');
  }

  get turbinado() {
    return this.forma === 'turbinado';
  }

  // Troca textura e corpo de colisão mantendo o pé no mesmo lugar.
  aplicarForma() {
    // as duas caixas terminam na última linha do quadro (o pé), e a origem do sprite é o pé: nada se mexe
    const c = J.corpo[this.forma];
    this.setTexture(`heroi-${heroi()}-${this.forma}`);
    this.body.setSize(c.largura, c.altura).setOffset(c.x, c.y);
    const atual = this.animAtual;
    this.animAtual = '';
    if (atual) this.tocar(atual);
  }

  setForma(forma) {
    if (forma === this.forma) return;
    this.forma = forma;
    this.aplicarForma();
  }

  setBone(sim) {
    this.bone = sim;
    const atual = this.animAtual;
    this.animAtual = '';
    this.tocar(atual || 'parado');
  }

  // Anima pelo nome curto ('correndo'); a chave real depende do herói, da forma e do boné (Preload).
  tocar(nome, forcar = false) {
    if (nome === this.animAtual && !forcar) return;
    this.animAtual = nome;
    this.play(`${heroi()}-${this.forma}-${this.bone ? 'b' : 's'}-${nome}`, true);
  }

  estaInvencivel(agora) {
    return agora < this.invencivelAte;
  }

  // Leva um toque vindo de "deOndeX". Turbinado: volta ao normal e não perde coração.
  // Devolve a vida que sobrou.
  levarDano(deOndeX, agora) {
    if (this.estaInvencivel(agora)) return this.vida;
    if (this.turbinado) this.setForma('normal');
    else this.vida = Math.max(0, this.vida - 1);
    this.invencivelAte = agora + J.invencivelMs;
    this.atordoadoAte = agora + J.atordoadoMs;
    const dir = this.x < deOndeX ? -1 : 1;
    this.body.setVelocity(J.recuoDano.x * dir, -J.recuoDano.y);
    this.subindoComBotao = false;
    this.saiEm = 0;
    this.arremessandoAte = 0;
    this.tocar('dano', true);
    return this.vida;
  }

  quicar(forca) {
    this.body.setVelocityY(-forca);
    this.subindoComBotao = false;
    this.ultimoNoChao = -Infinity;
  }

  // Chamar todo quadro. Devolve true no quadro em que o pão de queijo sai da mão.
  atualizar(entrada, agora, delta, podeArremessar = false) {
    const corpo = this.body;
    const dt = delta / 1000;
    const noChao = corpo.blocked.down || corpo.touching.down;
    if (noChao) this.ultimoNoChao = agora;
    this.setAlpha(this.estaInvencivel(agora) && Math.floor(agora / 70) % 2 === 0 ? 0.35 : 1);

    if (agora < this.atordoadoAte) {
      corpo.setGravityY(corpo.velocity.y > 0 ? J.gravidadeQuedaExtra : 0);
      this.setFlipX(!this.olhandoDireita);
      return false;
    }

    const alvo = entrada.esquerda ? -J.velocidade : entrada.direita ? J.velocidade : 0;
    if (alvo !== 0) this.olhandoDireita = alvo > 0;
    const acel = alvo === 0 ? J.freio : noChao ? J.aceleracaoChao : J.aceleracaoAr;
    corpo.setVelocityX(aproximar(corpo.velocity.x, alvo, acel * dt));

    if (entrada.pularApertou) this.ultimoPedidoPulo = agora;
    const pediuHaPouco = agora - this.ultimoPedidoPulo <= J.bufferPuloMs;
    const podePular = agora - this.ultimoNoChao <= J.coyoteMs;
    if (pediuHaPouco && podePular) {
      corpo.setVelocityY(-J.forcaPulo);
      this.ultimoPedidoPulo = -Infinity;
      this.ultimoNoChao = -Infinity;
      this.subindoComBotao = true;
      this.pulouAgora = true;
    }
    if (this.subindoComBotao && (!entrada.pular || corpo.velocity.y >= 0)) {
      if (corpo.velocity.y < 0) corpo.setVelocityY(corpo.velocity.y * J.cortePulo);
      this.subindoComBotao = false;
    }
    corpo.setGravityY(corpo.velocity.y > 0 ? J.gravidadeQuedaExtra : 0);

    let soltou = false;
    if (entrada.macaApertou && podeArremessar && agora >= this.arremessandoAte) {
      this.arremessandoAte = agora + J.arremessoMs;
      this.saiEm = agora + J.antecipacaoArremessoMs;
      this.tocar('arremessando', true);
    }
    if (this.saiEm && agora >= this.saiEm) {
      this.saiEm = 0;
      soltou = true;
    }
    this.escolherAnimacao(noChao, agora);
    return soltou;
  }

  escolherAnimacao(noChao, agora) {
    this.setFlipX(!this.olhandoDireita);
    if (noChao && this.estavaNoAr) this.aterrissandoAte = agora + J.aterrissagemMs;
    this.estavaNoAr = !noChao;
    if (agora < this.arremessandoAte) return;
    const v = this.body.velocity;
    let anim;
    if (!noChao) anim = v.y < 0 ? 'pulando' : 'caindo';
    else if (agora < (this.aterrissandoAte ?? 0)) anim = 'aterrissando';
    else anim = Math.abs(v.x) > 12 ? 'correndo' : 'parado';
    this.tocar(anim);
  }

  // Volta a um ponto de retorno, parado e com vida cheia (a forma turbinada se perde).
  reposicionar(x, y, agora = 0) {
    this.setForma('normal');
    this.body.reset(x, y);
    this.subindoComBotao = false;
    this.ultimoPedidoPulo = -Infinity;
    this.atordoadoAte = 0;
    this.vida = J.coracoes;
    this.invencivelAte = agora + J.invencivelMs;
  }
}

function aproximar(atual, alvo, passo) {
  if (atual < alvo) return Math.min(atual + passo, alvo);
  if (atual > alvo) return Math.max(atual - passo, alvo);
  return atual;
}
