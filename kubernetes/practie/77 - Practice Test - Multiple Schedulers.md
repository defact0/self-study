Practice Test - Multiple Schedulers

- https://uklabs.kodekloud.com/topic/practice-test-multiple-schedulers-2/

---

Q1. What is the name of the POD that deploys the default kubernetes scheduler in this environment?

```shell
root@controlplane:~# kubectl get pods --namespace=kube-system
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-74ff55c5b-4wpdb                1/1     Running   0          17m
coredns-74ff55c5b-kpdng                1/1     Running   0          17m
etcd-controlplane                      1/1     Running   0          17m
kube-apiserver-controlplane            1/1     Running   0          17m
kube-controller-manager-controlplane   1/1     Running   0          17m
kube-flannel-ds-nv2n5                  1/1     Running   0          17m
kube-proxy-77c9g                       1/1     Running   0          17m
kube-scheduler-controlplane            1/1     Running   0          17m
root@controlplane:~# 
```

- `kube-scheduler-controlplane`

---

Q2. What is the image used to deploy the kubernetes scheduler?

- Inspect the kubernetes scheduler pod and identify the image

```shell
# --------------------------------------------------
# kube-scheduler-controlplane 상세보기
# --------------------------------------------------
root@controlplane:~# kubectl describe pod kube-scheduler-controlplane --namespace=kube-system

# --------------------------------------------------
# grep -i image 만 출력
# --------------------------------------------------
root@controlplane:~# kubectl describe pod kube-scheduler-controlplane --namespace=kube-system | grep -i image
    Image:         k8s.gcr.io/kube-scheduler:v1.20.0
    Image ID:      docker-pullable://k8s.gcr.io/kube-scheduler@sha256:beaa71032..
```

- `k8s.gcr.io/kube-scheduler:v1.20.0`

---

Q3. Deploy an additional scheduler to the cluster following the given specification.

- Use the manifest file used by kubeadm tool. Use a different port than the one used by the current one.
  - Namespace: kube-system
  - Name: my-scheduler
  - Status: Running
  - Custom Scheduler Name

```shell
# --------------------------------------------------
# /etc/kubernetes/manifests/kube-scheduler.yaml 복사
# --------------------------------------------------
root@controlplane:~# cd /etc/kubernetes/manifests/
root@controlplane:/etc/kubernetes/manifests# ls
etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml
root@controlplane:/etc/kubernetes/manifests# cp kube-scheduler.yaml /root/kube-scheduler.yaml
root@controlplane:/etc/kubernetes/manifests# cd ~
root@controlplane:~# ls
kube-scheduler.yaml  nginx-pod.yaml

# --------------------------------------------------
# kube-scheduler.yaml 수정
#  - 공식 웹에서 Multiple Schedulers 검색
# --------------------------------------------------
root@controlplane:~# vi kube-scheduler.yaml 
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: my-scheduler
    tier: control-plane
  name: my-scheduler
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-scheduler
    - --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
    - --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
    - --bind-address=127.0.0.1
    - --kubeconfig=/etc/kubernetes/scheduler.conf
    - --leader-elect=false
    - --port=10282
    - --scheduler-name=my-scheduler
    - --secure-port=0
    image: k8s.gcr.io/kube-scheduler:v1.19.0
    imagePullPolicy: IfNotPresent
    livenessProbe:
      failureThreshold: 8
      httpGet:
        host: 127.0.0.1
        path: /healthz
        port: 10282
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 15
    name: kube-scheduler
    resources:
      requests:
        cpu: 100m
    startupProbe:
      failureThreshold: 24
      httpGet:
        host: 127.0.0.1
        path: /healthz
        port: 10282
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 15
    volumeMounts:
    - mountPath: /etc/kubernetes/scheduler.conf
      name: kubeconfig
      readOnly: true
  hostNetwork: true
  priorityClassName: system-node-critical
  volumes:
  - hostPath:
      path: /etc/kubernetes/scheduler.conf
      type: FileOrCreate
    name: kubeconfig
status: {}

# --------------------------------------------------
# yaml 파일 적용 후 확인
# --------------------------------------------------
root@controlplane:~# kubectl apply -f kube-scheduler.yaml 
pod/my-scheduler created
root@controlplane:~# kubectl get pod -n kube-system
NAME                                   READY   STATUS             RESTARTS   AGE
coredns-74ff55c5b-4wpdb                1/1     Running            0          31m
coredns-74ff55c5b-kpdng                1/1     Running            0          31m
etcd-controlplane                      1/1     Running            0          31m
kube-apiserver-controlplane            1/1     Running            0          31m
kube-controller-manager-controlplane   1/1     Running            0          31m
kube-flannel-ds-nv2n5                  1/1     Running            0          31m
kube-proxy-77c9g                       1/1     Running            0          31m
kube-scheduler-controlplane            1/1     Running            0          31m
my-scheduler                           0/1     CrashLoopBackOff   1          24s
```

- https://v1-19.docs.kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/#define-a-kubernetes-deployment-for-the-scheduler
- `my-scheduler` Pod 가 생성 됨을 확인 할 수 있다.

---

Q4. A POD definition file is given. Use it to create a POD with the new custom scheduler.

- File is located at `/root/nginx-pod.yaml`
  - Name: nginx
  - Uses custom scheduler
  - Status: Running

```shell
# --------------------------------------------------
# nginx-pod.yaml 파일 제공
# --------------------------------------------------
root@controlplane:~# ls
kube-scheduler.yaml  nginx-pod.yaml
root@controlplane:~# vi nginx-pod.yaml

# --------------------------------------------------
# nginx-pod.yaml 수정 내용
# --------------------------------------------------
---
apiVersion: v1 
kind: Pod 
metadata:
  name: nginx 
spec:
  schedulerName: my-scheduler
  containers:
  - image: nginx
    name: nginx
    
# --------------------------------------------------
# nginx-pod.yaml 적용 후 확인
# --------------------------------------------------
root@controlplane:~# kubectl apply -f nginx-pod.yaml 
pod/nginx created
root@controlplane:~# kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          2m45s
```

