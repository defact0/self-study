Practice Test - Image Security

- https://uklabs.kodekloud.com/topic/practice-test-image-security-2/

---

Q1. We have an application running on our cluster. Let us explore it first. What image is the application using?

```shell
controlplane $ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
web-bd975bd87-hllkn   1/1     Running   0          78s
web-bd975bd87-rvhqz   1/1     Running   0          78s

controlplane $ kubectl describe pod web-bd975bd87-hllkn 
Name:         web-bd975bd87-hllkn
....
    Image:          nginx:alpine
```

- `nginx:alpine`

---

Q2. We decided to use a modified version of the application from an internal private registry. Update the image of the deployment to use a new image from `myprivateregistry.com:5000`

- The registry is located at `myprivateregistry.com:5000`. Don't worry about the credentials for now. We will configure them in the upcoming steps.

- https://kubernetes.io/ko/docs/tasks/configure-pod-container/pull-image-private-registry/

```shell
# ------------------------------------------
# edit deployments.apps web 
controlplane $ kubectl get deployments.apps 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     2            2           8m42s

controlplane $ kubectl edit deployments.apps web 
deployment.apps/web edited

# ------------------------------------------
# containers.image 수정
    spec:
      containers:
      - image: myprivateregistry.com:5000/nginx:alpine
        imagePullPolicy: IfNotPresent
        name: nginx       
```

---

Q3. Are the new PODs created with the new images successfully running?

```shell
controlplane $ kubectl get pod
NAME                   READY   STATUS         RESTARTS   AGE
web-85fcf65896-b9qvg   0/1     ErrImagePull   0          112s
web-bd975bd87-hllkn    1/1     Running        0          11m
web-bd975bd87-rvhqz    1/1     Running        0          11m
```

- `web-85fcf65896-b9qvg` pod의 상태가  `ErrImagePull` 이다. => NO

---

Q4. Create a secret object with the credentials required to access the registry

- Name: `private-reg-cred`
- Username: `dock_user`
- Password: `dock_password`
- Server: `myprivateregistry.com:5000`
- Email: `dock_user@myprivateregistry.com`

```shell
# ------------------------------------------
# create secret
kubectl create secret docker-registry private-reg-cred --docker-username=dock_user --docker-password=dock_password --docker-server=myprivateregistry.com:5000 --docker-email=dock_user@myprivateregistry.com

# ------------------------------------------
# get secrets
controlplane $ kubectl get secrets 
NAME                  TYPE                                  DATA   AGE
default-token-qzqr4   kubernetes.io/service-account-token   3      15m
private-reg-cred      kubernetes.io/dockerconfigjson        1      29s
```

---

Q5. Configure the deployment to use credentials from the new secret to pull images from the private registry

- 
  Image Pull Secret: private-reg-cred

```shell
# ------------------------------------------
# Edit deployment using kubectl edit deploy web command and add imagePullSecrets section. Use private-reg-cred
controlplane $ kubectl get deployments.apps 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     1            2           15m

# ------------------------------------------
# edit deployments
controlplane $ kubectl edit deployments.apps web 
    spec:
      containers:
      - image: myprivateregistry.com:5000/nginx:alpine
      ...
      imagePullSecrets:
      - name: private-reg-cred
```

- https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-pod-that-uses-your-secret

---

Q6. Check the status of PODs. Wait for them to be running. You have now successfully configured a Deployment to pull images from the private registry

```shell
# ------------------------------------------
# get pod
controlplane $ kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
web-5f558bb687-h5s4x   1/1     Running   0          28s
web-5f558bb687-n6w8k   1/1     Running   0          26s

# ------------------------------------------
# describe pod의 image 확인
controlplane $ kubectl describe pod web-5f558bb687-h5s4x | grep -i image
    Image:          myprivateregistry.com:5000/nginx:alpine
    Image ID:       docker-pullable://nginx@sha256:...
  Normal  Pulling    53s   kubelet, node01    Pulling image "myprivateregistry.com:5000/nginx:alpine"
  Normal  Pulled     53s   kubelet, node01    Successfully pulled image "myprivateregistry.com:5000/nginx:alpine" in 69.818279ms
```

- 이전에 오류가 발생했던 이미지가 정상적으로 Running 상태로 실행하고 있다.