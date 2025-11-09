#!/usr/bin/env bash
# Launcher per il generatore audio da Markdown

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEFAULT_ARTICLE="$REPO_ROOT/bridging-the-gap-article-draft.md"
CACHE_DIR="$REPO_ROOT/output/audio"
PIP_EXTRA_ARGS=()
if [[ -n "${AUDIO_PLAYER_PIP_FLAGS:-}" ]]; then
    # shellcheck disable=SC2206
    PIP_EXTRA_ARGS=(${AUDIO_PLAYER_PIP_FLAGS})
fi
TARGET_FILE="$DEFAULT_ARTICLE"
EXTRA_ARGS=()
if (($#)); then
    if [[ "$1" != --* ]]; then
        TARGET_FILE="$1"
        shift
    fi
    if (($#)); then
        EXTRA_ARGS=("$@")
    fi
fi

log() {
    echo -e "$1"
}

detect_python() {
    if [[ -n "${PYTHON_BIN:-}" ]] && command -v "$PYTHON_BIN" >/dev/null 2>&1; then
        printf "%s" "$(command -v "$PYTHON_BIN")"
        return 0
    fi
    if command -v python3 >/dev/null 2>&1; then
        printf "%s" "$(command -v python3)"
        return 0
    fi
    if command -v python >/dev/null 2>&1; then
        printf "%s" "$(command -v python)"
        return 0
    fi
    return 1
}

join_by() {
    local sep="$1"
    shift || true
    if (($# == 0)); then
        echo ""
        return
    fi
    local IFS="$sep"
    echo "$*"
}

ITALIAN_VOICES=("it-IT-IsabellaNeural" "it-IT-DiegoNeural" "it-IT-ElsaNeural")
ENGLISH_VOICES=("en-US-GuyNeural" "en-GB-RyanNeural" "en-GB-SoniaNeural")
DEFAULT_VOICE_IT="it-IT-IsabellaNeural"
DEFAULT_VOICE_EN="en-US-GuyNeural"
SECTION_ROWS=()
MENU_LANGUAGE_ARGS=()
MENU_SECTION_ARGS=()
SELECTED_LANGUAGES=()
SELECTED_SECTION_LABELS=()
declare -A SECTION_TITLES=()
declare -A SECTION_LANGS=()

load_sections_for_menu() {
    SECTION_ROWS=()
    SECTION_TITLES=()
    SECTION_LANGS=()

    local pythonpath="$SCRIPT_DIR"
    if [[ -n "${PYTHONPATH:-}" ]]; then
        pythonpath="$SCRIPT_DIR:$PYTHONPATH"
    fi

    local raw_output
    if ! raw_output="$(
        PYTHONPATH="$pythonpath" SECTION_SOURCE="$TARGET_FILE" "$PYTHON_BIN" - <<'PY'
from pathlib import Path
import os
import sys

try:
    from audio_player import MarkdownAudioBuilder
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.stderr.write(f"Errore import audio_player: {exc}\n")
    sys.exit(1)

source = Path(os.environ["SECTION_SOURCE"])
builder = MarkdownAudioBuilder(source)
for idx, section in enumerate(builder.sections, 1):
    title = section["title"].replace("\n", " ").strip()
    print(f"{idx}\t{section['language']}\t{title}")
PY
    )"; then
        return 1
    fi

    if [[ -z "$raw_output" ]]; then
        return 1
    fi

    mapfile -t SECTION_ROWS <<<"$raw_output"

    if ((${#SECTION_ROWS[@]} == 0)); then
        return 1
    fi

    local row idx lang title
    for row in "${SECTION_ROWS[@]}"; do
        IFS=$'\t' read -r idx lang title <<<"$row"
        SECTION_TITLES["$idx"]="$title"
        SECTION_LANGS["$idx"]="$lang"
    done
    return 0
}

prompt_language_menu() {
    local input tokens token
    local -A chosen=()

    echo ""
    log "🌍 Seleziona le lingue da convertire:"
    echo " 1) Italiano"
    echo " 2) Inglese"
    echo "    Premi Invio per includerle entrambe"
    read -rp "Lingue (es. '1 2' oppure '1'): " input
    input="${input//,/ }"
    read -ra tokens <<<"$input"

    for token in "${tokens[@]}"; do
        case "${token,,}" in
        1 | it) chosen[it]=1 ;;
        2 | en) chosen[en]=1 ;;
        3 | all | both) chosen[it]=1 chosen[en]=1 ;;
        "" ) ;;
        *) log "⚠️  Lingua '${token}' non riconosciuta, ignorata." ;;
        esac
    done

    SELECTED_LANGUAGES=()
    if ((${#chosen[@]} == 0)); then
        SELECTED_LANGUAGES=(it en)
    else
        for lang in it en; do
            if [[ -n "${chosen[$lang]+_}" ]]; then
                SELECTED_LANGUAGES+=("$lang")
            fi
        done
    fi

    MENU_LANGUAGE_ARGS=()
    if ((${#SELECTED_LANGUAGES[@]} == 1)); then
        MENU_LANGUAGE_ARGS=(--language "${SELECTED_LANGUAGES[0]}")
    fi

    local readable=()
    for lang in "${SELECTED_LANGUAGES[@]}"; do
        case "$lang" in
        it) readable+=("italiano") ;;
        en) readable+=("inglese") ;;
        esac
    done
    log "🌍 Lingue selezionate: $(join_by ', ' "${readable[@]}")"
}

prompt_section_menu() {
    echo ""
    log "📚 Sezioni disponibili (${#SECTION_ROWS[@]}):"
    local row idx lang title
    for row in "${SECTION_ROWS[@]}"; do
        IFS=$'\t' read -r idx lang title <<<"$row"
        printf " %2d) [%s] %s\n" "$idx" "$lang" "$title"
    done
    echo "    Premi Invio per convertire tutte le sezioni."
    read -rp "Seleziona le sezioni (numeri separati da spazio): " section_input
    section_input="${section_input//,/ }"
    read -ra section_tokens <<<"$section_input"

    MENU_SECTION_ARGS=()
    SELECTED_SECTION_LABELS=()
    if ((${#section_tokens[@]} == 0)); then
        log "📑 Sezioni: tutte"
        return
    fi

    local -A seen=()
    local token trimmed
    for token in "${section_tokens[@]}"; do
        trimmed="${token//[[:space:]]/}"
        if [[ -z "$trimmed" ]]; then
            continue
        fi
        if [[ ! "$trimmed" =~ ^[0-9]+$ ]]; then
            log "⚠️  '$trimmed' non è un numero di sezione, ignorato."
            continue
        fi
        if [[ -z "${SECTION_TITLES[$trimmed]+_}" ]]; then
            log "⚠️  Sezione $trimmed non valida, ignorata."
            continue
        fi
        if [[ -n "${seen[$trimmed]+_}" ]]; then
            continue
        fi
        seen[$trimmed]=1
        MENU_SECTION_ARGS+=("--section" "${SECTION_TITLES[$trimmed]}")
        SELECTED_SECTION_LABELS+=("${SECTION_TITLES[$trimmed]}")
    done

    if ((${#MENU_SECTION_ARGS[@]} == 0)); then
        log "⚠️  Nessuna sezione valida selezionata, verranno usate tutte."
    else
        log "📑 Sezioni selezionate: $(join_by ', ' "${SELECTED_SECTION_LABELS[@]}")"
    fi
}

select_voice_for_language() {
    local result_var="$1"
    local _lang="$2"
    local label="$3"
    local default_voice="$4"
    shift 4
    local options=("$@")
    local found_default=0
    local i
    for i in "${!options[@]}"; do
        if [[ "${options[$i]}" == "$default_voice" ]]; then
            found_default=1
            break
        fi
    done
    if ((found_default == 0)) && [[ -n "$default_voice" ]]; then
        options+=("$default_voice")
    fi
    local default_index=1
    for i in "${!options[@]}"; do
        if [[ "${options[$i]}" == "$default_voice" ]]; then
            default_index=$((i + 1))
            break
        fi
    done

    {
        printf "\n"
        printf "🔊 Voce per %s:\n" "$label"
        printf " 0) Inserisci manualmente (mantieni valore corrente)\n"
        for i in "${!options[@]}"; do
            local idx=$((i + 1))
            local marker=""
            if [[ "${options[$i]}" == "$default_voice" ]]; then
                marker="(default)"
            fi
            printf " %d) %s %s\n" "$idx" "${options[$i]}" "$marker"
        done
    } >&2
    read -rp "Scelta [$default_index]: " voice_choice
    voice_choice="${voice_choice//[[:space:]]/}"
    if [[ -z "$voice_choice" ]]; then
        printf -v "$result_var" "%s" "$default_voice"
        return
    fi
    if [[ "$voice_choice" == "0" ]]; then
        read -rp "Inserisci il nome completo della voce: " custom_voice
        if [[ -z "$custom_voice" ]]; then
            printf -v "$result_var" "%s" "$default_voice"
        else
            printf -v "$result_var" "%s" "$custom_voice"
        fi
        return
    fi
    if [[ ! "$voice_choice" =~ ^[0-9]+$ ]]; then
        printf "⚠️  Scelta non valida, uso la voce di default.\n" >&2
        printf -v "$result_var" "%s" "$default_voice"
        return
    fi
    local index=$((voice_choice - 1))
    if ((index < 0 || index >= ${#options[@]})); then
        printf "⚠️  Scelta fuori intervallo, uso la voce di default.\n" >&2
        printf -v "$result_var" "%s" "$default_voice"
        return
    fi
    printf -v "$result_var" "%s" "${options[$index]}"
}

prompt_voice_menu() {
    local languages=("${SELECTED_LANGUAGES[@]}")
    if ((${#languages[@]} == 0)); then
        languages=(it en)
    fi

    local lang label default_voice selected
    for lang in "${languages[@]}"; do
        case "$lang" in
        it)
            label="Italiano"
            default_voice="${MD_AUDIO_VOICE_IT:-$DEFAULT_VOICE_IT}"
            select_voice_for_language selected "$lang" "$label" "$default_voice" "${ITALIAN_VOICES[@]}"
            export MD_AUDIO_VOICE_IT="$selected"
            ;;
        en)
            label="Inglese"
            default_voice="${MD_AUDIO_VOICE_EN:-$DEFAULT_VOICE_EN}"
            select_voice_for_language selected "$lang" "$label" "$default_voice" "${ENGLISH_VOICES[@]}"
            export MD_AUDIO_VOICE_EN="$selected"
            ;;
        *)
            continue
            ;;
        esac
        log "🔊 Voce $label selezionata: $selected"
    done
}

run_interactive_menu() {
    if ! load_sections_for_menu; then
        log "⚠️  Menu interattivo non disponibile (impossibile leggere le sezioni)."
        return 1
    fi

    log ""
    log "🎛️  Configurazione interattiva"
    prompt_language_menu
    prompt_section_menu
    prompt_voice_menu

    local menu_args=()
    if ((${#MENU_LANGUAGE_ARGS[@]})); then
        menu_args+=("${MENU_LANGUAGE_ARGS[@]}")
    fi
    if ((${#MENU_SECTION_ARGS[@]})); then
        menu_args+=("${MENU_SECTION_ARGS[@]}")
    fi

    if ((${#menu_args[@]})); then
        EXTRA_ARGS=("${menu_args[@]}" "${EXTRA_ARGS[@]}")
    fi
    return 0
}

log "🎵 Generatore Audio per Articoli Markdown"
log "======================================"
if ((${#PIP_EXTRA_ARGS[@]})); then
    log "⚙️  Opzioni aggiuntive pip: ${AUDIO_PLAYER_PIP_FLAGS}"
fi
log ""

# Opzionale: attiva ambiente conda scelto dall'utente
if [[ -n "${AUDIO_PLAYER_CONDA_ENV:-}" ]]; then
    if command -v conda >/dev/null 2>&1; then
        eval "$(conda shell.bash hook)"
        conda activate "$AUDIO_PLAYER_CONDA_ENV"
    else
        log "⚠️  AUDIO_PLAYER_CONDA_ENV impostata ma conda non trovato. Uso Python di sistema."
    fi
fi

if ! PYTHON_BIN="$(detect_python)"; then
    log "❌ Python non trovato. Installa python3 e riprova."
    exit 1
fi

log "🐍 Interpreter: $PYTHON_BIN"

if [[ ! -f "$TARGET_FILE" ]]; then
    log "❌ File Markdown non trovato: $TARGET_FILE"
    exit 1
fi

# Assicurati che pip sia disponibile
if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    log "📦 pip non disponibile per $PYTHON_BIN. Provo ad installarlo..."
    if ! "$PYTHON_BIN" -m ensurepip --default-pip >/dev/null 2>&1; then
        log "❌ Impossibile installare pip per $PYTHON_BIN. Installa manualmente e riprova."
        exit 1
    fi
fi

ensure_module() {
    local module="$1"
    local package="${2:-$module}"
    if ! "$PYTHON_BIN" -c "import ${module}" >/dev/null 2>&1; then
        log "📦 Installazione ${package}..."
        "$PYTHON_BIN" -m pip install --upgrade "${PIP_EXTRA_ARGS[@]}" "$package"
    else
        log "✅ ${package} già installato"
    fi
}

log ""
log "🔍 Verifica dipendenze..."
ensure_module edge_tts edge-tts

RUN_MENU=0
if [[ -t 0 ]] && ((${#EXTRA_ARGS[@]} == 0)); then
    RUN_MENU=1
fi
if [[ "${AUDIO_PLAYER_FORCE_MENU:-}" == "1" ]]; then
    RUN_MENU=1
fi
if [[ "${AUDIO_PLAYER_SKIP_MENU:-}" == "1" ]] || [[ ! -t 0 ]]; then
    RUN_MENU=0
fi

if ((RUN_MENU)); then
    if ! run_interactive_menu; then
        log "⚠️  Continuo senza menu interattivo."
    fi
fi

mkdir -p "$CACHE_DIR"
export MD_AUDIO_CACHE_DIR="$CACHE_DIR"
export MD_AUDIO_KEEP_FILES=1
if [[ -n "${AUDIO_PLAYER_SSH_TARGET:-}" ]]; then
    export MD_AUDIO_SSH_TARGET="$AUDIO_PLAYER_SSH_TARGET"
    log "📡 Invio SSH attivo verso: $AUDIO_PLAYER_SSH_TARGET"
fi
if [[ -n "${AUDIO_PLAYER_SSH_OPTIONS:-}" ]]; then
    export MD_AUDIO_SSH_OPTIONS="$AUDIO_PLAYER_SSH_OPTIONS"
fi

log ""
log "💾 Gli MP3 verranno salvati in: $CACHE_DIR"
log "▶️  Avvio generazione..."

exec "$PYTHON_BIN" "$SCRIPT_DIR/audio_player.py" "$TARGET_FILE" "${EXTRA_ARGS[@]}"
