# Íconos Nerd Font para waybar (y similares)

Referencia rápida de símbolos verificados contra el dataset oficial de
[Nerd Fonts](https://www.nerdfonts.com/cheat-sheet) (`glyphnames.json`),
organizados por categoría según para qué se usan normalmente en una barra
de estado tipo waybar. No es el catálogo completo (son más de 10,000
íconos en total) -- es una selección curada de los que más se usan en
este tipo de configuración.

## Cómo usarlos

1. Necesitas una Nerd Font instalada (ver el README de instalación).
2. En `config.jsonc`, el carácter va directo en el campo `"format"` de
   cada módulo, por ejemplo: `"format": "{icon} {capacity}%"` en battery,
   o pegado directo si es un ícono fijo como el logo de una app.
3. Puedes copiar el carácter directamente de este archivo (columna
   "Símbolo"), o usar el código Unicode (columna "Código") si tu editor
   te deja pegarlo así.
4. **Ojo con el formato del código:** la mayoría son `\uXXXX` (4 dígitos,
   plano básico de Unicode). Los íconos de Material Design (prefijo `md-`)
   usan `\UXXXXXXXX` (8 dígitos, mayúscula) porque están fuera de ese
   plano básico -- si tu herramienta espera `\u` con 4 dígitos, esos
   específicamente no van a funcionar igual, usa el carácter directo en
   su lugar.
5. Si un símbolo no se ve (aparece como cuadro vacío ☐), normalmente es
   que la fuente no está bien instalada o el `font-family` en `style.css`
   no coincide exactamente con el nombre real de la fuente -- no es que
   el código esté mal.
6. Catálogo completo y buscador visual: <https://www.nerdfonts.com/cheat-sheet>

---

## Sistema y estado

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF240` | `fa-battery_full` | batería llena |
|  | `\uF241` | `fa-battery_three_quarters` | batería 75% |
|  | `\uF242` | `fa-battery_half` | batería 50% |
|  | `\uF243` | `fa-battery_quarter` | batería 25% |
|  | `\uF244` | `fa-battery_empty` | batería vacía |
|  | `\uF0E7` | `fa-bolt` | cargando / rayo |
|  | `\uF028` | `fa-volume_up` | volumen alto |
|  | `\uF027` | `fa-volume_down` | volumen bajo |
|  | `\uF026` | `fa-volume_off` | silencio |
|  | `\uF185` | `fa-sun_o` | brillo / modo claro |
| 󰽥 | `\U000F0F65` | `md-moon_waning_crescent` | modo oscuro / luna |
|  | `\uF1EB` | `fa-wifi` | wifi |
| 󰖪 | `\U000F05AA` | `md-wifi_off` | wifi desconectado |
|  | `\uF293` | `fa-bluetooth` | bluetooth |
|  | `\uF294` | `fa-bluetooth_b` | bluetooth (alt) |
| 󰻠 | `\U000F0EE0` | `md-cpu_64_bit` | CPU |
| 󰍛 | `\U000F035B` | `md-memory` | memoria RAM |
|  | `\uF0A0` | `fa-hdd_o` | disco / almacenamiento |
|  | `\uF2C7` | `fa-thermometer_full` | temperatura alta |
|  | `\uF2C9` | `fa-thermometer_half` | temperatura media |
|  | `\uF2CB` | `fa-thermometer_empty` | temperatura baja |
|  | `\uF017` | `fa-clock_o` | reloj |
|  | `\uF073` | `fa-calendar` | calendario |
| 󰈀 | `\U000F0200` | `md-ethernet` | red / ethernet |
|  | `\uF023` | `fa-lock` | bloqueado |
|  | `\uF09C` | `fa-unlock` | desbloqueado |
|  | `\uF011` | `fa-power_off` | apagar |
| 󰜉 | `\U000F0709` | `md-restart` | reiniciar |
|  | `\uF013` | `fa-cog` | ajustes |
|  | `\uF085` | `fa-cogs` | ajustes (varios) |
|  | `\uF0F3` | `fa-bell` | notificación |
|  | `\uF1F6` | `fa-bell_slash` | notificaciones silenciadas |
|  | `\uF002` | `fa-search` | buscar |
|  | `\uF00C` | `fa-check` | check / correcto |
|  | `\uF00D` | `fa-times` | cerrar / error |
|  | `\uF071` | `fa-exclamation_triangle` | advertencia |
|  | `\uF05A` | `fa-info_circle` | información |
|  | `\uF062` | `fa-arrow_up` | flecha arriba (stats) |
|  | `\uF063` | `fa-arrow_down` | flecha abajo (stats) |
|  | `\uF0D8` | `fa-caret_up` | caret arriba |
|  | `\uF0D7` | `fa-caret_down` | caret abajo |

## Logos de distros Linux

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF303` | `linux-archlinux` | Arch Linux |
|  | `\uF313` | `linux-nixos` | NixOS |
|  | `\uF31B` | `linux-ubuntu` | Ubuntu |
|  | `\uF306` | `linux-debian` | Debian |
|  | `\uF30A` | `linux-fedora` | Fedora |
|  | `\uF30E` | `linux-linuxmint` | Linux Mint |
|  | `\uF312` | `linux-manjaro` | Manjaro |
|  | `\uF314` | `linux-opensuse` | openSUSE |
|  | `\uF30D` | `linux-gentoo` | Gentoo |
|  | `\uF32E` | `linux-void` | Void Linux |
|  | `\uF302` | `linux-apple` | macOS |
| 󰖳 | `\U000F05B3` | `md-microsoft_windows` | Windows |
|  | `\uF31A` | `linux-tux` | Tux (genérico) |

## Navegadores

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF269` | `fa-firefox` | Firefox |
|  | `\uF268` | `fa-chrome` | Chrome |
|  | `\uF26A` | `fa-opera` | Opera |
| 󰇩 | `\U000F01E9` | `md-microsoft_edge` | Edge |
|  | `\uF132` | `fa-shield` | Brave (no existe ícono oficial, se usa un escudo) |

## Terminales y editores

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF120` | `fa-terminal` | terminal (genérico) |
| 󰆍 | `\U000F018D` | `md-console` | consola |
|  | `\uF121` | `fa-code` | editor / código |
|  | `\uE70C` | `dev-visualstudio` | Visual Studio Code |
|  | `\uE7C5` | `dev-vim` | Vim |
| 󰌠 | `\U000F0320` | `md-language_python` | Python |

## Archivos y ofimática

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF0F6` | `fa-file_text_o` | documento de texto |
|  | `\uF1C1` | `fa-file_pdf_o` | PDF |
|  | `\uF1C2` | `fa-file_word_o` | Word |
|  | `\uF1C3` | `fa-file_excel_o` | Excel |
|  | `\uF1C4` | `fa-file_powerpoint_o` | PowerPoint |
|  | `\uF07B` | `fa-folder` | carpeta |
|  | `\uF07C` | `fa-folder_open` | carpeta abierta |

## Multimedia

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF001` | `fa-music` | música |
|  | `\uF04B` | `fa-play` | play |
|  | `\uF04C` | `fa-pause` | pausa |
|  | `\uF051` | `fa-step_forward` | siguiente |
|  | `\uF048` | `fa-step_backward` | anterior |
|  | `\uF025` | `fa-headphones` | audífonos |
| 󰓇 | `\U000F04C7` | `md-spotify` | Spotify |

## Chat y comunicación

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF086` | `fa-comments` | chat genérico |
| 󰙯 | `\U000F066F` | `md-discord` | Discord |
| 󰖣 | `\U000F05A3` | `md-whatsapp` | WhatsApp |
| 󰒱 | `\U000F04B1` | `md-slack` | Slack |
|  | `\uF2C6` | `fa-telegram` | Telegram |

## Git y desarrollo

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF1D3` | `fa-git` | git |
|  | `\uF09B` | `fa-github` | GitHub |
|  | `\uF126` | `fa-code_fork` | fork / rama |
|  | `\uF418` | `oct-git_branch` | rama de git |
|  | `\uF417` | `oct-git_commit` | commit |

## Clima

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uE30D` | `weather-day_sunny` | soleado |
|  | `\uE312` | `weather-cloudy` | nublado |
|  | `\uE318` | `weather-rain` | lluvia |
|  | `\uE31A` | `weather-snow` | nieve |
|  | `\uE31D` | `weather-thunderstorm` | tormenta |
|  | `\uE313` | `weather-fog` | niebla |
|  | `\uE32B` | `weather-night_clear` | despejado de noche |
|  | `\uE34B` | `weather-strong_wind` | viento |

## Separadores estilo powerline

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uE0B2` | `pl-right_hard_divider` | separador sólido > |
|  | `\uE0B0` | `pl-left_hard_divider` | separador sólido < |
|  | `\uE0B3` | `pl-right_soft_divider` | separador fino > |
|  | `\uE0B1` | `pl-left_soft_divider` | separador fino < |

## IA y robótica

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uEC82` | `cod-claude` | Claude |
|  | `\uEC81` | `cod-openai` | OpenAI / ChatGPT (o "IA" genérico) |
|  | `\uEE9C` | `fa-brain` | Ollama (no existe ícono oficial, se usa un cerebro) |
| 󰭆 | `\U000F0B46` | `md-robot_industrial` | ROS / robótica |
|  | `\uE794` | `dev-cmake` | CMake |

## Juegos

| Símbolo | Código | Nombre | Uso |
|:---:|---|---|---|
|  | `\uF1B6` | `fa-steam` | Steam |
|  | `\uF11B` | `fa-gamepad` | juego genérico (control) |
