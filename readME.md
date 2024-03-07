https://github.com/CodeAcademy-Online/python-new-material-level2/wiki/Mongo-DB---lesson-1:-Introduction
https://www.youtube.com/watch?v=c2M-rlkkT5o
https://www.mongodb.com/docs/mongodb-shell/reference/data-types/#numeric-types

pažiūrėti docker failus galima dadėti -a viskam

docker ps

peržiūrėti images
docker images

ištrinti viską
docker system prune -a

paleisti 
docker run -d -p 27017:27017 --name test-mongo mongo:latest


peržiūrėti docker parametrus
docker inspect test-mongo 

pervardinti docker
docker rename [old name] [new name]



