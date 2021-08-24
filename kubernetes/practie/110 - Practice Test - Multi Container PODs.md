Practice Test - Multi Container PODs

- https://uklabs.kodekloud.com/topic/practice-test-multi-container-pods-2/

---

Q1. Identify the number of containers created in the `red` pod.

```shell
root@controlplane:~# kubectl get pods
NAME        READY   STATUS              RESTARTS   AGE
app         0/1     ContainerCreating   0          56s
fluent-ui   0/1     ContainerCreating   0          56s
red         0/3     ContainerCreating   0          47s
```

- 3

---

Q2. Identify the name of the containers running in the `blue` pod.

```shell
# -----------------------------------------
# get pods
# -----------------------------------------
root@controlplane:~# kubectl get pods
NAME        READY   STATUS              RESTARTS   AGE
app         0/1     ContainerCreating   0          2m10s
blue        0/2     ContainerCreating   0          43s
fluent-ui   0/1     ContainerCreating   0          2m10s
red         0/3     ContainerCreating   0          2m1s

# -----------------------------------------
# describe pod blue
# -----------------------------------------
root@controlplane:~# kubectl describe pod blue 
Name:         blue
Namespace:    default
Priority:     0
Node:         controlplane/10.47.227.6
Start Time:   Mon, 23 Aug 2021 22:46:51 +0000
Labels:       <none>
Annotations:  <none>
Status:       Pending
IP:           
IPs:          <none>
Containers:
  teal:
    ...
  navy:
    ...
```

- `teal & navy`

---

Q3. Create a multi-container pod with 2 containers.

- Use the spec given below.
  If the pod goes into the `crashloopbackoff` then add `sleep 1000` in the `lemon` container.
  - Name: yellow
  - Container 1 Name: lemon
  - Container 1 Image: busybox
  - Container 2 Name: gold
  - Container 2 Image: redis

```shell
# -----------------------------------------
# create pod.yaml
# -----------------------------------------
kubectl run yellow --image=busybox --restart=Never --dry-run=client -o yaml > pod.yaml

# -----------------------------------------
# vi pod.yaml
# -----------------------------------------
vi pod.yaml

# -----------------------------------------
# pod.yaml
# -----------------------------------------
apiVersion: v1
kind: Pod
metadata:
  name: yellow
spec:
  containers:
  - name: lemon
    image: busybox
    command:
      - sleep
      - "1000"

  - name: gold
    image: redis
    
# -----------------------------------------
# pod/yellow created
# -----------------------------------------
root@controlplane:~# kubectl apply -f pod.yaml 
pod/yellow created
```

---

Q4. We have deployed an application logging stack in the `elastic-stack` namespace. Inspect it.

![](https://res.cloudinary.com/dezmljkdo/image/upload/v1627191939/kubernetes-ckad-elastic-stack_oacdz5.png)

- Before proceeding with the next set of questions, please wait for all the pods in the `elastic-stack` namespace to be ready. This can take a few minutes.

```shell
# -----------------------------------------
# get namespace
# -----------------------------------------
root@controlplane:~# kubectl get ns
NAME              STATUS   AGE
default           Active   18m
elastic-stack     Active   13m
kube-node-lease   Active   18m
kube-public       Active   18m
kube-system       Active   18m

# -----------------------------------------
# elastic-stack namespace get pod,svc
# -----------------------------------------
root@controlplane:~# kubectl -n elastic-stack get pod,svc
NAME                 READY   STATUS    RESTARTS   AGE
pod/app              1/1     Running   0          13m
pod/elastic-search   1/1     Running   0          13m
pod/kibana           1/1     Running   0          13m

NAME                    TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
service/elasticsearch   NodePort   10.105.110.151   <none>        9200:30200/TCP,9300:30300/TCP   13m
service/kibana          NodePort   10.110.60.178    <none>        5601:30601/TCP                  13m
root@controlplane:~# 

```

---

Q5. Once the pod is in a ready state, inspect the Kibana UI using the link above your terminal. There shouldn't be any logs for now.

- We will configure a sidecar container for the application to send logs to Elastic Search.
- NOTE: It can take a couple of minutes for the `Kibana` UI to be ready after the `Kibana` pod is ready.
- You can inspect the `Kibana` logs by running:
  `kubectl -n elastic-stack logs kibana`

---

Q6. Inspect the `app` pod and identify the number of containers in it.

- It is deployed in the `elastic-stack` namespace.

```shell
root@controlplane:~# kubectl -n elastic-stack get pod
NAME                 READY   STATUS    RESTARTS   AGE
pod/app              1/1     Running   0          13m
pod/elastic-search   1/1     Running   0          13m
pod/kibana           1/1     Running   0          13m
```

- app의 Pod의 1개 인 것을 확인 할 수 있다.

---

Q7. The application outputs logs to the file `/log/app.log`. View the logs and try to identify the user having issues with Login.

- Inspect the log file inside the pod.

```shell
# -----------------------------------------
# logs app
# -----------------------------------------
root@controlplane:~# kubectl -n elastic-stack logs app
root@controlplane:~# kubectl -n elastic-stack logs app | grep WARNING
```

- 로그를 보면 `USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.`가 반복적으로 출력되는 것을 확인 할 수 있다.
  - `USER5 `

---

Q8. Edit the pod to add a sidecar container to send logs to Elastic Search. Mount the log volume to the sidecar container.

- Only add a new container. Do not modify anything else. Use the spec provided below.
  - Name: app
  - Container Name: sidecar
  - Container Image: kodekloud/filebeat-configured
  - Volume Mount: log-volume
  - Mount Path: /var/log/event-simulator/
  - Existing Container Name: app
  - Existing Container Image: kodekloud/event-simulator

```shell
# -----------------------------------------
# create app.yaml
# -----------------------------------------
kubectl -n elastic-stack get pod app -o yaml > app.yaml

# -----------------------------------------
# delete app.yaml
# -----------------------------------------
kubectl delete pod app -n elastic-stack

# -----------------------------------------
# vi app.yaml
# -----------------------------------------
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: elastic-stack
  labels:
    name: app
spec:
  containers:
  - name: app
    image: kodekloud/event-simulator
    volumeMounts:
    - mountPath: /log
      name: log-volume

  - name: sidecar
    image: kodekloud/filebeat-configured
    volumeMounts:
    - mountPath: /var/log/event-simulator/
      name: log-volume

  volumes:
  - name: log-volume
    hostPath:
      # directory location on host
      path: /var/log/webapp
      # this field is optional
      type: DirectoryOrCreate


# -----------------------------------------
# apply app.yaml
# -----------------------------------------
root@controlplane:~# kubectl apply -f app.yaml 
pod/app created
```

---

Q9. Inspect the Kibana UI. You should now see logs appearing in the `Discover` section.

- You might have to wait for a couple of minutes for the logs to populate. You might have to create an index pattern to list the logs. If not sure check this video: `https://bit.ly/2EXYdHf`