Hi,
to use the syncing run the "sync.py" script. 
You need to provide foue arguments: 
1. is the delay between syncing (in seconds) 
2. is the path to the log file
2. is the path to the source folder
2. is the path to the replica folder

When first evaluating this project, my first idea was to:
1. do diff between the folder, log accordingly
2. then delete "replica" folder and duplicate the "source", renaming it to "replica". 
However that is quite inefficent, current solution is much more versatile.

Recomended use of the script "python sync.py 10 log.txt source replica"