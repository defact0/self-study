Practice Test - Services

- https://uklabs.kodekloud.com/topic/practice-test-services-2/

---

Q1. How many Services exist on the system?

- in the current(default) namespace

```shell
root@controlplane:~# kubectl get service
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   6m5s
root@controlplane:~# 
```

- 현재 service는 1개가 존재한다.

---

Q2. That is a default service created by Kubernetes at launch.

- ok 클릭

Q3. What is the type of the default `kubernetes` service?

- ClusterIP

---

Q4. [★] What is the `targetPort` configured on the `kubernetes` service?

```shell
root@controlplane:~# kubectl get service
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   8m58s
root@controlplane:~# kubectl describe service kubernetes 
Name:              kubernetes
Namespace:         default
Labels:            component=apiserver
                   provider=kubernetes
Annotations:       <none>
Selector:          <none>
Type:              ClusterIP
IP Families:       <none>
IP:                10.96.0.1
IPs:               10.96.0.1
Port:              https  443/TCP
TargetPort:        6443/TCP
Endpoints:         10.28.153.3:6443
Session Affinity:  None
Events:            <none>
root@controlplane:~# 
```

- `TargetPort` 은 `6443` 이다.

---

Q5. How many labels are configured on the `kubernetes` service?

```shell
root@controlplane:~# kubectl describe service kubernetes 
Name:              kubernetes
Namespace:         default
Labels:            component=apiserver
                   provider=kubernetes
```

- label 이 2개 잡혀있다.

---

Q6. How many Endpoints are attached on the `kubernetes` service?

```shell
root@controlplane:~# kubectl describe svc kubernetes 
Name:              kubernetes
Namespace:         default
Labels:            component=apiserver
                   provider=kubernetes
...
Endpoints:         10.29.53.6:6443
...
```

- Endpoints는 1개가 설정되어 있다.

---

Q7. How many Deployments exist on the system now?

- in the current(default) namespace

```shell
root@controlplane:~# kubectl get deployments.apps 
NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
simple-webapp-deployment   4/4     4            4           78s
```

- Deployments 리소스가 1개 있다.

---

Q8. What is the image used to create the pods in the deployment?

```shell
root@controlplane:~# kubectl get deployments.apps 
NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
simple-webapp-deployment   4/4     4            4           78s

root@controlplane:~# kubectl get pod
NAME                                       READY   STATUS    RESTARTS   AGE
simple-webapp-deployment-b56f88b77-b6thf   1/1     Running   0          2m13s
simple-webapp-deployment-b56f88b77-dglnh   1/1     Running   0          2m13s
simple-webapp-deployment-b56f88b77-hdbqr   1/1     Running   0          2m13s
simple-webapp-deployment-b56f88b77-zrmfn   1/1     Running   0          2m13s

root@controlplane:~# kubectl describe pod simple-webapp-deployment-b56f88b77-b6thf | grep -i image
    Image:          kodekloud/simple-webapp:red
    Image ID:       docker-pullable://kodekloud/simple-webapp@sha256:175ba08b8986076df14c40db45c4cc1fbbb16ffff031a646d6bc98f20fb5d902
  Normal  Pulling    2m33s  kubelet            Pulling image "kodekloud/simple-webapp:red"
  Normal  Pulled     2m22s  kubelet            Successfully pulled image "kodekloud/simple-webapp:red" in 10.931785222s
```

- Image 는 kodekloud/simple-webapp:red 으로 사용하였다.

---

Q9. Are you able to accesss the Web App UI?

- Try to access the Web Application UI using the tab simple-webapp-ui above the terminal.
  - `502 Bad Gateway` 으로 출력된다.
  - `NO` 선택

---

Q10. [★★] Create a new service to access the web application using the service-definition-1.yaml file

- `Name:` webapp-service
- `Type:` NodePort
- `targetPort:` 8080
- `port:` 8080
- `nodePort:` 30080
- `selector:` simple-webapp

```shell
# deployment 생성
kubectl expose deployment simple-webapp-deployment --name=simple-webapp --target-port=8080 --type=NodePort --port=8080 --dry-run=client -o yaml > service-definition-1.yaml

# svc.yaml 파일 수정
vi svc.yaml

# [ nodePort: 30080 ] 추가
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  name: simple-webapp
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
    nodePort: 30080
  selector:
    name: simple-webapp
  type: NodePort
status:
  loadBalancer: {}
  
# svc.yaml 적용
kubectl apply -f service-definition-1.yaml
```

- `Hello from simple-webapp-deployment-b56f88b77-mpglb!` 이런 메세지가 나오는데 `check` 버튼으로 확인하면 오류가 발생하니 넘어가도록 한다.