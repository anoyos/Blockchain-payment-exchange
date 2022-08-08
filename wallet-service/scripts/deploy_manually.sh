git pull

docker build \
 --build-arg SSH_PRV_KEY="$(cat ~/.ssh/id_git)" \
 -t  551678202612.dkr.ecr.us-east-2.amazonaws.com/wallet-service:latest .


aws ecr get-login-password \
    --region us-east-2 \
| docker login \
    --username AWS \
    --password-stdin 551678202612.dkr.ecr.us-east-2.amazonaws.com

docker push 551678202612.dkr.ecr.us-east-2.amazonaws.com/wallet-service:latest

helm delete wallet -n prod
helm install wallet -f ./helmchart/values.prod.yaml ./helmchart -n prod

