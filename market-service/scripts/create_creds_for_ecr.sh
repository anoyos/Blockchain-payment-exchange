#!/bin/sh
kubectl create secret docker-registry regcred \
  --docker-server=551678202612.dkr.ecr.us-east-2.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password) \
  --namespace=prod