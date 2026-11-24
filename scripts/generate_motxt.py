"""Run the same Java generator used by the installed MoTxT VS Code extension."""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, help='Path to the MoTxT extension bin/motxt.jar')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    jar = args.jar
    if jar is None:
        candidates = list((Path.home() / '.vscode/extensions').glob('csui-rse-lab.motxt-*/bin/motxt.jar'))
        if len(candidates) != 1:
            parser.error('Specify --jar: expected exactly one installed MoTxT generator.')
        jar = candidates[0]
    jar = jar.resolve()
    if not jar.is_file():
        parser.error(f'Generator not found: {jar}')
    # Keep regeneration away from manually corrected application files.
    target = root / 'generated' / 'diagram' / 'Django'
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        'java', '-cp', str(jar), 'id.ac.ui.cs.ppl.motxt.main.Generate',
        str(root / 'diagrams/KebabDEL.uml'), str(target), 'Django',
    ], check=True)
    generated = target / 'KebabDEL/main/models.py'
    if not generated.is_file():
        raise SystemExit('Generator exited without creating the expected models.py.')
    evidence = root / 'docs' / 'evidence'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'motxt-models.py.txt').write_bytes(generated.read_bytes())
    check = subprocess.run(
        [sys.executable, str(target / 'KebabDEL/manage.py'), 'check'],
        text=True, capture_output=True,
    )
    log = f'Raw generated Django check exit code: {check.returncode}\n' + check.stdout + check.stderr
    (evidence / 'motxt-check.txt').write_text(log.replace(str(root), '$PROJECT'))
    print(f'Raw generated Django check exit code: {check.returncode}')
    print('See docs/evidence/ for raw output; manual corrections are in the main project.')
    print(f'Output: {target / "KebabDEL"}')


if __name__ == '__main__':
    main()
