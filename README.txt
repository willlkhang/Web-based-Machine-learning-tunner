start mongo database for macOS: sudo mongod --dbpath=/Users/Admin/data/db
(Replase Admin with your associate user-name)

docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management

To start the app,
    1. start backend, python3 app (for mac). Or python app.py (for window/linux)
    2. start frontend, npm start

If there is an accidence that a running program is suspended (Ctrl + Z) which means the background is still running. 
    The port is still in used
Solution:
    1. lsof -i :9000
    2. kill -9 <PID> 