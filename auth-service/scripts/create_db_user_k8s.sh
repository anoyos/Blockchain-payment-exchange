#!/bin/sh

POD_NAME="bf-mongo-mongodb-0"
NAMESPACE="dev"
MONGODB_ROOT_USER="root"
MONGODB_DB="auth"

MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace dev mongo-creds -o jsonpath="{.data.mongodb-root-password}" | base64 --decode)
MONGODB_PASSWORD=$(kubectl get secret --namespace dev mongo-creds -o jsonpath="{.data.mongodb-password}" | base64 --decode)
MONGODB_USER=$(kubectl get secret --namespace dev mongo-creds -o jsonpath="{.data.mongodb-user}" | base64 --decode)

CMD="db.getSiblingDB('$MONGODB_DB').createUser({user: '$MONGODB_USER', pwd: '$MONGODB_PASSWORD', roles: ['readWrite']})"

echo $CMD
kubectl --namespace $NAMESPACE exec $POD_NAME -- mongo admin -u $MONGODB_ROOT_USER -p $MONGODB_ROOT_PASSWORD --eval "$CMD"


#mongo mongodb://bf-mongo-mongodb-0.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017,bf-mongo-mongodb-1.bf-mongo-mongodb-headless.dev.svc.cluster.local:27017/auth?authSource=auth --username mongodb-user