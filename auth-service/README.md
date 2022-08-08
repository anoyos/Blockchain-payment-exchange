## Auth Service
Provides API for user account operations in `/api/v1/auth/` endpoint

### Build locally
```bash
docker-compose build --build-arg SSH_PRV_KEY="$(cat ~/.ssh/id_git)" backend
```

### Deploy
Provided by GitHub Actions, see configuration in `.github/workflows/build.yml`

### Deploy manually in AWS EKS via Helm
```bash
helm install auth ./helmchart -n dev
```
`trollbox` - is **release_name** in Helm terms.

### Delete manually in AWS EKS via Helm
```bash
helm delete auth -n dev
```

### Deploy locally
```bash
docker-compose up -d
```

### Deploy configuring 

**Helm** provides template engine to configure Kubernetes resources easier.
 - In simple case, you just need to change `helmchart/values.yml` to changes deployment constant
 - In more complex case, refer to [write first helm chart](https://docs.bitnami.com/tutorials/create-your-first-helm-chart/)
or [full documentation](https://helm.sh/docs/)



### Private dependency disclaimer
1. This service has [api_contrib](https://github.com/bullflag-company/api_contrib) package as dependency.<br>
   It hosted in github company's repository, which is private, so you **need provide ssh key during build** <br>
   as for load these sources.
2. On deploy step, private key saved as one of the organization's secrets.
3. Organization's secret link with razzor58@gmail.com account. So it should be replaced, if access revoked
