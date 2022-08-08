#!/bin/sh
docker run --name eth -p 8545:8545 -v ~/.geth-rinkeby:/geth \
           ethereum/client-go:stable \
           --syncmode "light" \
           --rinkeby \
           --allow-insecure-unlock \
           --http \
           --http.addr 0.0.0.0 \
           --http.api personal,eth,net,web3 \
           --http.corsdomain "*" \
           --datadir /geth
