Practice Test - Imperative Commands

- https://uklabs.kodekloud.com/topic/practice-test-imperative-commands-3/

> 이번 연습테스트는 YAML 파일을 생성하지 않고 명령어 만으로 리소스를 생성하는 것이다.
>
> - pod 생성 시 `kubectl run pod (x)`  ` kubectl run redis (o)` 실수 하는 부분을 고쳐라
> - deployment 리소스에서 replicas 설정을 하려면 
>   `kubectl create deployment ` 형태로 먼저 생성 후 
>   `kubectl scale deployment <리소스이름> --replicas=` 형태로 작성해라
> - service 생성 시 `kubectl expose pod <pod이름> --name <service 이름>` 형태로 생성해라

---

Q1. In this lab, you will get hands-on practice with creating Kubernetes objects imperatively.

>  All the questions in this lab can be done imperatively. However, for some questions, you may need to first create the YAML file using imperative methods. You can then modify the YAML according to the need and create the object using `kubectl apply -f` command.

---

Q2. Deploy a pod named `nginx-pod` using the `nginx:alpine` image.

- Use imperative commands only.
  - Name: nginx-pod
  - Image: nginx:alpine

```shell
# 주의!
#  kubectl run pod nginx-pod 이런식으로 명령하면 안된다. (X)
#  kubectl run nginx-pod 이런식으로 명령해야 한다. (O)
root@controlplane:~# kubectl run nginx-pod --image=nginx:alpine

root@controlplane:~# kubectl get pod
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          4s
```

---

Q3. Deploy a `redis` pod using the `redis:alpine` image with the labels set to `tier=db`.

> Either use imperative commands to create the pod with the labels. Or else use imperative commands to generate the pod definition file, then add the labels before creating the pod using the file.

- Pod Name: redis
- Image: redis:alpine
- Labels: tier=db

```shell
root@controlplane:~# kubectl run redis --image=redis:alpine --labels=tier=db
```

---

Q4. [★] Create a service `redis-service` to expose the `redis` application within the cluster on port `6379`.

- Service: redis-service
- Port: 6379
- Type: ClusterIP

```shell
kubectl expose pod redis --name redis-service --port 6379 --target-port 6379
```

---

Q5. Create a deployment named `webapp` using the image `kodekloud/webapp-color` with `3` replicas.

- Name: webapp
- Image: kodekloud/webapp-color
- Replicas: 3

```shell
# deployment 리소스 생성
root@controlplane:~# kubectl create deployment webapp --image=kodekloud/webapp-color
deployment.apps/webapp created


# replicas 설정
root@controlplane:~# kubectl scale deployment webapp --replicas=3
deployment.apps/webapp scaled

root@controlplane:~# kubectl get deployments.apps 
NAME     READY   UP-TO-DATE   AVAILABLE   AGE
webapp   3/3     3            3           43s

```

---

Q6. Create a new pod called `custom-nginx` using the `nginx` image and expose it on `container port 8080`.

```shell
root@controlplane:~# kubectl run custom-nginx --image=nginx --port=8080
pod/custom-nginx created

# 설정내용 확인하기
root@controlplane:~# kubectl describe pod custom-nginx                               
Name:         custom-nginx
Namespace:    default
Priority:     0
Node:         controlplane/10.30.73.9
Start Time:   Sat, 21 Aug 2021 17:43:37 +0000
Labels:       run=custom-nginx
Annotations:  <none>
Status:       Running
IP:           10.244.0.11
IPs:
  IP:  10.244.0.11
Containers:
  custom-nginx:
    Container ID:   docker://1789676fc4e1d399cfae52e39b4e37ae2e7b3e34165e08bf0555985118c8e0c0
    Image:          nginx
    Image ID:       docker-pullable://nginx@sha256:4d4d96ac750af48c6a551d757c1cbfc071692309b491b70b2b8976e102dd3fef
    Port:           8080/TCP
```

---

Q7. Create a new namespace called `dev-ns`.

```shell
root@controlplane:~# kubectl create ns dev-ns
namespace/dev-ns created

root@controlplane:~# kubectl get namespaces 
NAME              STATUS   AGE
default           Active   32m
dev-ns            Active   12s
kube-node-lease   Active   32m
kube-public       Active   32m
kube-system       Active   32m
root@controlplane:~# 
```

---

Q8. [★] Create a new deployment called `redis-deploy` in the `dev-ns` namespace with the `redis` image. It should have `2` replicas.

- 'redis-deploy' created in the 'dev-ns' namespace?
- replicas: 2

```shell
# redis-deploy.yaml 생성
root@controlplane:~# kubectl create deployment redis-deploy --image=nginx --namespace=dev-ns --dry-run=client -o yaml > redis-deploy.yaml

# replicas를 수정한다.
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: redis-deploy
  name: redis-deploy
  namespace: dev-ns
spec:
  replicas: 2 

# redis-deploy.yaml 적용하기
root@controlplane:~# kubectl apply -f redis-deploy.yaml 
deployment.apps/redis-deploy created


# namespace=dev-ns 를 지정하여 deployments를 확인하기
root@controlplane:~# kubectl get deployments.apps -n dev-ns
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
redis-deploy   2/2     2            2           3m9s
```

---

Q9. [★]  Create a pod called `httpd` using the image `httpd:alpine` in the default namespace. Next, create a service of type `ClusterIP` by the same name `(httpd)`. The target port for the service should be `80`.

- 'httpd' pod created with the correct image?
- 'httpd' service is of type 'ClusterIP'?
- 'httpd' service uses correct target port 80?
- 'httpd' service exposes the 'httpd' pod?

```shell
kubectl run httpd --image=httpd:alpine --port 80 --expose
```

- pod 생성 시간이 조금 걸리니 기다려라



