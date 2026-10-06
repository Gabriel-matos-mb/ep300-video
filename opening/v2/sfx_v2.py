"""EP300 · V2 — sound design sintético (R$ 0, numpy). Regra: VOZ > SFX. Tudo macio, sem agudos agressivos (low-pass ~6–7 kHz),
picos baixos; o build ainda aplica ducking automático sob o diálogo. Substitui o 'risco/scratch' (Pencil Line) dos big numbers."""
import numpy as np
SR = 48000


def _stereo(x): return np.stack([x, x], 1).astype(np.float32)

def _lp(x, fc):
    # one-pole low-pass repetido 2x (12 dB/oit) — suficiente p/ tirar brilho agressivo
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0; s2 = 0.0
    b = 1 - a
    out = np.empty_like(x)
    for i, v in enumerate(x):
        s = a * s + b * v; s2 = a * s2 + b * s; out[i] = s2
    return out

def _lp_fast(x, fc):
    from numpy.fft import rfft, irfft
    n = len(x); X = rfft(x, n); f = np.fft.rfftfreq(n, 1 / SR); H = 1 / (1 + (f / fc) ** 4)
    return irfft(X * H, n)

def _env(n, a=.002, d=.1):
    t = np.arange(n) / SR; e = np.minimum(1, t / a) * np.exp(-t / d); return e

def tickup(dur=1.1, f0=620., f1=1150.):
    """contagem: tiques de madeira macios que aceleram e sobem de tom (acompanha o contador)."""
    n = int((dur + .15) * SR); y = np.zeros(n)
    t = 0.0; k = 0
    while t < dur:
        p = t / dur; f = f0 + (f1 - f0) * p
        m = int(.03 * SR); tt = np.arange(m) / SR
        tick = np.sin(2 * np.pi * f * tt) * np.exp(-tt / .008) + .4 * np.sin(2 * np.pi * f * 2.01 * tt) * np.exp(-tt / .004)
        i = int(t * SR); y[i:i + m] += tick[:max(0, n - i)][:m] * (.35 + .5 * p)
        t += .11 - .075 * p
    y = _lp_fast(y, 6500)
    # remate suave (assenta o número)
    m = int(.22 * SR); tt = np.arange(m) / SR; i = int(dur * SR)
    y[i:i + m] += (np.sin(2 * np.pi * 220 * tt) * np.exp(-tt / .07) * .5)[:max(0, n - i)][:m]
    return _stereo(y * .55)

def thump(dur=.55):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 42 + 60 * np.exp(-t / .05); ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / .16) * .9
    nz = np.random.RandomState(3).randn(n); nz = _lp_fast(nz, 500) * np.exp(-t / .03) * .5
    return _stereo(_lp_fast(y + nz, 900) * .8)

def pop(dur=.18):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 420 + 900 * (1 - np.exp(-t / .012)); ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / .03)
    return _stereo(_lp_fast(y, 5000) * .6)

def party(dur=1.6):
    """300: estouro surdo + confete (crepitar de papel) + língua de sogra (2 sopros curtos), tudo curto e baixo."""
    n = int(dur * SR); y = np.zeros(n); rs = np.random.RandomState(300)
    # estouro
    m = int(.25 * SR); t = np.arange(m) / SR
    pop_ = np.sin(2 * np.pi * np.cumsum(90 + 260 * np.exp(-t / .02)) / SR) * np.exp(-t / .06)
    nz = _lp_fast(rs.randn(m), 3500) * np.exp(-t / .05)
    y[:m] += pop_ * .9 + nz * .5
    # confete: milhares de micro-estalos
    m = int(1.0 * SR); c = np.zeros(m)
    idx = np.sort((rs.exponential(.28, 220) * SR).astype(int)); idx = idx[idx < m - 200]
    for i in idx:
        L = 160; tt = np.arange(L) / SR
        c[i:i + L] += rs.randn(L) * np.exp(-tt / .0025) * (0.25 + .5 * rs.rand()) * np.exp(-i / SR / .5)
    c = _lp_fast(c, 6000)
    y[int(.03 * SR):int(.03 * SR) + m] += c * .5
    # língua de sogra: sopro com palheta (tom subindo + tremolo) — 2x
    for st, ln in ((.22, .34), (.66, .40)):
        L = int(ln * SR); tt = np.arange(L) / SR
        f = 520 + 380 * np.sin(np.pi * tt / ln * .5) ** 1.5 + 12 * np.sin(2 * np.pi * 28 * tt)
        ph = np.cumsum(f) / SR * 2 * np.pi
        tone = (np.sin(ph) + .5 * np.sin(2 * ph) + .25 * np.sin(3 * ph)) * (.65 + .35 * np.sin(2 * np.pi * 30 * tt))
        air = _lp_fast(rs.randn(L), 4000) * .25
        env = np.minimum(1, tt / .02) * np.minimum(1, (ln - tt) / .06)
        i = int(st * SR); y[i:i + L] += (tone * .5 + air) * env * .55
    y = _lp_fast(y, 6500)
    return _stereo(y / max(1, np.abs(y).max()) * .55)

def rise(dur=1.0):
    """subida curta e macia (revelação/escala)."""
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 * (2 ** (2.2 * t / dur)); ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.minimum(1, t / .1) * np.minimum(1, (dur - t) / .08) * .5
    y += _lp_fast(np.random.RandomState(5).randn(n), 1800) * .18 * (t / dur)
    return _stereo(_lp_fast(y, 4500) * .8)

SYN = {'thump': thump, 'pop': pop, 'party': party, 'rise': rise}

def make(key):
    if key.startswith('tickup'):
        d = float(key[6:] or 1.1); return tickup(d)
    if key.startswith('rise') and len(key) > 4:
        return rise(float(key[4:]))
    return SYN[key]()
