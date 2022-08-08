
### Market Service
Provides trading engine and API

![Deploy](https://github.com/bullflag-company/market-service/actions/workflows/build.yaml/badge.svg)

### Run tests 
make sure you configure `.env.local` environment file
```
docker-compose up -d 
cd app
pytest --cov=app app/tests
```
### API Documentation 
REST API endpoints [spec](https://bullflag.com/api/v1/market/docs)

### Build locally
```bash
docker-compose build --build-arg SSH_PRV_KEY="$(cat ~/.ssh/id_git)" backend
```

### Deploy
Provided by GitHub Actions, see configuration in `.github/workflows/build.yml`

### Deploy manually in AWS EKS via Helm
```bash
helm install markets ./helmchart -n dev
```
`markets` - is **release_name** in Helm terms.

### Delete manually in AWS EKS via Helm
```bash
helm delete markets -n dev
```

### Deploy locally
```bash
docker-compose up -d
```

### Deploy configuring 

**Helm** provides template engine to configure Kubernetes resources easier.
 - In simple case, you just need to change `helmchart/values.yml` to changes deployment constant
 - In more complex case, refer to [write first helm chart](https://docs.bitnami.com/tutorials/create-your-first-helm-chart/)
or [full documentation](https://helm.sh/docs/)

MongoDB can be accessed on the following DNS name(s) and ports from within your cluster:

    bf-mongo-mongodb-0.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017
    bf-mongo-mongodb-1.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017

To get the root password run:

    export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace dev bf-mongo-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 --decode)

To connect to your database, create a MongoDB client container:

    kubectl run --namespace dev bf-mongo-mongodb-client --rm --tty -i --restart='Never' --env="MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD" --image docker.io/bitnami/mongodb:4.4.3-debian-10-r21 --command -- bash

Then, run the following command:
    mongo admin --host "bf-mongo-mongodb-0.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017,bf-mongo-mongodb-1.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017" --authenticationDatabase admin -u root -p $MONGODB_ROOT_PASSWORD


mongo admin --host "bf-mongo-mongodb-0.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017,bf-mongo-mongodb-1.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017"