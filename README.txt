start mongo database for macOS: sudo mongod --dbpath=/Users/Admin/data/db
(Replase Admin with your associate user-name)

To start the app,
    1. start backend, python3 app (for mac). Or python app.py (for window/linux)
    2. start frontend, npm start

If there is an accidence that a running program is suspended (Ctrl + Z) which means the background is still running. 
    The port is still in used
Solution:
    1. lsof -i :9000
    2. kill -9 <PID> 