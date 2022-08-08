FROM 101351886674.dkr.ecr.eu-west-1.amazonaws.com/python-service-base:latest

ARG IMAGE_TAG
ENV IMAGE_TAG=$IMAGE_TAG

ARG CODEARTIFACT_TOKEN
WORKDIR /bullflag/app

COPY requirements.txt /bullflag/app/requirements.txt
COPY scripts/create_virtual_env.sh /bullflag/app/create_virtual_env.sh

RUN ./create_virtual_env.sh $CODEARTIFACT_TOKEN

COPY src /bullflag/app
COPY deploy/boot.sh.kube /bullflag/app/boot.sh

RUN mkdir -p /bullflag/app/logs
RUN chown bullflag /bullflag/app/logs -R
RUN chmod +x /bullflag/app/boot.sh

EXPOSE 5000 6000

USER bullflag
CMD ["./boot.sh"]
