import argparse
import time
import os
import shutil
import logging
import hashlib
import sys

class SyncFolders():
  def __init__(self, source: str, replica: str, logger: logging.Logger, interval: int):
    """
    Initialize the SyncFolders object with source, replica, logger, and interval.
    """
    self.source = os.path.abspath(source)
    self.replica = os.path.abspath(replica)
    self.logger = logger
    self.interval = interval

  def start_syncing(self):
    """
    Start the folder synchronization loop.
    """
    self._verify_paths()
    self._verify_source()
    self._verify_replica()
    self.logger.info("Synchronization started")
    try:
      while True:
        try:
          self.sync_once()
        except OSError as e:
          self.logger.exception(f"Synchronization failed: {e}")
        time.sleep(self.interval)
    except KeyboardInterrupt:
      self.logger.info("Synchronization stopped")

  def sync_once(self):
    """
    Perform a single synchronization pass.
    """
    self._compare_folders()

  def _verify_paths(self):
    """
    Verify source and replica are distinct and not nested inside each other.
    """
    if self.source == self.replica:
      msg = "Source and replica folders must be different"
      self.logger.warning(msg)
      raise ValueError(msg)

    try:
      common = os.path.commonpath([self.source, self.replica])
    except ValueError:
      return

    if common == self.source:
      msg = f"Replica folder cannot be inside the source folder ({self.replica})"
      self.logger.warning(msg)
      raise ValueError(msg)
    if common == self.replica:
      msg = f"Source folder cannot be inside the replica folder ({self.source})"
      self.logger.warning(msg)
      raise ValueError(msg)

  def _verify_source(self):
    """
    Verify the existence and type (directory) of the source folder.
    """
    if not os.path.exists(self.source):
      msg = f"Source folder {self.source} does not exist"
      self.logger.warning(msg)
      raise FileNotFoundError(msg)
    if not os.path.isdir(self.source):
      msg = f"{self.source} is not a folder"
      self.logger.warning(msg)
      raise NotADirectoryError(msg)

  def _verify_replica(self):
    """
    Verify the existence of the replica folder, create it if needed.
    """
    if not os.path.exists(self.replica):
      self._create_folder(self.replica)

  def _compare_folders(self):
    """
    Compare the source and replica folders, copying and syncing files.
    """
    for root, dirs, files in os.walk(self.source):
      replica_full_path = os.path.join(self.replica, os.path.relpath(root, self.source))

      for directory in dirs:
        replica_dir = os.path.join(replica_full_path, directory)
        if not os.path.exists(replica_dir):
          os.makedirs(replica_dir)
          self.logger.info(f"Directory created: {replica_dir}")

      for filename in files:
        source_file = os.path.join(root, filename)
        replica_file = os.path.join(replica_full_path, filename)

        if not os.path.exists(replica_file):
          self._copy_file(source_file, replica_file)
        else:
          self._sync_file(source_file, replica_file)

    self._remove_extra_replica_items()

  def _remove_extra_replica_items(self):
    """
    Remove files and folders present in replica but not in source.
    Uses bottom-up traversal so parent directories are deleted after their contents.
    """
    for root, dirs, files in os.walk(self.replica, topdown=False):
      source_path = os.path.join(self.source, os.path.relpath(root, self.replica))

      for filename in files:
        replica_item = os.path.join(root, filename)
        if not os.path.exists(os.path.join(source_path, filename)):
          self._delete_item(replica_item)

      for directory in dirs:
        replica_item = os.path.join(root, directory)
        if not os.path.exists(os.path.join(source_path, directory)):
          self._delete_item(replica_item)

  def _delete_item(self, replica_item: str):
    """
    Delete a file or directory inside the replica folder.
    """
    if not os.path.abspath(replica_item).startswith(self.replica + os.sep) and os.path.abspath(replica_item) != self.replica:
      msg = f"Refusing to delete item outside replica folder: {replica_item}"
      self.logger.warning(msg)
      raise ValueError(msg)

    if os.path.isfile(replica_item):
      try:
        os.remove(replica_item)
        self.logger.info(f"File removed: {replica_item}")
      except OSError as e:
        self.logger.error(f"Failed to remove file: {replica_item} ({e})")
    elif os.path.isdir(replica_item):
      try:
        shutil.rmtree(replica_item)
        self.logger.info(f"Directory removed: {replica_item}")
      except OSError as e:
        self.logger.error(f"Failed to remove directory: {replica_item} ({e})")
    else:
      msg = f"Item {replica_item} is not a folder neither a file"
      self.logger.warning(msg)
      raise FileNotFoundError(msg)

  def _create_folder(self, folder: str):
    """
    Create a folder if it doesn't exist.
    """
    if not os.path.exists(folder):
      os.makedirs(folder)
      self.logger.info(f"{folder} folder was created")

  def _copy_file(self, source_file: str, replica_file: str):
    """
    Copy a file from source to replica, creating parent directories if needed.
    """
    parent = os.path.dirname(replica_file)
    if parent and not os.path.exists(parent):
      os.makedirs(parent)

    shutil.copy2(source_file, replica_file)
    self.logger.info(f"{source_file} file copied to {replica_file}")

  def _sync_file(self, source_file: str, replica_file: str):
    """
    Compare and copy a file when size, mtime, or content differs.
    """
    if self._files_differ(source_file, replica_file):
      self._copy_file(source_file, replica_file)

  def _files_differ(self, source_file: str, replica_file: str) -> bool:
    """
    Return True when files differ by metadata or content.
    """
    source_stat = os.stat(source_file)
    replica_stat = os.stat(replica_file)

    if source_stat.st_size != replica_stat.st_size:
      return True
    if source_stat.st_mtime_ns != replica_stat.st_mtime_ns:
      return True

    return self._hashfile(source_file) != self._hashfile(replica_file)

  def _hashfile(self, file: str):
    """
    Calculate the SHA-256 hash of a file.
    """
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
      while True:
        data = f.read(BUF_SIZE)
        if not data:
          break
        sha256.update(data)

    return sha256.hexdigest()

def main():
  parser = argparse.ArgumentParser(
    prog='syncfolders',
    description='synchronizes two folders: source and replica. It maintains a full, identical copy of the source folder in the replica folder',
    epilog='sample usage: syncfolders.py --source sourceFolder --replica replicaFolder --log syncfolders.log --interval 10')

  parser.add_argument('-s', '--source', type=str, help='source folder path', default='tmp/source')
  parser.add_argument('-r', '--replica', type=str, help='replica folder path', default='tmp/replica')
  parser.add_argument('-l', '--log', type=str, help='log file path', default='tmp/syncfolders.log')
  parser.add_argument('-i', '--interval', type=int, help='synchronization interval (in seconds)', default=5)
  args = parser.parse_args()

  logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s %(message)s')
  logger = logging.getLogger()
  logger.addHandler(logging.StreamHandler(sys.stdout))

  sync = SyncFolders(args.source, args.replica, logger, args.interval)
  sync.start_syncing()

if __name__ == "__main__":
  main()
