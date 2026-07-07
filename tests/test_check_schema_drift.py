#!/usr/bin/env python3
"""Tests for the engine-pinned schema-mirror drift gate.

The drift check is code, so it gets the RED->GREEN treatment: these
tests build a *local* fake engine npm tarball (the same layout
``registry.npmjs.org`` serves: ``package/schema/lesson.schema.json``)
and assert that

* the pin is read from ``schema/engine-version.txt`` and resolves to
  the registry tarball URL for exactly that version (pin mechanics),
* a byte-identical mirror passes (GREEN),
* a manipulated mirror is detected as drift (RED),
* ``--update`` rewrites the mirror from the tarball.

Everything runs offline — ``ENGINE_TARBALL`` points the script at the
local tarball, so the tests never touch the network.
"""
from __future__ import annotations

import io
import json
import sys
import tarfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_schema_drift as drift  # noqa: E402

SCHEMA_BYTES = json.dumps({"title": "Lesson", "x-schema-version": "9.9"}).encode()
MANIFEST_BYTES = json.dumps({"title": "ContentManifest"}).encode()
QUALITY_BYTES = json.dumps({"rules": {"minExercisesPerLesson": 5}}).encode()


def make_tarball(path: Path, schema_bytes: bytes = SCHEMA_BYTES) -> Path:
    """Write an npm-layout tarball with all mirrored schema members."""
    with tarfile.open(path, "w:gz") as tar:
        for member, data in (
            ("package/schema/lesson.schema.json", schema_bytes),
            ("package/schema/content-manifest.schema.json", MANIFEST_BYTES),
            ("package/schema/quality-rules.json", QUALITY_BYTES),
        ):
            info = tarfile.TarInfo(member)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return path


def write_full_mirror(mirror_root: Path) -> None:
    """Write a byte-identical mirror of every tarball member."""
    (mirror_root / "schema").mkdir(parents=True)
    (mirror_root / "schema" / "lesson.schema.json").write_bytes(SCHEMA_BYTES)
    (mirror_root / "schema" / "content-manifest.schema.json").write_bytes(
        MANIFEST_BYTES
    )
    (mirror_root / "schema" / "quality-rules.json").write_bytes(QUALITY_BYTES)


def test_pin_is_read_from_version_file(tmp_path: Path) -> None:
    (tmp_path / "engine-version.txt").write_text("0.3.1\n", encoding="utf-8")
    assert drift.read_pin(tmp_path / "engine-version.txt") == "0.3.1"


def test_pin_resolves_to_registry_tarball_url() -> None:
    url = drift.tarball_url("0.3.1")
    assert url == (
        "https://registry.npmjs.org/learn-content-engine/-/"
        "learn-content-engine-0.3.1.tgz"
    )


def test_repo_pin_matches_declared_mirror_header() -> None:
    """The committed pin file exists and carries a plain semver."""
    pin = drift.read_pin(drift.PIN_FILE)
    assert pin, "schema/engine-version.txt must not be empty"
    parts = pin.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts), pin


def test_identical_mirror_passes(tmp_path: Path) -> None:
    tarball = make_tarball(tmp_path / "engine.tgz")
    mirror_root = tmp_path / "repo"
    write_full_mirror(mirror_root)
    rc = drift.run_check(tarball_source=str(tarball), repo_root=mirror_root)
    assert rc == 0


def test_manipulated_mirror_is_drift(tmp_path: Path) -> None:
    tarball = make_tarball(tmp_path / "engine.tgz")
    mirror_root = tmp_path / "repo"
    write_full_mirror(mirror_root)
    (mirror_root / "schema" / "lesson.schema.json").write_bytes(
        SCHEMA_BYTES + b"\n// tampered"
    )
    rc = drift.run_check(tarball_source=str(tarball), repo_root=mirror_root)
    assert rc == 1


def test_tampered_quality_rules_is_drift(tmp_path: Path) -> None:
    """quality-rules.json is engine-mirrored (0.4.0+): tampering trips the gate."""
    tarball = make_tarball(tmp_path / "engine.tgz")
    mirror_root = tmp_path / "repo"
    write_full_mirror(mirror_root)
    (mirror_root / "schema" / "quality-rules.json").write_bytes(
        QUALITY_BYTES + b"\n// tampered"
    )
    rc = drift.run_check(tarball_source=str(tarball), repo_root=mirror_root)
    assert rc == 1


def test_missing_mirror_is_drift(tmp_path: Path) -> None:
    tarball = make_tarball(tmp_path / "engine.tgz")
    mirror_root = tmp_path / "repo"
    (mirror_root / "schema").mkdir(parents=True)
    rc = drift.run_check(tarball_source=str(tarball), repo_root=mirror_root)
    assert rc == 1


def test_update_rewrites_mirror_from_tarball(tmp_path: Path) -> None:
    tarball = make_tarball(tmp_path / "engine.tgz")
    mirror_root = tmp_path / "repo"
    (mirror_root / "schema").mkdir(parents=True)
    (mirror_root / "schema" / "lesson.schema.json").write_bytes(b"stale")
    (mirror_root / "schema" / "content-manifest.schema.json").write_bytes(b"stale")
    (mirror_root / "schema" / "quality-rules.json").write_bytes(b"stale")
    rc = drift.run_check(
        tarball_source=str(tarball), repo_root=mirror_root, update=True
    )
    assert rc == 0
    got = (mirror_root / "schema" / "lesson.schema.json").read_bytes()
    assert got == SCHEMA_BYTES
    got_manifest = (
        mirror_root / "schema" / "content-manifest.schema.json"
    ).read_bytes()
    assert got_manifest == MANIFEST_BYTES
    got_quality = (mirror_root / "schema" / "quality-rules.json").read_bytes()
    assert got_quality == QUALITY_BYTES


def test_repo_mirror_matches_pinned_engine_tarball_when_cached() -> None:
    """Full-repo parity against the real pinned tarball — only when a
    cached tarball is provided (CI downloads it; offline runs skip)."""
    import os

    cached = os.environ.get("ENGINE_TARBALL")
    if not cached or not Path(cached).is_file():
        pytest.skip("no cached engine tarball (offline run)")
    rc = drift.run_check(tarball_source=cached, repo_root=REPO_ROOT)
    assert rc == 0


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
