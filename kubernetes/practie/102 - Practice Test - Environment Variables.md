Practice Test - Environment Variables

- https://uklabs.kodekloud.com/topic/practice-test-env-variables-2/

---

Q1. How many PODs exist on the system?

- in the current(default) namespace

```shell
root@controlplane:~# kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
webapp-color   1/1     Running   0          53s
```

- 1

---

Q2. What is the environment variable name set on the container in the pod?

```shell
root@controlplane:~# kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
webapp-color   1/1     Running   0          53s
root@controlplane:~# kubectl describe pod webapp-color                                     
Name:         webapp-color
Namespace:    default
Priority:     0
Node:         controlplane/10.26.35.9
Start Time:   Mon, 23 Aug 2021 13:19:29 +0000
Labels:       name=webapp-color
Annotations:  <none>
Status:       Running
IP:           10.244.0.4
IPs:
  IP:  10.244.0.4
Containers:
  webapp-color:
    Container ID:   docker://...
    Image:          kodekloud/webapp-color
    Image ID:       docker-pullable://kodekloud/webapp-color@sha256:....
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Mon, 23 Aug 2021 13:19:47 +0000
    Ready:          True
    Restart Count:  0
    Environment:
      APP_COLOR:  pink
```

- `APP_COLOR`

---

Q3. What is the value set on the environment variable `APP_COLOR` on the container in the pod?

- `pink`

---

Q4. View the web application UI by clicking on the `Webapp Color` Tab above your terminal.

- This is located on the right side.
- `Webapp Color` 버튼 클릭하여 Web페이지 확인

---

Q5. Update the environment variable on the POD to display a `green` background

- Note: Delete and recreate the POD. Only make the necessary changes. Do not modify the name of the Pod.
  - Pod Name: webapp-color
  - Label Name: webapp-color
  - Env: APP_COLOR=green

```shell
root@controlplane:~# kubectl get pod webapp-color -o yaml > webapp-color.yaml
root@controlplane:~# vi webapp-color.yaml 

root@controlplane:~# kubectl delete pod webapp-color 
pod "webapp-color" deleted
root@controlplane:~# kubectl get pod
No resources found in default namespace.

root@controlplane:~# kubectl apply -f webapp-color.yaml 
pod/webapp-color created
root@controlplane:~# kubectl get pod
NAME           READY   STATUS    RESTARTS   AGE
webapp-color   1/1     Running   0          5s
```

---

Q6. View the changes to the web application UI by clicking on the `Webapp Color` Tab above your terminal.

- If you already have it open, simply refresh the browser.
  - 웹 페이지를 새로고침하면 Pink -> Green 으로 변경되어 있음을 확인 할 수 있다.

---

Q7. How many `ConfigMaps` exist in the environment?

```shell
root@controlplane:~# kubectl get configmaps
NAME               DATA   AGE
db-config          3      11s
kube-root-ca.crt   1      16m
```

- 2

---

Q8. Identify the database host from the config map `db-config`

```shell
root@controlplane:~# kubectl get configmaps
NAME               DATA   AGE
db-config          3      11s
kube-root-ca.crt   1      16m
root@controlplane:~# kubectl describe configmaps db-config 
Name:         db-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
DB_HOST:
----
SQL01.example.com
DB_NAME:
----
SQL01
DB_PORT:
----
3306
Events:  <none>
```

- `SQL01.example.com`

---

Q9. Create a new ConfigMap for the `webapp-color` POD. Use the spec given below.

- ConfigName Name: webapp-config-map
- Data: APP_COLOR=darkblue

```shell
root@controlplane:~# kubectl create configmap webapp-config-map --from-literal=APP_COLOR=darkblue
configmap/webapp-config-map created

root@controlplane:~# kubectl get configmaps 
NAME                DATA   AGE
db-config           3      2m52s
kube-root-ca.crt    1      18m
webapp-config-map   1      13s
```

---

Q10. Update the environment variable on the POD to use the newly created ConfigMap

- Note: Delete and recreate the POD. Only make the necessary changes. Do not modify the name of the Pod.
  - Pod Name: webapp-color
  - EnvFrom: webapp-config-map

```shell
kubectl delete pod webapp-color

# 해당 내용을 복사
kubectl explain pods --recursive | grep enFrom -A3

# pod 수정
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: webapp-color
  name: webapp-color
  namespace: default
spec:
  containers:
  - envFrom:
    - configMapRef:
         name: webapp-config-map
    image: kodekloud/webapp-color
    name: webapp-color
    
# pod 삭제 후 적용
kubectl delete pod webapp-color
kubectl apply -f pod.yaml
```

---

Q11. View the changes to the web application UI by clicking on the `Webapp Color` Tab above your terminal.

- If you already have it open, simply refresh the browser.
- `Ok` 버튼을 누른다.