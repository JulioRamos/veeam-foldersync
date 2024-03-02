# veeam-foldersync
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