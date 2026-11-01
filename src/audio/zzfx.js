// ZzFX - Zuper Zmall Zound Zynth (gerador de amostras, função zzfxG).
// Autor: Frank Force. Licença MIT. https://github.com/KilledByAPixel/ZzFX
// Copyright (c) 2019 Frank Force. A licença completa está em CREDITS.md.
//
// Adaptação deste projeto: só a parte que GERA as amostras. Quem toca é o src/audio/som.js, com o
// AudioContext único do jogo (o ZzFX original cria o seu próprio, e o iPhone tem limite de contextos).
// Os parâmetros seguem a ordem do ZzFX, então dá para criar sons no site do ZzFX e colar aqui.

export const ZZFX_TAXA = 44100;

export function zzfxG(
  volume = 1,
  randomness = 0.05,
  frequency = 220,
  attack = 0,
  sustain = 0,
  release = 0.1,
  shape = 0,
  shapeCurve = 1,
  slide = 0,
  deltaSlide = 0,
  pitchJump = 0,
  pitchJumpTime = 0,
  repeatTime = 0,
  noise = 0,
  modulation = 0,
  bitCrush = 0,
  delay = 0,
  sustainVolume = 1,
  decay = 0,
  tremolo = 0,
  filter = 0,
) {
  const PI2 = Math.PI * 2;
  const taxa = ZZFX_TAXA;
  const abs = Math.abs;
  const sign = (v) => (v < 0 ? -1 : 1);
  let startSlide = (slide *= (500 * PI2) / taxa / taxa);
  let startFrequency = (frequency *= ((1 + randomness * 2 * Math.random() - randomness) * PI2) / taxa);
  let modOffset = 0;
  let repeat = 0;
  let crush = 0;
  let jump = 1;
  let length;
  const b = [];
  let t = 0;
  let i = 0;
  let s = 0;
  let f;

  // filtro biquad (passa-baixa se filter > 0, passa-alta se < 0)
  const quality = 2;
  const w = (PI2 * abs(filter) * 2) / taxa;
  const cos = Math.cos(w);
  const alpha = Math.sin(w) / 2 / quality;
  const a0 = 1 + alpha;
  const a1 = (-2 * cos) / a0;
  const a2 = (1 - alpha) / a0;
  const b0 = (1 + sign(filter) * cos) / 2 / a0;
  const b1 = -(sign(filter) + cos) / a0;
  const b2 = b0;
  let x2 = 0;
  let x1 = 0;
  let y2 = 0;
  let y1 = 0;

  attack = attack * taxa || 9; // evita estalo quando o ataque é 0
  decay *= taxa;
  sustain *= taxa;
  release *= taxa;
  delay *= taxa;
  deltaSlide *= (500 * PI2) / taxa ** 3;
  modulation *= PI2 / taxa;
  pitchJump *= PI2 / taxa;
  pitchJumpTime *= taxa;
  repeatTime = (repeatTime * taxa) | 0;

  for (length = (attack + decay + sustain + release + delay) | 0; i < length; b[i++] = s * volume) {
    if (!(++crush % ((bitCrush * 100) | 0))) {
      s = shape
        ? shape > 1
          ? shape > 2
            ? shape > 3
              ? Math.sin(t ** 3) // 4 ruído
              : Math.max(Math.min(Math.tan(t), 1), -1) // 3 tangente
            : 1 - (((((2 * t) / PI2) % 2) + 2) % 2) // 2 serra
          : 1 - 4 * abs(Math.round(t / PI2) - t / PI2) // 1 triângulo
        : Math.sin(t); // 0 seno

      s =
        (repeatTime ? 1 - tremolo + tremolo * Math.sin((PI2 * i) / repeatTime) : 1) *
        sign(s) *
        abs(s) ** shapeCurve *
        (i < attack
          ? i / attack
          : i < attack + decay
            ? 1 - ((i - attack) / decay) * (1 - sustainVolume)
            : i < attack + decay + sustain
              ? sustainVolume
              : i < length - delay
                ? ((length - i - delay) / release) * sustainVolume
                : 0);

      s = delay
        ? s / 2 + (delay > i ? 0 : ((i < length - delay ? 1 : (length - i) / delay) * b[(i - delay) | 0]) / 2 / volume)
        : s;

      if (filter) s = y1 = b2 * x2 + b1 * (x2 = x1) + b0 * (x1 = s) - a2 * y2 - a1 * (y2 = y1);
    }

    f = (frequency += slide += deltaSlide) * Math.cos(modulation * modOffset++);
    t += f + f * noise * Math.sin(i ** 5);

    if (jump && ++jump > pitchJumpTime) {
      frequency += pitchJump;
      startFrequency += pitchJump;
      jump = 0;
    }

    if (repeatTime && !(++repeat % repeatTime)) {
      frequency = startFrequency;
      slide = startSlide;
      jump = jump || 1;
    }
  }
  return b;
}
