# syncfolders

One-way folder synchronizer: keeps a **replica** folder identical to a **source** folder. The source is never modified.

## Setup

```bash
pip install -r requirements.txt
```

Runtime uses Python standard library only. `pytest` is listed in `requirements.txt` for running tests.

## Usage

Run from the `syncfolders` directory:

```bash
cd syncfolders
python syncfolders.py
```

With custom paths:

```bash
python syncfolders.py --source tmp/source --replica tmp/replica --log tmp/syncfolders.log --interval 15
```

Stop with `Ctrl+C`.

### Arguments

| Argument | Short | Default | Description |
|----------|-------|---------|-------------|
| `--source` | `-s` | `tmp/source` | Source folder |
| `--replica` | `-r` | `tmp/replica` | Replica folder |
| `--log` | `-l` | `tmp/syncfolders.log` | Log file path |
| `--interval` | `-i` | `5` | Seconds between sync passes |

Create/copy/remove operations are logged to the log file and the console.

### Use as a library

```python
import logging
import syncfolders  # run with syncfolders/ on PYTHONPATH, or from that directory

logger = logging.getLogger("sync")
logger.addHandler(logging.StreamHandler())
sync = syncfolders.SyncFolders("tmp/source", "tmp/replica", logger, interval=5)
sync.start_syncing()   # periodic loop
# or
sync.sync_once()       # single pass
```

## Tests

From the project root:

```bash
pytest tests/test.py -v
```

Tests cover copying from source to replica, removing extra files, and removing extra directories.

## Original task (Veeam QA test)

- One-way sync: replica matches source; source is not changed.
- Periodic synchronization.
- Log file operations to file and console.
- Configure paths, interval, and log via command-line arguments.
- Do not use third-party folder-sync libraries (stdlib + general utilities such as `hashlib` are fine).

For code review notes and future improvements, see [CODE_REVIEW.md](CODE_REVIEW.md).
