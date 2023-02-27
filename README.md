# MAvis: Searchclient x

This readme describes how to use the included Python search client with the server that is contained in server.jar.

## Requirements

The server requires a Java Runtime Environment version at least 17 and has been compiled and tested with OpenJDK.

The Python searchclient has been tested with Python 3.9, but should work with versions of Python 3.7 and above.
The searchclient requires the 'psutil' package to monitor its memory usage; the package can be installed with pip:
```bash
$ pip install psutil
```
## Usage

All the following commands assume the working directory is the one this readme is located in.

You can read about the server options using the -h argument:
```bash
$ java -jar server.jar -h
```

Starting the server using the searchclient:
```bash
$ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py" -l levels/SAD1.lvl
```

(Assuming python is bound to the correct Python 3 interpreter. Otherwise try replacing "python" with "python3")

The searchclient uses the BFS search strategy by default. Use arguments -dfs, -astar, or -greedy to set
alternative search strategies (after you implement them). For instance, to use DFS search on the same level as above:
```bash
$ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py -dfs" -l levels/SAD1.lvl
```

When using either -astar or -greedy, you must also specify which heuristic to use. Use arguments -goalcount or
-advancedheuristic to select between the two heuristic in domains/hospital/heuristics.py.
For instance, to use A* search with a goal count heuristic, on the same level as above:
```bash
$ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py -astar -goalcount" -l levels/SAD1.lvl
```

## Debugging

As communication with the java server is performed over stdout, print(<something>) does not work directly, and debuggers will also fail.
To get information out, you should use
```python
print(<something>, file=sys.stderr)
```
and then you will see the information.

Note that the HospitalState has a nice string representation such that you can write
    print(state, file=sys.stderr)
and see what state your agent is stuck in.

## Settings

### Memory settings

**Unless your hardware is unable to support this, you should let the searchclient allocate at least 4GB of memory**

The searchclient monitors its own process' memory usage and terminates the search if it exceeds a given number of MiB.
To set the max memory usage to 4GB:
```bash
$ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py --max-memory 4g" -l levels/SAD1.lvl
```

Avoid setting max memory usage too high, since it will lead to your OS doing memory swapping which is terribly slow.

### Rendering on Unix systems
We experienced poor performance when rendering on some Unix systems, because hardware rendering is not turned on by default.
To enable OpenGL hardware acceleration you should use the following JVM option: -Dsun.java2d.opengl=true
```bash
$ java -Dsun.java2d.opengl=true -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py" -l levels/SAD1.lvl
```

See http://docs.oracle.com/javase/8/docs/technotes/guides/2d/flags.html for more information.
