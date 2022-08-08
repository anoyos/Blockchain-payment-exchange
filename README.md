# Blockchain-payment-exchange

make sure you clone 6 repos in same folder:

admin-service  
auth-service   
balance-service   
market-service  
systemtest  
wallet-service 
api-contrib

go to systemtest and change to branch "local"

run command to set the variable

`export ID_RSA=$(cat ~/.ssh/id_rsa)` , with that file is your private key, public key should be added to github

then you can run 

`docker-compose build --no-cache` (Build image)
`docker-compose up -d` (bring up the services)

if you run:

`docker ps -a` 

you will see 4 docker container crashed, that the thing we are fixing

you can use

`docker logs <container-name>` 

to see why it crash
then you update the api-contrib, push to github, and re-run command to check again

`docker-compose build --no-cache` (Build image)
`docker-compose up -d` (bring up the services)
