docker build \
  -t 551678202612.dkr.ecr.us-east-2.amazonaws.com/market-service:latest \
  --build-arg SSH_PRV_KEY="$(cat ~/.ssh/id_git)" \
  .

aws ecr get-login-password \
    --region us-east-2 \
| docker login \
    --username AWS \
    --password-stdin 551678202612.dkr.ecr.us-east-2.amazonaws.com

docker push 551678202612.dkr.ecr.us-east-2.amazonaws.com/market-service:latest
helm delete markets -n dev
helm install markets ./helmchart -n dev

