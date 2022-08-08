#!/bin/bash
kubectl delete secret regcred -n prod
kubectl create secret docker-registry regcred \
  --docker-server=551678202612.dkr.ecr.us-east-2.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password) \
  --namespace=prod

curl -X 'POST' \
  'http://127.0.0.1:80/api/v1/user/onboarding/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "pincode": "string",
  "referred_by": "string"
}'