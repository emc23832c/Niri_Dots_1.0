import os
import random
import sys
import matplotlib
matplotlib.use('Agg')
import pyfracgen as pf
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib import colormaps

# --- Paleta fría (azules, verdes, morados, negros) --------------------------
# Curada a mano y verificada una por una contra matplotlib. Se excluyen a
# propósito los colormaps cálidos del set original (hot, autumn, spring,
# Wistia, jet, rainbow, hsv, nipy_spectral, pink, Oranges, Reds, jet) para que
# combine con el resto del sistema (waybar/rofi en azul oscuro + aqua).
COOL_CMAPS = [
    'viridis', 'viridis_r', 'cividis', 'cividis_r',
    'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r',
    'Blues', 'Blues_r', 'Greens', 'Greens_r', 'Purples', 'Purples_r',
    'PuBu', 'PuBu_r', 'PuBuGn', 'PuBuGn_r', 'BuGn', 'BuGn_r',
    'GnBu', 'GnBu_r', 'BuPu', 'BuPu_r',
    'ocean', 'ocean_r', 'winter', 'winter_r', 'cool', 'cool_r',
    'bone', 'bone_r', 'cubehelix', 'cubehelix_r',
]

# Pares fríos para el módulo Lyapunov (necesita dos colormaps: uno para zonas
# "ordenadas" y otro para zonas "caóticas"). bone/bone_r es del repo original;
# se agregan un par más para variar sin salirse del tono frío.
LYAPUNOV_CMAP_PAIRS = [
    ("bone", "bone_r"),
    ("PuBu", "PuBu_r"),
    ("Blues", "Blues_r"),
]

# --- Variedad de formas de fractal -------------------------------------------
# pyfracgen soporta distintas "funciones de actualización" para Mandelbrot y
# Julia (power, conj_power, cosine, sine, exponential, magnetic_1, magnetic_2).
# Se probaron las 7 con varios valores random antes de elegir estas 3:
# cosine/sine/exponential dieron imágenes casi vacías con los límites usados
# aquí, y magnetic_1 salía plano/aburrido tanto en Mandelbrot como en Julia.
# power, conj_power y magnetic_2 dieron resultados ricos y consistentes.
UPDATE_FUNCS = [pf.funcs.power, pf.funcs.conj_power, pf.funcs.magnetic_2]


def get_random_cmap():
    return random.choice(COOL_CMAPS)


def get_random_update_func():
    return random.choice(UPDATE_FUNCS)


def cool_tint(output_path, red=0.45, green=0.85, blue=1.15):
    """Aplica un tinte frío por post-procesamiento (baja el rojo, sube el
    azul). Se usa en el buddhabrot porque, por cómo funciona el algoritmo
    (arma el color combinando 3 renders en los canales R/G/B), su núcleo
    sale naturalmente cálido/anaranjado sin importar qué colormap se use --
    esta es la forma confiable de corregirlo hacia el tono frío."""
    img = Image.open(output_path).convert('RGB')
    arr = np.array(img).astype(float)
    arr[:, :, 0] *= red
    arr[:, :, 1] *= green
    arr[:, :, 2] *= blue
    arr = np.clip(arr, 0, 255).astype('uint8')
    Image.fromarray(arr).save(output_path)


# --- Zoom aleatorio "garantizado interesante" --------------------------------
# En pyfracgen, un pixel que NUNCA escapa (interior del set) queda en 0, y uno
# que escapa casi de inmediato (exterior lejano/vacío) también queda en un
# valor bajo -- solo los pixeles cerca del borde real del fractal (donde está
# todo el detalle) tienen valores altos y variados. Por eso la varianza de una
# región es un buen indicador de "qué tan interesante" se ve: varianza baja =
# zona plana (todo interior o todo vacío), varianza alta = borde con detalle.

def _render_scout(fractal_type, xbound, ybound, update_func, c, maxiter):
    """Render barato (baja resolución) solo para escanear la estructura."""
    if fractal_type == 'mandelbrot':
        return pf.mandelbrot(xbound, ybound, update_func, width=192, height=108, dpi=1, maxiter=maxiter)
    else:
        return next(pf.julia([c], xbound=xbound, ybound=ybound, update_func=update_func,
                              maxiter=maxiter, width=192, height=108, dpi=1))

def find_interesting_bounds(fractal_type, xbound, ybound, update_func, c=None,
                             zoom_frac_range=(0.08, 0.4), scout_maxiter=150):
    """Escanea un render barato del fractal completo y devuelve un (xbound,
    ybound, maxiter) nuevo -- más zoomeado, centrado en una zona con mucho
    detalle de borde en vez de interior plano o exterior vacío. Mantiene el
    mismo aspecto 16:9 que el render final, para no deformar la imagen."""
    scout = _render_scout(fractal_type, xbound, ybound, update_func, c, scout_maxiter)
    arr = scout.image_array
    ny, nx = arr.shape

    (xmin, xmax), (ymin, ymax) = xbound, ybound
    full_w, full_h = xmax - xmin, ymax - ymin

    zoom_frac = random.uniform(*zoom_frac_range)
    win_w = max(16, int(nx * zoom_frac))
    win_h = max(9, int(ny * zoom_frac))
    step = max(2, win_w // 4)

    candidates = []
    for iy in range(0, ny - win_h, step):
        for ix in range(0, nx - win_w, step):
            score = arr[iy:iy + win_h, ix:ix + win_w].std()
            candidates.append((score, ix, iy))

    if not candidates:
        return xbound, ybound, 300

    candidates.sort(key=lambda t: t[0], reverse=True)
    top_n = max(1, len(candidates) // 10)  # top 10% más interesante
    _, ix, iy = random.choice(candidates[:top_n])

    cx = xmin + (ix + win_w / 2) * full_w / nx
    cy = ymin + (iy + win_h / 2) * full_h / ny
    half_w = (win_w / nx) * full_w / 2
    half_h = (win_h / ny) * full_h / 2

    new_xbound = (cx - half_w, cx + half_w)
    new_ybound = (cy - half_h, cy + half_h)
    # los zooms más profundos necesitan más iteraciones para verse nítidos,
    # no borrosos/planos -- se compensa subiendo maxiter según qué tanto se acercó
    new_maxiter = min(1000, int(300 / zoom_frac))
    return new_xbound, new_ybound, new_maxiter


def generate_mandelbrot(output_path):
    xbound, ybound = (-2.0, 1.0), (-1.5, 1.5)
    update_func = get_random_update_func()
    maxiter = 300
    if random.random() < 0.65:  # 65% de las veces, hace zoom a una zona interesante
        xbound, ybound, maxiter = find_interesting_bounds('mandelbrot', xbound, ybound, update_func)
    res = pf.mandelbrot(xbound, ybound, update_func, width=192, height=108, dpi=10, maxiter=maxiter)
    stacked = pf.images.get_stacked_cmap(colormaps[get_random_cmap()], 50)
    pf.images.image(res, cmap=stacked, gamma=0.8)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_julia(output_path):
    c = complex(random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8))
    update_func = get_random_update_func()
    xbound, ybound = (-1.5, 1.5), (-1.5, 1.5)
    maxiter = 300
    if random.random() < 0.65:
        xbound, ybound, maxiter = find_interesting_bounds('julia', xbound, ybound, update_func, c=c)
    res_gen = pf.julia([c], xbound=xbound, ybound=ybound, update_func=update_func, maxiter=maxiter, width=192, height=108, dpi=10)
    res = next(res_gen)
    pf.images.image(res, cmap=colormaps[get_random_cmap()], gamma=0.8)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_lyapunov(output_path):
    string = random.choice(["AB", "AAB", "ABB", "ABAB", "AABB", "ABBA"])
    cmap_neg, cmap_pos = random.choice(LYAPUNOV_CMAP_PAIRS)
    res = pf.lyapunov(string, (2.5, 3.4), (3.4, 4.0), width=192, height=108, dpi=10, ninit=500, niter=500)
    pf.images.markus_lyapunov_image(res, colormaps[cmap_neg], colormaps[cmap_pos], gammas=(8, 1))
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_randomwalk(output_path):
    res = pf.randomwalk(niter=500000, width=192, height=108, dpi=10)
    pf.images.image(res, cmap=colormaps[get_random_cmap()], gamma=1.0)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_buddhabrot(output_path):
    res = pf.buddhabrot((-1.75, 0.85), (-1.10, 1.10), ncvals=200000, update_func=pf.funcs.power, horizon=1.0e5, maxiters=(50, 200, 1000), width=192, height=108, dpi=10)
    pf.images.nebula_image(tuple(res), gamma=0.4)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    cool_tint(output_path)  # corrige el núcleo cálido natural del algoritmo

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_fractal.py <ruta_de_salida>")
        sys.exit(1)
    
    output_path = sys.argv[1]
    fractal_type = random.choice(['mandelbrot', 'julia', 'lyapunov', 'randomwalk', 'buddhabrot'])
    
    print(f"Generando fractal tipo: {fractal_type}...")
    try:
        if fractal_type == 'mandelbrot': generate_mandelbrot(output_path)
        elif fractal_type == 'julia': generate_julia(output_path)
        elif fractal_type == 'lyapunov': generate_lyapunov(output_path)
        elif fractal_type == 'randomwalk': generate_randomwalk(output_path)
        elif fractal_type == 'buddhabrot': generate_buddhabrot(output_path)
        print(f"Guardado exitosamente en: {output_path}")
    except Exception as e:
        print(f"Error al generar el fractal: {e}")
        sys.exit(1)
