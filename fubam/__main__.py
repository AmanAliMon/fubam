from pathlib import Path
import shutil
import argparse
import json
from .fubam import Fubam

# ------------------ CONFIG ------------------
DEFAULT_OUTPUT_DIR = Path("./")
# -------------------------------------------

def transform_filename(name: str) -> str:
    return name.lower().replace("-", "_").replace(" ", "_")

def load_resources(ref):
    if not ref:
        return {}

    ref_path = Path(ref)

    if not ref_path.exists():
        raise SystemExit(f"[fubam] --ref file not found: {ref_path}")

    try:
        return json.loads(ref_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"[fubam] invalid JSON in {ref_path}: {e}")

def process_files(
    files,
    recursive=False,
    output_dir=DEFAULT_OUTPUT_DIR,
    ext=None,
    resources={}
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 🔑 Detect template root
    first = Path(files[0])
    template_root = first if first.is_dir() else first.parent

    compiler = Fubam(template_dir=str(template_root.resolve()))

    for src in files:
        src_path = Path(src)

        if src_path.is_dir() and recursive:
            pmx_files = list(src_path.rglob("*.pmx"))
        elif src_path.is_file():
            pmx_files = [src_path] if src_path.suffix == ".pmx" else []
        else:
            continue

        # ---------- PMX → HTML ----------
        for pmx_file in pmx_files:
            rel = pmx_file.relative_to(template_root)
            new_name = transform_filename(pmx_file.stem)

            out_file = output_dir / rel.parent / new_name
            out_file = out_file.with_suffix(f".{ext.lstrip('.')}" if ext else "")

            out_file.parent.mkdir(parents=True, exist_ok=True)

            html = compiler.renderTemplate(
                str(rel.with_suffix("")),
                resources=resources
            )

            out_file.write_text(html, encoding="utf-8")
            print(f"Built: {out_file}")

# ------------------ CLI ------------------
def main():
    parser = argparse.ArgumentParser(prog="fubam")

    parser.add_argument(
        "files", nargs="+",
        help="Files or directories to process"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process directories recursively"
    )

    parser.add_argument(
        "--ext",
        help="Output extension (e.g. html)"
    )

    parser.add_argument(
        "--ref",
        help="JSON file for template resources"
    )

    parser.add_argument(
        "-o", "--out",
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory"
    )

    args = parser.parse_args()
    resources = load_resources(args.ref)

    process_files(
        files=args.files,
        recursive=args.recursive,
        output_dir=args.out,
        ext=args.ext,
        resources=resources
    )

if __name__ == "__main__":
    main()
