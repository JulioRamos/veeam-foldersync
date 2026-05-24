# Code review and improvement notes

## Addressed in recent changes

- **Replica cleanup during `os.walk`:** Extra items are removed bottom-up so deleted directories are not walked again.
- **Error handling:** Sync errors are logged and the loop continues; `Ctrl+C` stops cleanly.
- **Deletion safety:** Paths are validated so source/replica cannot be the same or nested; deletes are refused outside the replica tree.
- **File comparison:** Size and modification time are checked before SHA-256 hashing.
- **Replica creation:** Nested replica paths are created with `os.makedirs`.
- **Tests:** `tests/test.py` covers copy, orphan file removal, and orphan directory removal.

## Remaining considerations

### Performance

- Large folders still hash files when size and mtime match but content may differ (rare edge case).
- Very large trees or short intervals may benefit from caching hashes or parallel copies.

### Error handling

- Disk full, permission denied, and locked files are logged on failure but do not stop the periodic loop.
- No retry/backoff for transient I/O errors.

### Logging

- Log files grow without rotation; long-running syncs may need log rotation or archival.

### Edge cases

- Symlinks, special files, and read-only attributes are not handled explicitly.
- Cross-platform path casing (e.g. Windows) is not normalized beyond `abspath`.

### Usability

- No progress output for large syncs beyond per-operation log lines.
- No dry-run mode to preview changes before deleting replica-only items.

## Recommendations

- Add more tests (modified files, nested directories, invalid paths).
- Add log rotation for production use.
- Document expected behavior for symlinks and hidden files if relevant to your environment.
