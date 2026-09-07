# Waybar personalizada para niri (Arch Linux)

Este `config.jsonc` y `style.css` son una versión personalizada de
[waybar-niri-workspaces-enhanced](https://github.com/justbuchanan/waybar-niri-workspaces-enhanced)
de **justbuchanan**. El módulo de workspaces (el `.so` que se compila con Rust)
es el trabajo original del autor del repositorio; el tema visual (colores,
íconos, botón de apagado, layout) fue armado a la medida con la ayuda de
Claude (Anthropic), a partir de ese proyecto base.

## Qué incluye

- Workspaces/ventanas activas de niri, con íconos por app.
- Hora, batería, volumen, brillo y temperatura.
- Logo de Arch Linux clickeable al centro (abre `rofi -show drun`), con comentario
  para cambiarlo por el de NixOS.
- Botón de apagado.
- Tema azul oscuro con acentos en verde aqua.

## Requisitos e instalación de niri

Primero lo primero: `niri` (el compositor de Wayland) y sus dependencias
principales. `niri` está en el repositorio oficial `extra` de Arch, **no
hace falta AUR** para esto.

```bash
sudo pacman -S niri xwayland-satellite alacritty
```

- `niri`: el compositor en sí.
- `xwayland-satellite`: deja correr apps que todavía no soportan Wayland
  nativo (X11) dentro de niri. No es obligatorio, pero muchas apps de
  escritorio comunes todavía lo necesitan.
- `alacritty`: una terminal. La necesitas para poder escribir comandos
  (los que siguen en este mismo README). Puedes usar otra si prefieres
  (`kitty`, `ghostty`, `foot` -- esta waybar ya trae íconos para varias),
  solo reemplaza `alacritty` por la que elijas en todo lo que sigue.

**Cómo arrancar niri:**

- Si usas un gestor de sesión gráfico (un login manager, como SDDM o
  greetd): al iniciar sesión, elige "niri" en el selector de sesión que
  aparece en la pantalla de login (junto a tu usuario/contraseña).
- Si NO usas gestor de sesión gráfico (entras directo a una terminal en
  texto tras prender la PC): inicia sesión normal con tu usuario y
  contraseña, y luego corre:

  ```bash
  niri-session
  ```

  Esto arranca niri junto con las variables de entorno necesarias para
  que todo lo demás (waybar, rofi, polkit, etc.) funcione bien. Evita
  correr `niri` a secas (sin `-session`) para el uso diario -- es el
  mismo compositor, pero sin esa integración de sesión.

Una vez adentro de niri, ya puedes abrir una terminal
(`alacritty` o la que hayas instalado) para seguir con el resto de esta
guía: compilar el módulo de la waybar, instalar las fuentes, etc.

## Requisitos para esta waybar personalizada

- `waybar`
- `rust` (para compilar el módulo, **1.85 o más nuevo** -- el proyecto usa
  `edition = "2024"` en `Cargo.toml`, con una versión más vieja de `rustc`
  falla el build)
- `git`
- `rofi` (lanzador de aplicaciones, para el botón del logo de Arch --
  las versiones recientes de rofi ya soportan Wayland de forma nativa; si
  al hacer click no abre nada, prueba el paquete `rofi-wayland` del AUR
  como alternativa)
- `pavucontrol` (para el click en el módulo de volumen)
- `brightnessctl` (para el scroll en el módulo de brillo)
- Una Nerd Font instalada (ver sección de fuentes más abajo)

Instalar lo básico:

```bash
sudo pacman -S waybar rust git rofi pavucontrol brightnessctl
```

## 1. Compilar el módulo de workspaces

```bash
cd ~
git clone https://github.com/justbuchanan/waybar-niri-workspaces-enhanced.git
cd waybar-niri-workspaces-enhanced
cargo build --release
```

Esto genera `target/release/libwaybar_niri_workspaces_enhanced.so`.

## 2. Copiar los archivos a `~/.config/waybar/`

```bash
mkdir -p ~/.config/waybar
cp target/release/libwaybar_niri_workspaces_enhanced.so \
   ~/.config/waybar/niri-workspaces-enhanced.so
```

Copia también `config.jsonc` y `style.css` (los que te compartió Claude) a
esa misma carpeta.

## 3. Ajustar `module_path`

Dentro de `config.jsonc`, en el bloque `"cffi/niri-workspaces-enhanced"`,
el campo `module_path` **tiene que ser una ruta absoluta literal** --
`waybar` usa `dlopen()` para cargarlo, y `dlopen()` no expande `~`.

```bash
echo "$HOME/.config/waybar/niri-workspaces-enhanced.so"
```

Pega ese resultado exacto como valor de `"module_path"`.

## 4. Autoarranque desde niri

En tu `config.kdl` de niri, evita `spawn-at-startup "waybar"` a secas --
niri puede lanzar waybar antes de que su propio socket IPC esté listo, y
el módulo de workspaces falla en silencio. Usa en su lugar:

```kdl
spawn-sh-at-startup "until niri msg workspaces >/dev/null 2>&1; do sleep 0.2; done; exec waybar"
```

## 5. Fuentes: que carguen los símbolos (guía para quien nunca usó Linux)

Esta waybar usa un montón de símbolos e íconos (batería, reloj, apps, etc.)
que **no vienen en las fuentes normales** de tu sistema. Vienen de una
"Nerd Font" -- una fuente normal (como Arial o Roboto) a la que le pegaron
miles de íconos extra. Si no la instalas, en vez de íconos vas a ver
cuadritos vacíos (☐) o espacios en blanco donde debería haber un símbolo.

Todo esto se hace desde la **terminal** (una ventana negra donde escribes
comandos de texto en vez de hacer click). Si no sabes cómo abrir una:
en niri, por defecto el atajo es **Super (tecla Windows) + Return/Enter**,
y te debería abrir una terminal. Si no funciona, revisa tu `config.kdl` de
niri para ver qué terminal tienes configurada, o usa el ícono de Arch de la
waybar (una vez que la tengas corriendo) que abre rofi, donde puedes
buscar "terminal" o el nombre de la que instalaste (ghostty, alacritty, kitty).

Una vez que tengas la terminal abierta, sigue estos pasos **en orden**,
copiando y pegando cada bloque de texto tal cual (para pegar en la mayoría
de terminales de Linux se usa `Ctrl+Shift+V`, no `Ctrl+V`):

**Paso 1 -- Crea la carpeta donde van a vivir las fuentes de tu usuario:**

```bash
mkdir -p ~/.local/share/fonts
```

Esto no muestra nada en pantalla si funcionó -- así es como debe verse.

**Paso 2 -- Descarga la fuente Nerd Font "Hack":**

```bash
cd ~/Downloads
wget https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hack.zip
```

Si te dice `wget: command not found`, instala wget primero con
`sudo pacman -S wget` (te va a pedir tu contraseña de usuario, es normal,
no se ve nada mientras la escribes, solo escríbela y da Enter) y vuelve a
correr el comando de arriba.

**Paso 3 -- Descomprime el .zip dentro de la carpeta de fuentes:**

```bash
unzip Hack.zip -d ~/.local/share/fonts/HackNerd
```

Si te dice `unzip: command not found`, instala unzip:
`sudo pacman -S unzip`, y repite el comando.

**Paso 4 -- Dile al sistema que hay fuentes nuevas:**

```bash
fc-cache -fv
```

Esto va a imprimir un montón de líneas en pantalla, es normal, significa
que está revisando todas tus fuentes. Espera a que termine y te devuelva
el cursor para escribir de nuevo.

**Paso 5 -- Confirma que quedó instalada correctamente:**

```bash
fc-list | grep -i "Hack Nerd"
```

Deberías ver varias líneas con rutas de archivo terminando en `.ttf`, algo
como:

```
/home/tu_usuario/.local/share/fonts/HackNerd/HackNerdFontPropo-Regular.ttf: Hack Nerd Font Propo:style=Regular
```

Si no ves ninguna línea, algo falló en los pasos anteriores -- revisa que
el `.zip` se haya descomprimido bien (`ls ~/.local/share/fonts/HackNerd`
debería mostrarte archivos `.ttf`).

**Paso 6 -- Confirma que el nombre coincide con el que usa `style.css`:**

Fíjate en el nombre exacto que te devolvió el comando anterior, por ejemplo
`Hack Nerd Font Propo`. Abre `style.css` y busca la línea:

```css
font-family: "Hack Nerd Font Propo";
```

Si el nombre que te dio `fc-list` es distinto (a veces varía según la
versión de la fuente), cámbialo ahí para que sea idéntico, letra por letra.

**Paso 7 -- Reinicia waybar para que use la fuente nueva:**

```bash
killall waybar && waybar &
```

**Si después de todo esto los símbolos siguen sin verse:** lo más probable
es que el nombre del Paso 6 no haya quedado exactamente igual, o que
`killall waybar` no haya encontrado el proceso (prueba primero solo
`killall waybar`, y si dice `no process found`, es que waybar no estaba
corriendo -- solo ejecuta `waybar &` para abrirlo).

## 6. El botón de apagado

El botón corre `systemctl poweroff` directo. En la mayoría de sesiones de
escritorio en Arch esto ya funciona sin pedir contraseña (permiso otorgado
por `systemd-logind`/`polkit` a la sesión activa). Si en tu caso pide
contraseña, crea `/etc/polkit-1/rules.d/50-poweroff.rules`:

```js
polkit.addRule(function(action, subject) {
    if ((action.id == "org.freedesktop.login1.power-off" ||
         action.id == "org.freedesktop.login1.reboot") &&
        subject.isInGroup("wheel")) {
        return polkit.Result.YES;
    }
});
```

y reinicia polkit: `sudo systemctl restart polkit`.

## 7. Íconos de aplicaciones

En `window-icons` dentro de `config.jsonc` hay iconos para varias apps
(navegadores, terminales, ofimática, etc.), añadidos a los que ya traía el
repo original. La clave de cada entrada es el `app_id` que reporta la
ventana. Son una estimación razonable, pero pueden variar según cómo esté
empaquetada la app en tu sistema.

Ya se confirmaron y están activos (vía `niri msg windows`, con el `app_id`
real): Zen Browser, GeoGebra, LibreOffice Writer, Aisleriot/Sol y Obsidian.

Quedan **comentados a propósito**: Wolfram Mathematica, GNU Octave, y las
variantes de LibreOffice Calc/Impress (solo se confirmó Writer). Si usas
alguna de esas, necesitas su `app_id` exacto:

```bash
niri msg windows
```

**Ojo con un error común:** el comando es `niri msg windows` (con "msg" y
"windows" completos). Si en vez de eso escribes solo `niri`, vas a ver el
mensaje `A niri session is already running.` -- eso pasa porque `niri` a
secas intenta abrir un compositor nuevo (y ya tienes uno corriendo), no es
un error de verdad, es que el comando no era el correcto.

Corre `niri msg windows` con la app abierta que quieres identificar, busca
la línea de esa ventana, copia el valor exacto de `app_id`, y reemplázalo
en la entrada comentada correspondiente de `config.jsonc` (quitando el `//`
de adelante para activarla).

## Reiniciar waybar tras cualquier cambio

```bash
killall waybar && waybar &
```

O, para ver errores en vivo mientras pruebas cambios:

```bash
killall waybar
waybar
```
