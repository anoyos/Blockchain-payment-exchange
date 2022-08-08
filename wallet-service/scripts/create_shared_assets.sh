#!/bin/sh
kubectl delete -n prod configmap asset-configmap
kubectl create configmap asset-configmap -n prod --from-file=../app/conf/assets.json