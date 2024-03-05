import argparse
import time
import os
import shutil
import logging
import hashlib

class SyncFolders():
  def __init__(self, source: str, replica: str, logger: logging.Logger, interval: int):
    """
    Initialize the SyncFolders object with source, replica, logger, and interval.
    """
    self.source = source
    self.replica = replica
    self.logger = logger
    self.interval = interval

  def start_syncing(self):
    """
    Start the folder synchronization loop.
    """
    self._verify_source()
    self._verify_replica()
    while True:
      try:
        self._compare_folders()
      except:
        print('Exiting...')
      time.sleep(self.interval)

    
  def _verify_source(self):
    """
    Verify the existence and type (directory) of the source folder.
    """
    if not os.path.exists(self.source):
      msg = f"Source folder {self.source} does not exist"
      self.logger.warning(msg)
      raise Exception(msg)
    elif not os.path.isdir(self.source):
      msg = f"{self.source} is not a folder"
      self.logger.warning(msg)
      raise Exception(msg)

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
    # walk over the source folder
    for root, dirs, files in os.walk(self.source):
      # Construct the corresponding path in the replica folder
      replica_full_path = os.path.join(self.replica, os.path.relpath(root, self.source))

      # Create missing directories in the replica folder
      for directory in dirs:
        replica_dir = os.path.join(replica_full_path, directory)
        if not os.path.exists(replica_dir):
          os.makedirs(replica_dir)
          self.logger.info(f"Directory created: {replica_dir}")

      # Handle files in the source folder
      for filename in files:
        source_file = os.path.join(root, filename)
        replica_file = os.path.join(replica_full_path, filename)

        # Check if file exists in replica
        if not os.path.exists(replica_file):
          # Copy the file from source to replica
          self._copy_file(source_file, replica_file)
        else:
          self._sync_file(source_file, replica_file)

    # Handle files/folders present in the replica folder, but not in the source folder
    # While removing files/folders present only in the replica folder can be a risky action,
    for root, dirs, files in os.walk(self.replica):
      # Construct the corresponding path in the source folder
      source_path = os.path.join(self.source, os.path.relpath(root, self.replica))

      # Check for files/folders present in replica but not in source
      for item in (dirs + files):
        replica_item = os.path.join(root, item)
        if not os.path.exists(os.path.join(source_path, item)):
          self._delete_item(replica_item)

  def _delete_item(self, replica_item: str):
    """
    This is a safe measure for deleting items (only inside a specific path).
    """
    if os.path.isfile(replica_item):
      try:
        os.remove(replica_item)
        self.logger.info(f"File removed: {replica_item}")
      except OSError as e:
        self.logger.error(f"Failed to remove file: {replica_item} ({e})")
    elif os.path.isdir(replica_item):
      try:
          shutil.rmtree(replica_item)  # shutil.rmtree for recursive deletion
          self.logger.info(f"Directory removed: {replica_item}")
      except OSError as e:
          self.logger.error(f"Failed to remove directory: {replica_item} ({e})")
    else:
      msg = f"Item {replica_item} is not a folder neither a file"
      self.logger.warning(msg)
      raise Exception(msg)
        
  def _create_folder(self, folder: str):
    """
    Create a folder if it doesn't exist.
    """
    if not os.path.exists(folder):
      os.mkdir(folder)
      self.logger.info(f"{folder} folder was created")

  def _copy_file(self, source_file: str, replica_file: str):
      """
      Copy a file from source to replica, creating parent directories if needed.
      """
      if not os.path.exists(os.path.dirname(replica_file)):
        os.makedirs(os.path.dirname(replica_file))
      
      shutil.copy2(source_file, replica_file)
      self.logger.info(f"{source_file} file copied to {replica_file}")

  def _sync_file(self, source_file: str, replica_file: str):
      """
      Compare and potentially copy a file based on file hashes.
      TBD: add other forms of comparison like file size, timestamps and content
      """
      if (self._hashfile(source_file) != self._hashfile(replica_file)):
        self._copy_file(source_file, replica_file)

  def _hashfile(self, file: str):
      """
      Calculate the SHA-256 hash of a file.
      source: https://www.geeksforgeeks.org/hashlib-module-in-python/
      """      
      # A arbitrary (but fixed) buffer size
      # 65536 = 65536 bytes = 64 kilobytes
      BUF_SIZE = 65536
  
      # Initializing the sha256() method
      sha256 = hashlib.sha256()
  
      with open(file, 'rb') as f:
        while True:
          # reading data = BUF_SIZE from the 
          # file and saving it in a variable
          data = f.read(BUF_SIZE)

          # True if eof = 1
          if not data:
              break

          # Passing that data to that sh256 hash 
          # function (updating the function with that data)
          sha256.update(data)
  
      # sha256.hexdigest() hashes all the input data passed to the sha256() via sha256.update()
      # Acts as a finalize method, after which all the input data gets hashed hexdigest() hashes the data, and returns the output in hexadecimal format
      return sha256.hexdigest()

def main():
  # Instantiate the parser
  parser = argparse.ArgumentParser(
    prog='syncfolders',
    description='synchronizes two folders: source and replica. It maintains a full, identical copy of the source folder in the replica folder',
    epilog='sample usage: syncfolders.py --source sourceFolder --replica replicaFolder --interval 10 --log syncfolders.log')

  # Collecting the 4 arguments - source folde, replica folder, log path and synchronization interval in seconds. If not defined, use default values
  # Out of Scope: handling possible errors when parsing the arguments
  parser.add_argument('-s', '--source', type=str, help='source folder path', default = 'tmp/source')
  parser.add_argument('-r', '--replica', type=str, help='replica folder path', default = 'tmp/replica')
  parser.add_argument('-l', '--log', type=str, help='log file path', default = 'tmp/syncfolders.log')
  parser.add_argument('-i', '--interval', type=int, help='synchronization interval (in seconds)', default = 5)
  args = parser.parse_args()
    
  # Setting up a logger for handling our events
  logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s %(message)s')
  logger = logging.getLogger()

  # Will call the method that starts the monitoring of bothe folder, source and replica
  a = SyncFolders(args.source, args.replica, logger, args.interval)
  a.start_syncing()  

if __name__ == "__main__":
  main()