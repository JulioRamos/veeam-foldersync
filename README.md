# syncFolder: a one-way folder synchronizer
<br>

## **Program Description**
syncfolder: an Python application that synchronizes two folders: source and replica. The program maintains a full, identical copy of the source folder in the replica folder.

The program can be executed from the command line. Alternativaly, a class SyncFolders() can be imported.

Main features:
* Synchronization in one-way: the replica folder is modified to exactly match the content of the source folder;
* The source folder is never modified;
* Synchronization should be performed periodically, using a parameter;
* File creation/copying/removal operations are logged to a specified file and to the console output;
* Folder paths, synchronization intervals, and log file paths are provided using the command line arguments.
<br>

## Usage
### Arguments
- `source` (string): Source folder path. Default value is tmp\source
- `replica` (string): Replica folder path. Default value is tmp\replica
- `logs` (string): Logs file path (required). Default value is tmp\syncfolders.log
- `interval` (int): Interval in seconds between each synchronization. Default value is 5

### Sample usages
#### Simple Execution using default parameter
```bash
python syncfolders.py
```

#### Execution defining all the parameters
```bash
python syncfolders.py --source tmp/source --replica tmp/replica --log tmp/syncfolders.log --interval 15
```


## A review of the code, highlighting potential issues and areas for improvement
<br>

### Potential Issues:

* File Handling:
_hashfile method uses a fixed buffer size (BUF_SIZE = 65536) for reading files. Consider adjusting this based on file sizes or using dynamic buffering for efficiency.
Handling of large files or memory-constrained environments might need optimization.

* Deletion Safety:
The _deleteItem method's safety check using replica_item.find('tmp//replica') could be more robust. A single path check might not prevent accidental deletions under certain scenarios. Explore alternative strategies for deletion safety.

* Synchronization Logic:
_syncFile method relies solely on file hashes for comparison. Consider incorporating additional checks like file sizes and timestamps to potentially reduce unnecessary file copying.
Handling file conflicts or changes in both source and replica folders might need further logic (e.g., version control or user intervention).

* Error Handling:
Error handling could be more comprehensive, especially for file operations (e.g., checking for permissions, disk space, potential errors during copying).
Consider logging more detailed information for easier troubleshooting.

* Logging:
Ensure log files are managed properly (e.g., rotated or archived) to avoid excessive disk usage, especially with frequent synchronization.

### Additional Considerations:
Performance: For large folders or frequent synchronization, explore performance optimization techniques like caching, parallelization, or selective synchronization.
User Feedback: Provide clear feedback to users about synchronization progress, errors, or conflicts, potentially through command-line output or visual indicators.
Testing: Implement thorough unit tests for various scenarios to ensure code reliability and catch potential issues.

### Recommendations:
Review and address the identified areas for improvement.
Implement comprehensive testing to ensure robustness.
Consider usability enhancements for user feedback and configuration.
Explore performance optimization techniques if needed.

## **Original Task**
<br>
Test Task - QA Engineer - Veeam Software

Write a program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of the source folder in the replica folder. Solve the test task by writing a program in Python.

Functional Requirements:
* Synchronization must be one-way: after the synchronization content of the replica, the folder should be modified to exactly match the content of the source folder;
* Synchronization should be performed periodically;
* File creation/copying/removal operations should be logged to a file and the console output;
* Folder paths, synchronization intervals, and log file paths should be provided using the command line arguments.

Others Requirements:
* It is undesirable to use third-party libraries that implement folder synchronization;
* It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library.