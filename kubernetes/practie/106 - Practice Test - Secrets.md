Practice Test - Secrets

- https://uklabs.kodekloud.com/topic/practice-test-secrets-2/

---

Q1. How many `Secrets` exist on the system?

- in the current(default) namespace

```shell
root@controlplane:~# kubectl get secrets
NAME                  TYPE                                  DATA   AGE
default-token-fqtcp   kubernetes.io/service-account-token   3      6m59s
```

- 1

---

Q2. How many secrets are defined in the `default-token` secret?

```shell
root@controlplane:~# kubectl get secrets
NAME                  TYPE                                  DATA   AGE
default-token-fqtcp   kubernetes.io/service-account-token   3      6m59s

root@controlplane:~# kubectl describe secrets default-token-fqtcp 
Name:         default-token-fqtcp
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: default
              kubernetes.io/service-account.uid: 8573d47a-b147-46e6-bc0f-d44b76b0579c

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1066 bytes
namespace:  7 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IktiVDR4d1ZTUWNrUXVrTnE5dWdya0VXYkVkTW9CSl9rQ0pNX2w3OERFejgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tZnF0Y3AiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg1NzNkNDdhLWIxNDctNDZlNi1iYzBmLWQ0NGI3NmIwNTc5YyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.Q1nVHLDYxfX3wB8GpNxwRYW2qQyEogHah1peLaAYQaYohZKH52lrfHaV604EI_Ujhng-CgVM0aS--XgpCFflFRNNzosV6u5mTkhuhTjrFzOsGF2eE7Fi5aVYTVnofyhcSMEtvkNmU-PgHUc2Zx2RIgUOKIN2I3D8X2mLpnMOnV1x3xB5hHor1Rq0vq_uvef1H7JjsXKEFc-9ImIDXBUvcOQyQX99Uo-1O0J_ITwuAGA9fJdz_xD1hdFnVf4oxqlbLbMaRhzLDu-mZzUNjfOE7LEcKlf6xJPa-Gpk3GHpV4VS4xnZ0-8SqvjgmxKaoGR42rsvJ2VnK1jP13IIdY6aXg
```

- 3 - (There are three secrets - `ca.crt`, `namespace` and `token`.)
  - Run the command `kubectl describe secrets deploy-token-<id>` and look at the `data` field.
    There are three secrets - `ca.crt`, `namespace` and `token`.

---

Q3. What is the type of the `default-token` secret?

```shell
root@controlplane:~# kubectl describe secrets default-token-fqtcp 
Name:         default-token-fqtcp
...
Type:  kubernetes.io/service-account-token
...
```

- kubernetes.io/service-account-token

---

Q4. Which of the following is not a secret data defined in `default-token` secret?

- `type`
  - There are three secrets - `ca.crt`, `namespace` and `token`.

---

Q5. We are going to deploy an application with the below architecture

- We have already deployed the required pods and services. Check out the pods and services created. Check out the web application using the `Webapp MySQL` link above your terminal, next to the Quiz Portal Link.

```shell
root@controlplane:~# kubectl get pods,svc
NAME             READY   STATUS    RESTARTS   AGE
pod/mysql        1/1     Running   0          79s
pod/webapp-pod   1/1     Running   0          79s

NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP          17m
service/sql01            ClusterIP   10.99.161.72    <none>        3306/TCP         79s
service/webapp-service   NodePort    10.102.171.77   <none>        8080:30080/TCP   79s
```

- webpage

```log
Failed connecting to the MySQL database.
Environment Variables: DB_Host=Not Set; DB_Database=Not Set; DB_User=Not Set; DB_Password=Not Set; 2003: Can't connect to MySQL server on 'localhost:3306' (111 Connection refused)
From webapp-pod!
```

---

Q6. The reason the application is failed is because we have not created the secrets yet. Create a new secret named `db-secret` with the data given below.

- You may follow any one of the methods discussed in lecture to create the secret.
  - Secret Name: db-secret
  - Secret 1: DB_Host=sql01
  - Secret 2: DB_User=root
  - Secret 3: DB_Password=password123

```shell
#
# create secret
#
root@controlplane:~# kubectl create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=password123
secret/db-secret created

#
# describe secrets db-secret
#
root@controlplane:~# kubectl describe secrets db-secret
Name:         db-secret
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
DB_User:      4 bytes
DB_Host:      5 bytes
DB_Password:  11 bytes
```

---

Q7. Configure `webapp-pod` to load environment variables from the newly created secret.

- Delete and recreate the pod if required.
  - Pod name: webapp-pod
  - Image name: kodekloud/simple-webapp-mysql
  - Env From: Secret=db-secret

```shell
#
# get pods
#
root@controlplane:~# kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
mysql        1/1     Running   0          16m
webapp-pod   1/1     Running   0          16m

#
# create pod.yaml
#
root@controlplane:~# kubectl get pod webapp-pod -o yaml > pod.yaml

#
# delete pod webapp-pod
#
root@controlplane:~# kubectl delete pod webapp-pod
pod "webapp-pod" deleted

#
# vi pod.yaml
#
vi pod.yaml
# 필요없는 설정은 삭제

kubectl explain pods --recursive | less
# envFrom 설정 부분 찾기
kubectl explain pods --recursive | grep -A8 envFrom
# 설정값을 복사해서 pod.yaml 에 붙여넣기
---
apiVersion: v1 
kind: Pod 
metadata:
  labels:
    name: webapp-pod
  name: webapp-pod
  namespace: default 
spec:
  containers:
  - image: kodekloud/simple-webapp-mysql
    imagePullPolicy: Always
    name: webapp
    envFrom:
    - secretRef:
        name: db-secret
        
#
# apply pod.yaml
#
kubectl apply -f pod.yaml
```

---

Q8. View the web application to verify it can successfully connect to the database

- 웹 페이지가 정상동작하는 것을 확인