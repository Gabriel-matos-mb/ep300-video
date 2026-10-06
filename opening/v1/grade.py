"""Aproximação numérica do Lumetri (Correção básica) que o Gabriel aplicou por câmera no Premiere
(projeto 'EP300_ABERTURA_V0 Cópia.prproj', sequência EP300_SYNC_3CAM). Gera LUT 3D (.cube) por câmera
para o PROXY. No Premiere, a cor oficial continua sendo o Lumetri dele (ver README_EDITAVEL_V1).
Valores lidos do .prproj (Exposição, Contraste, Realces, Sombras, Brancos, Pretos, Temperatura, Tonalidade,
Saturação, Vibração; vinheta só na CAM_GERAL)."""
import os, numpy as np
LUMETRI = {
    'W': dict(temp=-2.0, tint=-8.5, sat=102, exp=0.74, con=40.0, hi=-7.6, sh=21.6, wh=-18.8, bl=0.0, vib=20, vig=-1.13),
    'G': dict(temp=-9.94, tint=-0.05, sat=121.46, exp=0.989, con=-40.73, hi=29.15, sh=21.22, wh=-17.54, bl=0.61, vib=20, vig=0),
    'L': dict(temp=-2.0, tint=-8.5, sat=102, exp=0.60, con=43.6, hi=-7.6, sh=21.6, wh=-18.8, bl=0.0, vib=20, vig=0),
}
def s2l(x): return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def l2s(x): x = np.clip(x, 0, None); return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)
def apply(rgb, p):
    """rgb em [0,1] sRGB -> sRGB. Aproximação perceptual (não é o Lumetri exato)."""
    x = s2l(rgb) * (2 ** p['exp'])
    # temperatura/tonalidade (escala Lumetri ±100) -> ganhos por canal
    t, g = p['temp'] / 100, p['tint'] / 100
    x = x * np.array([1 + 0.25 * t, 1 - 0.25 * g, 1 - 0.25 * t])
    y = l2s(x)
    Y = (y * [0.2126, 0.7152, 0.0722]).sum(-1, keepdims=True)
    # sombras/realces/brancos/pretos: curvas suaves em luma
    Yc = np.clip(Y, 0, 1.5)
    d = (p['sh'] / 100) * 0.22 * np.clip(1 - Yc / 0.5, 0, 1) ** 2 * (Yc / 0.5) * 2
    d += (p['hi'] / 100) * 0.22 * np.clip((Yc - 0.45) / 0.55, 0, 1) * (1 - np.clip((Yc - 0.85) / 0.4, 0, 1))
    d += (p['wh'] / 100) * 0.18 * np.clip((Yc - 0.65) / 0.35, 0, 1) ** 1.5
    d += (p['bl'] / 100) * 0.10 * np.clip(1 - Yc / 0.25, 0, 1)
    y = y + d
    # contraste em torno de 0.45 (S suave)
    c = p['con'] / 100 * 0.45
    y = 0.45 + (y - 0.45) * (1 + c)
    # compressão suave de altas luzes (evita estouro)
    y = np.where(y > 0.92, 0.92 + (1 - np.exp(-(y - 0.92) / 0.08)) * 0.08, y)
    Y = (y * [0.2126, 0.7152, 0.0722]).sum(-1, keepdims=True)
    chroma = y - Y
    satn = np.abs(chroma).max(-1, keepdims=True)
    k = p['sat'] / 100 * (1 + p['vib'] / 100 * 0.5 * np.clip(1 - satn / 0.35, 0, 1))
    return np.clip(Y + chroma * k, 0, 1)
def cube(cam, path, n=33):
    r = np.linspace(0, 1, n); B, G, R = np.meshgrid(r, r, r, indexing='ij')
    rgb = np.stack([R, G, B], -1).reshape(-1, 3)
    out = apply(rgb, LUMETRI[cam])
    with open(path, 'w') as f:
        f.write(f'TITLE "EP300 Lumetri aprox {cam}"\nLUT_3D_SIZE {n}\n')
        for v in out: f.write(f'{v[0]:.5f} {v[1]:.5f} {v[2]:.5f}\n')
    return path
def vf(cam, luts_dir, w=1280, h=720):
    p = cube(cam, os.path.join(luts_dir, f'LUMETRI_APROX_{cam}.cube'))
    s = f"lut3d='{p.replace(os.sep, '/').replace(':', chr(92) + ':')}'"
    if LUMETRI[cam]['vig']: s += ',vignette=angle=PI/5:mode=forward'
    return s
