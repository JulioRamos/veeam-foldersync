import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "syncfolders"))
import syncfolders


def _make_sync(source_folder, replica_folder, log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s %(message)s")
    logger = logging.getLogger(f"sync-{source_folder}")
    return syncfolders.SyncFolders(str(source_folder), str(replica_folder), logger, interval=1)


def test_one_way_sync(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "sync.log"

    source_folder.mkdir()
    (source_folder / "file.txt").write_text("Source content")

    sync = _make_sync(source_folder, replica_folder, log_file)
    sync._verify_source()
    sync._verify_replica()
    sync.sync_once()

    assert (replica_folder / "file.txt").read_text() == "Source content"


def test_removes_extra_replica_files(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "sync.log"

    source_folder.mkdir()
    replica_folder.mkdir()
    (source_folder / "keep.txt").write_text("keep")
    (replica_folder / "orphan.txt").write_text("remove me")

    sync = _make_sync(source_folder, replica_folder, log_file)
    sync._verify_source()
    sync._verify_replica()
    sync.sync_once()

    assert (replica_folder / "keep.txt").exists()
    assert not (replica_folder / "orphan.txt").exists()


def test_removes_extra_replica_directory(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "sync.log"

    source_folder.mkdir()
    replica_folder.mkdir()
    orphan_dir = replica_folder / "orphan"
    orphan_dir.mkdir()
    (orphan_dir / "nested.txt").write_text("remove me")

    sync = _make_sync(source_folder, replica_folder, log_file)
    sync._verify_source()
    sync._verify_replica()
    sync.sync_once()

    assert not orphan_dir.exists()
