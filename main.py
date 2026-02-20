#!/usr/bin/env python3

import select
import sys
import termios
import time
import tty
import random
import shlex
import shutil
import subprocess
import threading
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EXAM_DURATION  = 3 * 3600  # 3 heures
BASE_DIR       = Path(__file__).parent
EXAMS_DIR      = BASE_DIR / "exams"
SUBJECTS_DIR   = BASE_DIR / "subjects"
RENDER_DIR     = BASE_DIR / "render"
TRACES_DIR     = BASE_DIR / "traces"
SOLUTIONS_DIR  = BASE_DIR / "solutions"
LEVELS         = ["level1", "level2", "level3", "level4"]

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
start_time      = 0.0
current_level   = 0
current_subject = None   # Path to the active .txt file
time_expired    = False
debug_mode      = False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def format_time(seconds: float) -> str:
    s = abs(int(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def elapsed() -> float:
    return time.time() - start_time


def remaining() -> float:
    return EXAM_DURATION - elapsed()


def clear_dir(path: Path):
    for f in path.iterdir():
        if f.is_file():
            f.unlink()


def _read_line_with_timer() -> str:
    """
    Lit une ligne sur stdin en affichant un countdown live.
    Utilise le mode raw + select pour mettre à jour le timer
    chaque seconde sans bloquer la saisie.
    """
    buf: list[str] = []
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def _draw():
        t      = format_time(max(0.0, remaining()))
        prefix = f"[DEBUG | {t}]" if debug_mode else f"[{t}]"
        sys.stdout.write(f"\r\033[K{prefix} > {''.join(buf)}")
        sys.stdout.flush()

    try:
        tty.setraw(fd)
        _draw()
        while True:
            ready, _, _ = select.select([sys.stdin], [], [], 1.0)
            if not ready:
                _draw()   # mise à jour du timer
                continue
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                return "".join(buf)
            elif ch in ("\x7f", "\x08"):   # Backspace
                if buf:
                    buf.pop()
            elif ch == "\x03":             # Ctrl-C
                sys.stdout.write("\n")
                sys.stdout.flush()
                raise KeyboardInterrupt
            elif ch == "\x04":             # Ctrl-D / EOF
                sys.stdout.write("\n")
                sys.stdout.flush()
                raise EOFError
            elif ch.isprintable():
                buf.append(ch)
            _draw()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# ---------------------------------------------------------------------------
# Subject selection
# ---------------------------------------------------------------------------

def select_subject(level_name: str) -> Path | None:
    global current_subject
    level_dir = EXAMS_DIR / level_name
    subjects  = list(level_dir.glob("*.txt"))
    if not subjects:
        print(f"[ERROR] Aucun sujet disponible pour {level_name}")
        return None
    chosen = random.choice(subjects)
    clear_dir(SUBJECTS_DIR)
    shutil.copy(chosen, SUBJECTS_DIR / chosen.name)
    current_subject = chosen
    return chosen


# ---------------------------------------------------------------------------
# Subject parsing
# ---------------------------------------------------------------------------

def get_expected_files(subject_path: Path) -> list[str]:
    """Return the list of files the student must produce."""
    with open(subject_path) as f:
        for line in f:
            if line.startswith("Expected files"):
                return [x for x in line.split(":", 1)[1].strip().split() if x]
    return []


def parse_examples(subject_path: Path) -> list[tuple[str, str]]:
    """
    Extract (command, expected_output) pairs from the $> blocks.

    Handles:
      - "| cat -e"  → stripped from command, '$' at line-end → '\n'
      - other pipes → kept in command, run via shell, output compared as-is
    """
    examples = []
    with open(subject_path) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip("\n").lstrip()

        if stripped.startswith("$> ") and len(stripped) > 3:
            cmd_str   = stripped[3:]
            has_cat_e = "| cat -e" in cmd_str

            if has_cat_e:
                cmd_str = cmd_str[: cmd_str.index("| cat -e")].rstrip()

            # Collect expected-output lines until blank line or next "$>"
            expected_parts = []
            i += 1
            while i < len(lines):
                nxt = lines[i].rstrip("\n")
                if nxt.lstrip().startswith("$>") or nxt == "":
                    break
                expected_parts.append(nxt)
                i += 1

            # Build expected string
            if has_cat_e:
                expected = "".join(
                    (p[:-1] + "\n") if p.endswith("$") else (p + "\n")
                    for p in expected_parts
                )
            else:
                expected = "\n".join(expected_parts) + ("\n" if expected_parts else "")

            examples.append((cmd_str.strip(), expected))
        else:
            i += 1

    return examples


# ---------------------------------------------------------------------------
# Compilation
# ---------------------------------------------------------------------------

def compile_submission(
    expected_files: list[str], subject_name: str, as_binary: bool
) -> tuple[bool, str]:
    """
    Compile .c files from render/.
    as_binary=True  → link into an executable
    as_binary=False → compile only (-c flag, syntax check)

    Returns (success, binary_path_or_error_message).
    """
    c_files = []
    for fname in expected_files:
        fpath = RENDER_DIR / fname
        if not fpath.exists():
            return False, f"Fichier manquant : render/{fname}"
        if fname.endswith(".c"):
            c_files.append(str(fpath))

    if not c_files:
        return True, ""   # header-only

    if as_binary:
        binary = str(RENDER_DIR / subject_name)
        cmd    = ["cc", "-Wall", "-Wextra", "-Werror"] + c_files + ["-o", binary]
    else:
        binary = ""
        cmd    = ["cc", "-Wall", "-Wextra", "-Werror", "-c"] + c_files

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, f"Erreur de compilation :\n{proc.stderr.strip()}"
    return True, binary


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

def run_test(binary: str, cmd_str: str, expected: str) -> tuple[bool, str]:
    """
    Run one example command and return (passed, actual_output).

    If the command contains a pipe other than '| cat -e' (already stripped),
    run via shell with the binary path substituted; otherwise exec directly.
    """
    binary_name = Path(binary).name
    # Replace ./name or name at the start of the command with the full path
    safe_binary = binary.replace("'", "'\\''")

    if "|" in cmd_str:
        # Run via shell (e.g. "| head -N")
        shell_cmd = cmd_str.replace(f"./{binary_name}", f"'{safe_binary}'", 1)
        if shell_cmd == cmd_str:
            shell_cmd = cmd_str.replace(binary_name, f"'{safe_binary}'", 1)
        try:
            proc   = subprocess.run(shell_cmd, shell=True, capture_output=True,
                                    text=True, timeout=5)
            actual = proc.stdout
        except subprocess.TimeoutExpired:
            actual = "[TIMEOUT]\n"
    else:
        try:
            parts = shlex.split(cmd_str)
        except ValueError:
            parts = cmd_str.split()
        if parts and (parts[0] in (f"./{binary_name}", binary_name)):
            parts[0] = binary
        try:
            proc   = subprocess.run(parts, capture_output=True, text=True, timeout=5)
            actual = proc.stdout
        except subprocess.TimeoutExpired:
            actual = "[TIMEOUT]\n"
        except FileNotFoundError as e:
            actual = f"[NOT FOUND: {e}]\n"

    return actual == expected, actual


# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

def do_grademe():
    global current_level

    if current_subject is None:
        print("[ERROR] Aucun sujet sélectionné.")
        return
    subject_path = current_subject
    subject_name = subject_path.stem
    print(f"\n--- Correction : {subject_name} ---")

    # 1. Expected files
    expected_files = get_expected_files(subject_path)
    if not expected_files:
        print("[ERROR] Impossible de lire 'Expected files' dans le sujet.")
        return
    print(f"Fichiers attendus : {', '.join(expected_files)}")

    # 2. Examples → decide if we need a binary
    examples   = parse_examples(subject_path)
    as_binary  = bool(examples)

    # 3. Compile
    ok, result = compile_submission(expected_files, subject_name, as_binary)
    if not ok:
        print(result)
        trace = TRACES_DIR / f"{subject_name}_trace.txt"
        trace.write_text(result + "\n")
        print(f"Trace : traces/{trace.name}")
        return
    binary = result
    print("Compilation : OK")

    # 4. No examples → accept on compilation alone
    if not examples or not binary:
        if not binary:
            print("Exercice header-only : accepté.")
        else:
            print("Pas d'exemples exécutables : compilation OK → accepté.")
        _advance()
        return

    # 5. Run tests
    passed = 0
    total  = len(examples)
    lines  = [
        f"Sujet   : {subject_name}",
        f"Date    : {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Tests   : {total}",
        "",
    ]

    for idx, (cmd, expected) in enumerate(examples, 1):
        ok, actual = run_test(binary, cmd, expected)
        status = "OK" if ok else "KO"
        if ok:
            passed += 1
        lines += [
            f"[Test {idx}] $ {cmd}",
            f"  Statut   : {status}",
            f"  Attendu  : {repr(expected)}",
            f"  Obtenu   : {repr(actual)}",
            "",
        ]

    lines.append(f"Score : {passed}/{total}")
    trace = TRACES_DIR / f"{subject_name}_trace.txt"
    trace.write_text("\n".join(lines))

    print(f"Score : {passed}/{total} tests passés")
    print(f"Trace : traces/{trace.name}")

    if passed == total:
        _advance()
    else:
        print("Corrige ton code et retape 'grademe'.")


def _advance():
    global current_level, current_subject
    current_level += 1
    if current_level >= len(LEVELS):
        print(f"\nTous les niveaux complétés ! Temps : {format_time(elapsed())}")
        sys.exit(0)
    level_name = LEVELS[current_level]
    print(f"\nPassage au niveau {current_level + 1}…")
    subject = select_subject(level_name)
    if subject:
        print(f"[Niveau {current_level + 1}] Sujet : {subject.stem}")
        print(f"Sujet copié dans subjects/{subject.name}")
        print(f"Mets ton rendu dans render/\n")


def _show_solution():
    """Copie la solution du sujet courant dans subjects/ (debug mode only)."""
    if current_subject is None:
        return
    level_name   = LEVELS[current_level]
    subject_name = current_subject.stem
    sol_path     = SOLUTIONS_DIR / level_name / f"{subject_name}.c"
    if sol_path.exists():
        dest = SUBJECTS_DIR / sol_path.name
        shutil.copy(sol_path, dest)
        print(f"[DEBUG] Solution copiée dans subjects/{sol_path.name}")
    else:
        print(f"[DEBUG] Pas de solution trouvée pour {subject_name}"
              f" ({sol_path.relative_to(BASE_DIR)})")


# ---------------------------------------------------------------------------
# Timer watcher
# ---------------------------------------------------------------------------

def _timer_watcher():
    global time_expired
    while remaining() > 0:
        time.sleep(1)
    time_expired = True
    print(
        f"\n\n[!] Temps écoulé ! Durée totale : {format_time(elapsed())}\n"
        "Appuie sur Entrée pour quitter."
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    global start_time, debug_mode

    debug_mode = "--debug" in sys.argv

    print("=" * 60)
    print("           EXAM RANK 02 — MOCK EXAM")
    if debug_mode:
        print("               *** MODE DEBUG ***")
    print("=" * 60)
    print(f"Durée       : {format_time(EXAM_DURATION)}")
    if debug_mode:
        print("Commandes   : grademe | skip | finish | quit | status | subject")
    else:
        print("Commandes   : grademe | finish | quit | status | subject")
    print("=" * 60)

    start_time = time.time()

    # Nettoyer les dossiers de session
    for d in (RENDER_DIR, SUBJECTS_DIR, TRACES_DIR):
        clear_dir(d)

    # Background timer
    threading.Thread(target=_timer_watcher, daemon=True).start()

    # Pick first subject
    subject = select_subject(LEVELS[current_level])
    if not subject:
        sys.exit(1)
    print(f"\n[Niveau 1] Sujet : {subject.stem}")
    print(f"Sujet copié dans subjects/{subject.name}")
    print(f"Mets ton rendu dans render/\n")

    # Main loop
    while True:
        if time_expired:
            print(f"Durée totale : {format_time(elapsed())}")
            sys.exit(0)

        try:
            cmd = _read_line_with_timer().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\nInterrompu. Temps écoulé : {format_time(elapsed())}")
            sys.exit(0)

        if time_expired:
            print(f"Durée totale : {format_time(elapsed())}")
            sys.exit(0)

        if cmd in ("finish", "quit"):
            if debug_mode:
                _show_solution()
            print(f"\nExamen terminé. Temps écoulé : {format_time(elapsed())}")
            sys.exit(0)

        elif cmd == "grademe":
            do_grademe()

        elif cmd == "skip":
            if not debug_mode:
                print("Commande inconnue : 'skip' (disponible uniquement en mode debug)")
            else:
                print("[DEBUG] Exercice ignoré.")
                _show_solution()
                _advance()

        elif cmd == "status":
            print(
                f"  Niveau    : {current_level + 1}/{len(LEVELS)}\n"
                f"  Sujet     : {current_subject.stem if current_subject else '—'}\n"
                f"  Écoulé    : {format_time(elapsed())}\n"
                f"  Restant   : {format_time(max(0.0, remaining()))}"
            )

        elif cmd == "subject":
            if current_subject:
                print(f"Sujet actuel : {current_subject.stem}")
                print(f"Fichier      : subjects/{current_subject.name}")
            else:
                print("Aucun sujet sélectionné.")

        elif cmd == "":
            pass

        else:
            print(f"Commande inconnue : '{cmd}'")
            if debug_mode:
                print("Commandes : grademe | skip | finish | quit | status | subject")
            else:
                print("Commandes : grademe | finish | quit | status | subject")


if __name__ == "__main__":
    main()
