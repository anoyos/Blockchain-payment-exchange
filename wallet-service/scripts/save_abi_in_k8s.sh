#!/bin/sh
#kubectl create configmap contract-api \
#      --from-file=../app/app/blockchain/handlers/ethereum/abi/usdt.json \
#      --from-file=../app/app/blockchain/handlers/ethereum/abi/factory.json \
#      -n dev
#kubectl create configmap factory-api  -n dev
kubectl create configmap contract-api \
      --from-file=../app/app/blockchain/handlers/ethereum/abi/usdt.json \
      --from-file=../app/app/blockchain/handlers/ethereum/abi/factory.json \
      -n prod


