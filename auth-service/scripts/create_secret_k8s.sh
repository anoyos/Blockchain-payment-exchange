#!/bin/sh

kubectl create secret generic twilio-creds -n dev \
  --from-literal=sid='sid_from_console' \
  --from-literal=token='token_from_twillo_console'

