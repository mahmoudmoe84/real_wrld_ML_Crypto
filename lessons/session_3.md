# Session 3


## 1. Goals

- [x] Build the `candles` service.
- [x] Deploy the `candles` service to the `dev` cluster.
- [x] Deploy the `trades` service to the `prod` cluster
- [x] Deploy the `candles` service to the `prod` cluster
    - [x] build and push the image to the github container registry
    - [x] deployments/prod/candles/candles.yaml
    - [x] set KUBECONFIG to point to the `prod` cluster
    - [x] trigger the deployment manually with `kubectl apply -f deployments/prod/candles/candles.yaml`

- [ ] Build boilerlate for the `technical-indicators` service.
    - [ ] Install talib C library inside the devcontainer.

    
## Nuggets of wisdom

```sh
kubectl set image deployment/trades -n rwml trades=ghcr.io/real-world-ml/trades:0.1.5-beta.@sha256:1c4933acedfa3611903a1f7e2e6313e97ba7df1b84f4742f9e7368fb62cafd2e
```

- How to copy a file from one branch (for example `dev`) to another branch (for example `main`):
    ```sh
    git checkout dev -- deployments/prod/trades/trades.yaml
    ```
## Further materials

- A bit of jargon: Kafka topics, Kafka partitions, Kafka replication factor, Message keys.

## Challenges

- Instead of having one Dockerfile for each service, write a single Dockerfile that builds both services, by using build arguments.

- Improve this build command with proper labeling (open containers labeling scheme)
    ```sh
    docker buildx build --push --platform linux/amd64 -t ghcr.io/real-world-ml/${service}:0.1.5-beta.${BUILD_DATE} -f docker/${service}.Dockerfile .
    ```
- How to use a Kafka Registry to make sure messages have the correct format.

    Today we saw how an outdated version of the `trades` service was deployed to the `prod` cluster, producing
    messages with a different format expected by the `candles` service.

    To avoid this type of data issues, we can use a Kafka registry to validate the messages.




