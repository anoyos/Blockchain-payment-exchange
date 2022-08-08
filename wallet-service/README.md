## Wallet Service
Provides available markers and tickers on it, in `/api/v1/currency/` endpoint


### NOTE: 
**Some of APIs call are synchronous because it uses `bitcoinlib` which can't be asynchronous**


### Run tests

```bash
sh ./scripts/test.sh
```

**note**: 
 - For unit test purpose we use dump of test database stored in `app/app/tests/.db_data` because `mongomock` library 
   doesn't support async expression.
 - When some data has been updated in test database - update dump
   ```bash
      sh -x ./scripts/update_db_dump.sh
   ```
### Build locally

get app from github (it needs to load common configs during builds)
```
echo "place_token_here" > .github_token
```

```bash
docker-compose build --build-arg SSH_PRV_KEY="$(cat ~/.ssh/id_git)"  --build-arg GITHUB_TOKEN="$(cat .github_token)" backend
```

### Deploy manually in AWS EKS
```bash
helm install wallets ./helmchart -n dev
```

### Delete manually in AWS EKS
```bash
helm -n dev delete wallets
```

### Deploy locally
```bash
docker-compose up -d
```


### Test ETH node PRC
(optional) run pod with curl

```bash
kubectl run curl-test --image=radial/busyboxplus:curl - i --tty --rm  -n dev
```

execute command
```bash

curl -X POST http://wallet-service-eth.dev.svc.cluster.local:8545 -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":64}'
```

### Private dependency disclaimer
1. This service has [api_contrib](https://github.com/bullflag-company/api_contrib) package as dependency.<br>
   It hosted in github company's repository, which is private, so you **need provide ssh key during build** <br>
   as for load these sources.
2. On deploy step, private key saved as one of the organization's secrets.
3. Organization's secret link with razzor58@gmail.com account. So it should be replaced, if access revoked


### 