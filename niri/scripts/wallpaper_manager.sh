#!/bin/bash

WALLPAPER_DIR="/home/astro/wallpapers"
MAX_WALLPAPERS=20
SCRIPT_DIR="$(dirname "$0")"

# 1. Crear el directorio si no existe
mkdir -p "$WALLPAPER_DIR"

# 2. Generar un nombre de archivo único basado en la fecha y hora
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
NEW_WALLPAPER="$WALLPAPER_DIR/fractal_${TIMESTAMP}.png"

echo "Generando nuevo fractal..."
# python3 "$SCRIPT_DIR/generate_fractal.py" "$NEW_WALLPAPER"
"$HOME/.local/share/pyfracgen-venv/bin/python" "$SCRIPT_DIR/generate_fractal.py" "$NEW_WALLPAPER"

if [ $? -ne 0 ]; then
    echo "Error al generar el fractal."
    exit 1
fi

# 3. Mantener solo las últimas MAX_WALLPAPERS imágenes, borrando las más antiguas
cd "$WALLPAPER_DIR" || exit
ls -t *.png 2>/dev/null | tail -n +$((MAX_WALLPAPERS + 1)) | xargs -r rm --

# 4. Aplicar el fondo de pantalla con swaybg
# Terminamos cualquier instancia previa de swaybg para iniciar una nueva con la imagen fresca
killall swaybg 2>/dev/null
swaybg -i "$NEW_WALLPAPER" -m fill &

echo "Fondo de pantalla establecido: $NEW_WALLPAPER"
