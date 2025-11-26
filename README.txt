start mongo database for macOS: sudo mongod --dbpath=/Users/Admin/data/db
(Replase Admin with your associate user-name)

If there is an accidence that a running program is suspended (Ctrl + Z) which means the background is still running. 
    The port is still in used
Solution:
    1. lsof -i :9000
    2. kill -9 <PID> 