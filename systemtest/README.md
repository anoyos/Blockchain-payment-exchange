## Systemtest
Containing `service tests` and `connector tests`. 
Service tests will test the contract of REST APIs, end2end.
Connector tests will verify connector contract, end2end.

To run, you launch the `docker-compose up` which will start `mongo, redis, mysql and rabbitmq` 
together with any application that you want. The applications that is not started via compose
will need to be started manually from IDE of choice (run profiles exists for PyCharm)

#### Configure mongo permissions (done once)

Using docker-compose, mongodb runs in a replicated cluster. MongoDB needs to have users created, that applications
will use later on, to authenticate and read/write. To achieve this do:

- `docker-compose pull (see note on ECR authentication below)`
- `docker-compose up --force-recreate -d --remove-orphans`
- `<wait a sec or two for mongo to start>`
- `cd scripts`
- `./fix_mongo_permissions.sh`
  
#### Fix reverse proxy service discovery faluire

Sometimes nginx cannot proxy requests properly (seen in web-app, failing requests)

If so, try:
- `cd scripts/`
- `./fix_reverse_proxy_conf.sh`

and if you get output `... signal process started` everything should be fine and dandy.

#### Update your hosts file

In order for DNS lookup on service names when running apps in PyCharm or other IDE, 
the following entry is needed in your `/etc/hosts` file:

```shell script
127.0.0.1       mock_blockchain redis-master redis-replica rabbitmq mysql-master mysql-slave mongodb-primary mongodb-secondary mongodb-arbiter
```

#### ECR authentication

When pulling images, you need to be authenticated to bullflag ECR (container registry).
If getting errors, do log in:

```
aws ecr get-login-password --region eu-west-1 \ 
| docker login --username AWS --password-stdin 551678202612.dkr.ecr.us-east-2.amazonaws.com
```
