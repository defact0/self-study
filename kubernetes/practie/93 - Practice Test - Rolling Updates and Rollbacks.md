Practice Test - Rolling Updates and Rollbacks

- https://uklabs.kodekloud.com/topic/practice-test-rolling-updates-and-rollbacks-2/

---

Q1. We have deployed a simple web application. Inspect the PODs and the Services

- Wait for the application to fully deploy and view the application using the link called `Webapp Portal` above your terminal.

```shell
root@controlplane:~# kubectl get pod
NAME                        READY   STATUS    RESTARTS   AGE
frontend-7776cb7d57-hmjdn   1/1     Running   0          2m25s
frontend-7776cb7d57-mhlhh   1/1     Running   0          2m25s
frontend-7776cb7d57-s6bf8   1/1     Running   0          2m25s
frontend-7776cb7d57-w8b2j   1/1     Running   0          2m25s
root@controlplane:~# kubectl get deployments.apps 
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
frontend   4/4     4            4           2m43s
root@controlplane:~# kubectl get replicasets.apps 
NAME                  DESIRED   CURRENT   READY   AGE
frontend-7776cb7d57   4         4         4       2m59s
```

- `webapp portal` 버튼을 클릭하여 웹페이지 출력 확인

---

Q2. What is the current color of the web application?

- Access the Webapp Portal.
- `blue`

---

Q3. Run the script named `curl-test.sh` to send multiple requests to test the web application. Take a note of the output.

- Execute the script at `/root/curl-test.sh`.

```shell
root@controlplane:~# ls
curl-pod.yaml  curl-test.sh

root@controlplane:~# sh curl-test.sh 
Hello, Application Version: v1 ; Color: blue OK
```

curl-test.sh 내용

```shell
for i in {1..35}; do
   kubectl exec --namespace=kube-public curl -- sh -c 'test=`wget -qO- -T 2  http://webapp-service.default.svc.cluster.local:8080/info 2>&1` && echo "$test OK" || echo "Failed"';
   echo ""
done
```

---

Q4. Inspect the deployment and identify the number of PODs deployed by it

```shell
root@controlplane:~# kubectl get deployments.apps 
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
frontend   4/4     4            4           2m43s
```

- 4

---

Q5. What container image is used to deploy the applications?

```shell
root@controlplane:~# kubectl describe deployment | grep -i image
    Image:        kodekloud/webapp-color:v1
```

- `kodekloud/webapp-color:v1`

---

Q6. Inspect the deployment and identify the current strategy

```shell
root@controlplane:~# kubectl describe deployments.apps | grep -i StrategyType 
StrategyType:           RollingUpdate
```

- `RollingUpdate`

---

Q7. If you were to upgrade the application now what would happen?

- `PODs are upgraded few at a time`

---

Q8. Let us try that. Upgrade the application by setting the image on the deployment to `kodekloud/webapp-color:v2`

- Do not delete and re-create the deployment. Only set the new image name for the existing deployment.
  - Deployment Name: frontend
  - Deployment Image: kodekloud/webapp-color:v2

```shell
root@controlplane:~# kubectl edit deployments.apps frontend
#    spec:
#      containers:
#      - image: kodekloud/webapp-color:v1
      - image: kodekloud/webapp-color:v2

root@controlplane:~# kubectl get pods
NAME                        READY   STATUS              RESTARTS   AGE
frontend-7776cb7d57-hmjdn   1/1     Running             0          13m
frontend-7776cb7d57-mhlhh   1/1     Running             0          13m
frontend-7776cb7d57-s6bf8   1/1     Running             0          13m
frontend-7776cb7d57-w8b2j   1/1     Terminating         0          13m
frontend-7c7fcfc8cb-kkhz4   0/1     ContainerCreating   0          7s
frontend-7c7fcfc8cb-mhfkk   0/1     ContainerCreating   0          7s

root@controlplane:~# sh curl-test.sh 
Hello, Application Version: v2 ; Color: green OK
```

- 원래 curl-test.sh의 결과가 `Hello, Application Version: v1 ; Color: blue OK`이었는데,
  지금은 `Hello, Application Version: v2 ; Color: green OK` 으로 변경된 것을 확인 할 수 있다.

---

Q9. Run the script `curl-test.sh` again. Notice the requests now hit both the old and newer versions. However none of them fail.

- Execute the script at `/root/curl-test.sh`.

```shell
root@controlplane:~# /root/curl-test.sh
Hello, Application Version: v2 ; Color: green OK

Hello, Application Version: v1 ; Color: blue OK

..반복
```



---

Q10. Up to how many PODs can be down for upgrade at a time

- Consider the current strategy settings and number of PODs - 4

```shell
root@controlplane:~# kubectl describe deployments.apps frontend 
Name:                   frontend
Namespace:              default
CreationTimestamp:      Mon, 23 Aug 2021 02:19:57 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 2
Selector:               name=webapp
Replicas:               4 desired | 4 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        20
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  name=webapp
  Containers:
   simple-webapp:
    Image:        kodekloud/webapp-color:v2
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   frontend-7c7fcfc8cb (4/4 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  19m    deployment-controller  Scaled up replica set frontend-7776cb7d57 to 4
  Normal  ScalingReplicaSet  6m12s  deployment-controller  Scaled up replica set frontend-7c7fcfc8cb to 1
  Normal  ScalingReplicaSet  6m12s  deployment-controller  Scaled down replica set frontend-7776cb7d57 to 3
  Normal  ScalingReplicaSet  6m12s  deployment-controller  Scaled up replica set frontend-7c7fcfc8cb to 2
  Normal  ScalingReplicaSet  5m44s  deployment-controller  Scaled down replica set frontend-7776cb7d57 to 1
  Normal  ScalingReplicaSet  5m44s  deployment-controller  Scaled up replica set frontend-7c7fcfc8cb to 4
  Normal  ScalingReplicaSet  5m17s  deployment-controller  Scaled down replica set frontend-7776cb7d57 to 0
root@controlplane:~# 
```

- RollingUpdateStrategy:  25% max unavailable, 25% max surge
  - 정답은 1

---

Q11. Change the deployment strategy to `Recreate`

- Do not delete and re-create the deployment. Only update the strategy type for the existing deployment.
  - Deployment Name: frontend
  - Deployment Image: kodekloud/webapp-color:v2
  - Strategy: Recreate

```shell
root@controlplane:~# kubectl edit deployments.apps frontend
# strategy.type 을 RollingUpdate에서 Recreate 으로 수정한다.
# strategy.rollingUpdate 부분은 삭제한다.
deployment.apps/frontend edited

root@controlplane:~# kubectl describe deployments.apps frontend 
Name:               frontend
...
StrategyType:       Recreate
```

---

Q12. Upgrade the application by setting the image on the deployment to `kodekloud/webapp-color:v3`

- Do not delete and re-create the deployment. Only set the new image name for the existing deployment.
  - Deployment Name: frontend
  - Deployment Image: kodekloud/webapp-color:v3

```shell
root@controlplane:~# kubectl edit deployments.apps frontend
# kodekloud/webapp-color:v2 -> kodekloud/webapp-color:v3 으로 수정
deployment.apps/frontend edited 

# 수정사항 확인
root@controlplane:~# kubectl describe deployments.apps frontend | grep -i image
    Image:        kodekloud/webapp-color:v3
```

---

Q13. Run the script `curl-test.sh` again. Notice the failures. Wait for the new application to be ready. Notice that the requests now do not hit both the versions

- Execute the script at `/root/curl-test.sh`.

```shell
root@controlplane:~# /root/curl-test.sh
Failed

Failed

Failed

Failed
```



