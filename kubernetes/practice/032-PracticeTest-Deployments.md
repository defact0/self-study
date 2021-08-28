Practice Test - Deployments

- https://uklabs.kodekloud.com/topic/practice-tests-deployments-2/

---

Q1. How many PODs exist on the system?

- In the current(default) namespace.

```shell
root@controlplane:~# kubectl get pod
No resources found in default namespace.
```

- Pod가 존재하지 않는다.

---

Q2. How many ReplicaSets exist on the system?

- In the current(default) namespace.

```shell
root@controlplane:~# kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   13m
root@controlplane:~# 
```

- ReplicaSets 가 존재하지 않는다.

---

Q3. How many Deployments exist on the system?

- In the current(default) namespace.

```shell
root@controlplane:~# kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   13m
root@controlplane:~# 
```

- Deployments  가 존재하지 않는다.

---

Q4. How many Deployments exist on the system now?

- We just created a Deployment! Check again! (환경이 변경되었으니 다시 확인!)

```shell
root@controlplane:~# kubectl get deployments.apps 
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
frontend-deployment   0/4     4            0           35s
root@controlplane:~# 
```

- `frontend-deployment` 1개가 존재 한다.

---

Q5. How many ReplicaSets exist on the system now?

```shell
root@controlplane:~# kubectl get rs
NAME                             DESIRED   CURRENT   READY   AGE
frontend-deployment-56d8ff5458   4         4         0       9m46s
root@controlplane:~# 
```

- ReplicaSets 이 1개 존재한다.

---

Q6. How many PODs exist on the system now?

```shell
root@controlplane:~# kubectl get pod
NAME                                   READY   STATUS             RESTARTS   AGE
frontend-deployment-56d8ff5458-5zvw4   0/1     ImagePullBackOff   0          7m36s
frontend-deployment-56d8ff5458-h9pn4   0/1     ImagePullBackOff   0          7m36s
frontend-deployment-56d8ff5458-hvnlv   0/1     ImagePullBackOff   0          7m36s
frontend-deployment-56d8ff5458-sn9w4   0/1     ImagePullBackOff   0          7m36s
root@controlplane:~# 
```

- 4개의 Pod가 있다.

---

Q7. Out of all the existing PODs, how many are ready?

- 상태가 정상인 Pod는 0개 이다.

---

Q8. What is the image used to create the pods in the new deployment?

```shell
# pod 리스트를 확인한다.
root@controlplane:~# kubectl get pod
NAME                                   READY   STATUS             RESTARTS   AGE
frontend-deployment-56d8ff5458-5zvw4   0/1     ErrImagePull       0          11m
frontend-deployment-56d8ff5458-h9pn4   0/1     ImagePullBackOff   0          11m
frontend-deployment-56d8ff5458-hvnlv   0/1     ErrImagePull       0          11m
frontend-deployment-56d8ff5458-sn9w4   0/1     ImagePullBackOff   0          11m

# 1개의 Pod를 선택하여 상세 정보를 본다.
#  - 확인할 것은 Pod를 생성하는데 사용한 이미지(image) 정보이다.
root@controlplane:~# kubectl describe pod frontend-deployment-56d8ff5458-5zvw4 | grep -i image
    Image:         busybox888
    Image ID:      
      Reason:       ImagePullBackOff
  Normal   Pulling    10m (x4 over 12m)    kubelet            Pulling image "busybox888"
  Warning  Failed     10m (x4 over 12m)    kubelet            Failed to pull image "busybox888": rpc error: code = Unknown desc = Error response from daemon: pull access denied for busybox888, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
  Warning  Failed     10m (x4 over 12m)    kubelet            Error: ErrImagePull
  Warning  Failed     10m (x6 over 12m)    kubelet            Error: ImagePullBackOff
  Normal   BackOff    2m5s (x42 over 12m)  kubelet            Back-off pulling image "busybox888"
root@controlplane:~# 

```

- `busybox888`을 사용한 것을 알 수 있다.

---

Q9. Why do you think the deployment is not ready?

- The image BUSYBOX888 doesn't exist

---

Q10. Create a new Deployment using the `deployment-definition-1.yaml` file located at `/root/`.

- There is an issue with the file, so try to fix it.
  - Name: deployment-1

```shell
# deployment 생성 실패의 원인을 찾아라!
root@controlplane:~# ls
deployment-definition-1.yaml  sample.yaml
root@controlplane:~# kubectl apply -f deployment-definition-1.yaml 
Error from server (BadRequest): error when creating "deployment-definition-1.yaml": deployment in version "v1" cannot be handled as a Deployment: no kind "deployment" is registered for version "apps/v1" in scheme "k8s.io/kubernetes/pkg/api/legacyscheme/scheme.go:30"


# deployment-definition-1.yaml을 수정한다.
apiVersion: apps/v1
#kind: deployment
kind: Deployment
metadata:

# 다시 생성한다
root@controlplane:~# kubectl apply -f deployment-definition-1.yaml 
deployment.apps/deployment-1 created
root@controlplane:~# kubectl get deployments.apps 
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment-1          0/2     2            0           9s
frontend-deployment   0/4     4            0           20m
root@controlplane:~# 
```

---

Q11. Create a new Deployment with the below attributes using your own deployment definition file.

- Name: `httpd-frontend`;
- Replicas: `3`;
- Image: `httpd:2.4-alpine`

```shell
# 조건에 맞는 yaml 파일을 생성한다.
root@controlplane:~# kubectl create deployment httpd-frontend --image=httpd:2.4-alpine --replicas=3 --dry-run=client -o yaml > newDeploy.yaml 

# 생성된 yaml 파일을 apply 한다.
root@controlplane:~# kubectl apply -f newDeploy.yaml 
deployment.apps/httpd-frontend created

# 정상적으로 생성되었는지 확인한다.
root@controlplane:~# kubectl get deployments.apps 
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment-1          0/2     2            0           6m22s
frontend-deployment   0/4     4            0           27m
httpd-frontend        3/3     3            3           13s
root@controlplane:~# 

```

