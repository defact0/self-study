Practice Test - Service Accounts

- https://kodekloud.com/topic/practice-test-service-accounts-2/

---

Q1. How many Service Accounts exist in the default namespace?

```shell
controlplane $ kubectl get serviceaccounts
NAME      SECRETS   AGE
default   1         119s
```

- 1

---

Q2. What is the secret token used by the default service account?

```shell
controlplane $ kubectl describe serviceaccount default 
Name:                default
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   default-token-ct7vc
Tokens:              default-token-ct7vc
Events:              <none>
```

- default-token-ct7vc

---

Q3. We just deployed the Dashboard application. Inspect the deployment. What is the image used by the deployment?

```shell
controlplane $ kubectl describe deployment
Name:                   web-dashboard
Namespace:              default
CreationTimestamp:      Wed, 25 Aug 2021 05:46:56 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               name=web-dashboard
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  name=web-dashboard
  Containers:
   web-dashboard:
    Image:        kodekloud/my-kubernetes-dashboard
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
NewReplicaSet:   web-dashboard-548dff47bd (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  55s   deployment-controller  Scaled up replica set web-dashboard-548dff47bd to 1
```

- `kodekloud/my-kubernetes-dashboard`

---

Q4. Wait for the deployment to be ready. Access the custom-dashboard by clicking on the link to dashboard portal.

- ok

---

Q5. What is the state of the dashboard? Have the pod details loaded successfully?

- Fail

---

Q6. What type of account does the Dashboard application use to query the Kubernetes API?

- `service account`

---

Q7. Which account does the Dashboard application use to query the Kubernetes API?

- `default`

---

Q8. Inspect the Dashboard Application POD and identify the Service Account mounted on it.

```shell
controlplane $ kubectl describe pod 
Name:         web-dashboard-548dff47bd-vwnnr
Namespace:    default
Priority:     0
Node:         node01/172.17.0.9
Start Time:   Wed, 25 Aug 2021 05:46:56 +0000
Labels:       name=web-dashboard
              pod-template-hash=548dff47bd
Annotations:  <none>
Status:       Running
IP:           10.244.1.2
IPs:
  IP:           10.244.1.2
Controlled By:  ReplicaSet/web-dashboard-548dff47bd
Containers:
  web-dashboard:
    Container ID:   docker://c8a22e5f54fa928e898a1c98c7b994eb5d113dc5e6d404d568b8dcf64a276845
    Image:          kodekloud/my-kubernetes-dashboard
    Image ID:       docker-pullable://kodekloud/my-kubernetes-dashboard@sha256:51261309eebea4f4d2224fe95dcbb664e0fea03bbaecb4ec930fb972c475d927
    Port:           8080/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Wed, 25 Aug 2021 05:47:06 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-ct7vc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-ct7vc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-ct7vc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  8m38s  default-scheduler  Successfully assigned default/web-dashboard-548dff47bd-vwnnr to node01
  Normal  Pulling    8m37s  kubelet, node01    Pulling image "kodekloud/my-kubernetes-dashboard"
  Normal  Pulled     8m29s  kubelet, node01    Successfully pulled image "kodekloud/my-kubernetes-dashboard" in 7.398112517s
  Normal  Created    8m28s  kubelet, node01    Created container web-dashboard
  Normal  Started    8m28s  kubelet, node01    Started container web-dashboard
```

- `default`

---

Q9. At what location is the ServiceAccount credentials available within the pod?

- ` var/run/secrets/`

---

Q10. The application needs a ServiceAccount with the Right permissions to be created to authenticate to Kubernetes. The 'default' ServiceAccount has limited access. Create a new ServiceAccount named 'dashboard-sa'.

```shell
controlplane $ kubectl create serviceaccount dashboard-sa
serviceaccount/dashboard-sa created
```

---

Q11. We just added additional permissions for the newly created 'dashboard-sa' account using RBAC.

If you are interested checkout the files used to configure RBAC at /var/rbac. We will discuss RBAC in a separate section.

```shell
controlplane $ kubectl describe secret dashboard-sa
Name:         dashboard-sa-token-pb9r9
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: dashboard-sa
              kubernetes.io/service-account.uid: 480f51cb-5e08-47fb-999d-7a351127d58c

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1066 bytes
namespace:  7 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6InVtSFp3R25ZWXdJaWh0VWtvSnI1Z3BIbmJpd0RfWUoxTkpZZS1TOFJYb0UifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRhc2hib2FyZC1zYS10b2tlbi1wYjlyOSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJkYXNoYm9hcmQtc2EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI0ODBmNTFjYi01ZTA4LTQ3ZmItOTk5ZC03YTM1MTEyN2Q1OGMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpkYXNoYm9hcmQtc2EifQ.fTZKa2GrHZVg8fawCqg8fbP5ZQpZcmy6lYB8TFNueXwm2_y4v8pAkCZbxeVi4TS4X-wpVX8k4TV8EpeKRcjggxyDrO7WMkN8nVL7Jym0eR3cPZ8UDaj4_lmOR2FLp2fIL7O7PlOh9tW9EH-QPt5BDE-sjGhjtu13rGCh07FNLBe9GLFqkgGthKLIIZ5HJP-8K2ycLxmPii6hM7WZSzynPVzVBfbdF2LF3unRSUwqv93ql8vm0SR_TbNHE5pZrtO5FldtZwy7rhAtS-pO-pDFTpsLbtMKMDElP_5_MKUoXsmCvmMz5JOYWrAtCW-_r3txLmWP6ERcRrmYU1ynqaDscQ
```

---

Q13. You shouldn't have to copy and paste the token each time. The Dashboard application is programmed to read token from the secret mount location. However currently, the 'default' service account is mounted. Update the deployment to use the newly created ServiceAccount

Edit the deployment to change ServiceAccount from 'default' to 'dashboard-sa'

```shell
```

