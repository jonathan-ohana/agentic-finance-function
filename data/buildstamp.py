"""
Which version of the code produced this folder?

A delivered instance carries a mirror of the generator beside the data, and until now
nothing said whether that mirror is the code that actually built it. It usually is. The
case that matters is the one where it is not: a fix lands in the generator and the
instance is deliberately left alone - because rebuilding would regenerate a signed period -
and from that moment the folder and the code beside it describe different worlds with
nothing recording the gap.

That is the same defect this instance has now produced five times in other places: two
artifacts describing the same thing, and nothing putting them side by side. The stamp is
the side-by-side. It is written at build time, it is not editable after the fact without
saying so, and `validate.py` reads it.

It deliberately does NOT try to decide whether a difference matters. A hash cannot know
that. It reports which files moved and leaves the judgment where judgment belongs.
"""
import os, json, hashlib, datetime as dt

STAMP = os.path.join("00-company", "build-stamp.json")


def _sources(gen_dir):
    """Every generator source, by name and content hash. Sorted, so the digest is stable."""
    out = {}
    for f in sorted(os.listdir(gen_dir)):
        if not f.endswith(".py"):
            continue
        with open(os.path.join(gen_dir, f), "rb") as fh:
            out[f] = hashlib.sha256(fh.read()).hexdigest()
    return out


def digest(files):
    h = hashlib.sha256()
    for name in sorted(files):
        h.update(name.encode() + b"\0" + files[name].encode() + b"\n")
    return h.hexdigest()


def write(out_dir, gen_dir, built_at=None):
    """Called at the end of the build, after the generator mirror is laid down."""
    files = _sources(gen_dir)
    stamp = {
        "built_at": (built_at or dt.datetime.now()).isoformat(timespec="seconds"),
        "generator_files": len(files),
        "generator_sha256": digest(files),
        "files": files,
        "note": ("The generator that produced this folder. validate.py compares this to the "
                 "mirror in _generator/. A mismatch is not automatically wrong - the code may "
                 "have moved on deliberately - but it must never be silent."),
    }
    path = os.path.join(out_dir, STAMP)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stamp, f, indent=2)
        f.write("\n")
    return stamp


def compare(out_dir):
    """(state, detail) where state is 'match', 'drift', or 'absent'."""
    path = os.path.join(out_dir, STAMP)
    if not os.path.exists(path):
        return "absent", "no build stamp: this folder predates build stamping, so the code that produced it cannot be identified"
    stamp = json.load(open(path, encoding="utf-8"))
    gen = os.path.join(out_dir, "_generator")
    if not os.path.isdir(gen):
        return "drift", "the generator mirror is missing entirely"
    now = _sources(gen)
    if digest(now) == stamp.get("generator_sha256"):
        return "match", f"built {stamp.get('built_at')} from {len(now)} sources"
    was = stamp.get("files", {})
    changed = sorted(set(was) ^ set(now)) + sorted(f for f in set(was) & set(now) if was[f] != now[f])
    return "drift", (f"built {stamp.get('built_at')}, and the generator beside it has moved since: "
                     + ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else ""))
