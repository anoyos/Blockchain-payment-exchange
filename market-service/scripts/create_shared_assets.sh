#!/bin/sh
kubectl delete -n prod configmap asset-configmap
kubectl create configmap asset-configmap --from-file=../app/app/assets.json -n prod