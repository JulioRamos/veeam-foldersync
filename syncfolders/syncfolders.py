import argparse

'''
Write a program that synchronizes two folders: source and replica. The program should maintain a full,
identical copy of the source folder in the replica folder. Solve the test task by writing a program in Python.

Functional Requirements:
* Synchronization must be one-way: after the synchronization content of the replica,
    the folder should be modified to exactly match the content of the source folder;
* Synchronization should be performed periodically;
* File creation/copying/removal operations should be logged to a file and the console output;
* Folder paths, synchronization intervals, and log file paths should be provided using the command line arguments.

Others Requirements:
* It is undesirable to use third-party libraries that implement folder synchronization;
* It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example,
    there is no point in implementing yet another function that calculates MD5 if you need it for the tas.
    It is perfectly acceptable to use a third-party (or built-in) library.
'''

# python -m syncfolders.py --source sourceFolder --replica replicaFolder --interval 3 --logs syncfolders.log

def main():
  # Instantiate the parser
  parser = argparse.ArgumentParser(
    prog='syncfolders',
    description='Synchronizes two folders: source and replica. It maintains a full, identical copy of the source folder in the replica folder',
    epilog='Sample: syncfolders.py --source sourceFolder --replica replicaFolder --interval 10 --log syncfolders.log')

  # collecting the 4 arguments - source folde, replica folder, log path and synchronization interval in seconds. If not defined, use default values
  parser.add_argument('-s', '--source', type=str, help='source folder path', default = 'source')
  parser.add_argument('-r', '--replica', type=str, help='replica folder path', default = 'replica')
  parser.add_argument('-l', '--log', type=str, help='log file path', default = 'syncfolders.log')
  parser.add_argument('-i', '--interval', type=int, help='synchronization interval (in seconds)', default = '5')
  args = parser.parse_args()
    
  print (args.source, args.replica, args.interval, args.log)

  start_syncing()


def start_syncing():
  None

if __name__ == "__main__":
  main()