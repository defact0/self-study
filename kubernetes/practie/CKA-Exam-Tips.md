**CKA Exam Tips**

- 유튜브 [링크](https://www.youtube.com/channel/UC3aWdGjZDBckm8zgCX_kKHw/videos)

---

**Kubernetes.. ETCD Backup and Restore**

- ETCD
  - key-value store, secure and fast
  - port 2379

```shell
# ----------------------------------------------
# etcd 백업
etcdctl -version
kubectl -n kube-system get pod
kubectl -n kube-system describe pod etcd-controlplane
kubectl get deployments.apps

# 공식 웹 -> etcd snapshot 으로 검색
# https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#volume-snapshot
# 관련 명령어 복사 (메모장으로 작업)
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=<trusted-ca-file> --cert=<cert-file> --key=<key-file> \
  snapshot save /opt/snapshotdb.db

# ----------------------------------------------
# etcd 복원
# https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#volume-snapshot
# [공식] ETCDCTL_API=3 etcdctl --endpoints 10.2.0.9:2379 snapshot restore snapshotdb
ETCDCTL_API=3 etcdctl --data-dir=/var/lib/etcd-backup snapshot restore /opt/snapshotdb.db
# data-dir 옵션은 복원하는 DB파일 위치를 새롭게 선언하는 것
cd /etc/kubernetes/manifestes/
vi etcd.yaml
# volumes 항목에 name이 etcd-data 부분이 있는데 path를 /var/lib/etcd-backup 으로 수정한다.
#
# 정리하자면,
# 복원하는 etcd db파일을 새로운 위치에 설정하는 방식(기본위치가 아님)
```

---

**Kubernetes .. Cluster Upgrade (Master and Worker Node)..** 

- 업그레이드는 controlplane 부터 시작하며 작업은 동일하게 진행된다.

```shell
kubectl get node

# ---------------------------------------
# controlplane node upgrade command
kubeadm upgrade plan
kubectl drain controlplane -ignore-daemonsets
apt update
apt install kubeadm=1.19.0-00
kubeadm upgrade apply v1.19.0
apt install kubelet=1.19.0-00
systemctl restart kubelet
kubectl uncordon controlplane

# ---------------------------------------
# worker node upgrade command
kubectl drain node01 -ignore-daemonsets
ssh node01
apt install kubeadm=1.19.0-00
kubeadm upgrade apply v1.19.0
apt install kubelet=1.19.0-00
systemctl restart kubelet
kubectl uncordon node01
```

---

**Kubernetes .. Static Pod ..Very easy steps to create it**

- static pod 관련 공식 문서 ([링크](https://kubernetes.io/ko/docs/tasks/configure-pod-container/static-pod/))
- API 서버 없이 kubelet 데몬에 의해 관리
  - Pod 이름에 노드 호스트 이름 앞에 하이픈을 붙여 접미사로 추가 된다.
  - YAML에 정의된 Pod 이름이 static-worker 이고, 호스트 이름이 controlplane 이면 생성된 Pod 이름은 static-worker-controlplane 이 된다.

```shell
# --------------------------------------------
# controlplane
ps -aux | grep kubelet
# --config 부분의 value 값을 확인

cat /var/lib/kubelet/config.yaml
# staticPodPath: /etc/kubernetes/manifests

cd /etc/kubernetes/manifests
vi static.yaml
# static.yaml 내용
apiVersion: v1
kind: Pod
metadata:
  name: static-controlplane
spec:
  containers:
  - image: busybox
    name: static
    command: ["sleep", "1000"]
# 기존에 생성된 Pod이 있다면 지워준다.
# 지우면 다시 자동으로 /etc/kubernetes/manifests 경로에 작성했었던 Pod이 생성되었음을 확인 할 수 있다.
kubectl get pod

# --------------------------------------------
# worker
# node01 노드로 접속하여 controlplane에서 했던 작업을 수행한다.
ssh node01

ps -aux | grep kubelet
cat /var/lib/kubelet/config.yaml
vi static1.yaml
# static1.yaml 내용
apiVersion: v1
kind: Pod
metadata:
  name: static-worker
spec:
  containers:
  - image: busybox
    name: static
    command: ["sleep", "1000"]
    
# exit 명령으로 node01를 빠져나와 controlplane에서
# 생성된 pod를 확인하면 /etc/kubernetes/manifests 에서 작성된
# pod가 자동 생성된 것을 확인 할 수 있다.
kubectl get pod
```

---

**Kubernetes ... Simple Pod Creation ... Imperative and Declarative way ..**

- Pod Definition File

  | Kind       | Version |
  | ---------- | ------- |
  | Pod        | v1      |
  | Service    | v1      |
  | ReplicaSet | apps/v1 |
  | Deployment | apps/v1 |

- some important command

  ```shell
  # Createing a Pod
  kubectl apply -f pod.yaml
  
  # View created Pod
  kubectl get pod
  
  # Details description on Pod
  kubectl describe pod static-web
  
  # Details of Pod with wide option
  kubectl get pod static-web -o wide
  
  # Details of Pod with label option
  kubectl get pod -l role=myrole
  
  # Image used for this pod creation
  kubectl describe pod static-web | grep -i image
  ```

- lab session

  ```shell
  # 생성된 pod 확인
  kubectl get pod
  
  # nginx pod 만들기
  kubectl run simple-pod --image=nginx
  
  # nginx pod 상세보기
  kubectl describe pod simple-pod
  
  # pod을 yaml 파일로 저장하기
  kubectl run simple-pod1 --image=nginx --dru-run=client -o yaml > simple-pod1.yaml
  
  # 만들어진 yaml파일을 pod로 생성하기
  # metadata.labels 부분에 env: dev 를 추가
  kubectl apply -f simple-pod1.yaml
  
  # label을 이용하여 pod를 select 하기
  #   simple-pod1.yaml에서 작성된
  #   env: dev 정보를 확인하고 해당 pod을 출력한다.
  kubectl get pod -l env=dev
  
  # pod을 삭제하기
  kubectl delete pod simple-pod
  ```

---

**Kubernetes .. ReplicaSet .. Share the load ... Very Well Explained ...**

- ReplicaSet을 yaml파일로 정의 할 때 template 부분의 Pod 를 추가 정의 한다.

- Creating a ReplicaSet

  ```shell
  # yaml
  apiVersion: apps/v1
  kind: ReplicaSet
  ...
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: nginx
    template:
      # pod defind
  
  # apply
  kubectl apply -f rs.yaml
  ```

- some important command

  ```shell
  # View created ReplicaSet
  kubectl get rs
  
  # Details description on ReplicaSet
  kubectl describe rs replicaset-example
  
  # Details of Replicaset with wide option
  kubectl get rs replicaset-example -o wide
  
  # Image used for this ReplicaSet creation
  kubectl describe rs replicaset-example | grep -i image
  ```

- lab session

  ```shell
  # rs.yaml create
  kubectl create deployment rs-simple --image=nginx --replicas=3 --dry-run=client -o yaml > rs.yaml
  
  # vi rs.yaml
  # kind를 ReplicaSet 으로 변경
  kubectl apply -f rs.yaml
  kubectl get rs
  
  # --replicas=3 에 의해 Pod가 3개로 유지되는지 체크해라
  kubectl delete pod rs-simple-27q7r
  
  # edit replicaSet
  kubectl edit rs rs-simple
  ```

----

**Kubernetes .. Deployments...**

- creating a Deploymet

  ```shell
  kubectl create Deployment <deployment-name> --image=<image-name> -o yaml > depoy.yaml
  # deployment 라벨은 같이 생성되는 pod의 라벨과 동일해야 한다.
  
  kubectl apply -f depoy.yaml
  ```

- some important command

  ```shell
  # view all created deplotment
  kubectl get deployment
  
  # details description on deployment
  kubectl describe deployment deployment-example
  
  # details of deployment with option
  kubectl get deployment deployment-example -o wide
  
  # image used for this deployment
  kubectl describe deployment deployment-example | grep -i image
  
  # check the history of deployment
  kubectl rollout history deployment <deployment-name>
  
  # get more information about revision number for the deployment
  kubectl rollout history deployment <deployment-name> --revision 1
  
  # rollback to any particular deployment version
  kubectl set image deployment <deployment-name> <container-name>=<new-image>
  
  # scale exsting deployment
  kubectl scale deployment <deployment-name> --replicas 10
  
  # rollout undo
  kubectl rollout undo deploymnet <deployment-name>
  ```

- lab session

  ```shell
  # create deployment
  kubectl create deployment web --image=nginx:1.20.1
  
  # create check
  kubectl get deployments
  kubectl get rs
  kubectl get pod
  
  # replicas 설정
  kubectl scale deployment web --replicas=4
  
  # pod image 변경
  #  - record 옵션은 rollout을 하기 위한 기록
  kubectl set image deployment web nginx=nginx:1.21.1 --record
  
  # image를 이전상태로 되돌리기
  kubectl rollout histroy deployment web
  kubectl rollout undo deployment web
  
  ```

---

**Kubernetes .. Label and Selector**

- labels은 key-value 형태로 명령된다.

- 라벨 이름은 63글자 미만으로

- yaml 예시

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: label-demo
    labels:
      job: engineer
      app: nginx
  spec:
    ...
  ```

- some important command

  ```shell
  # 라벨추가
  kubectl label pod <pod-name> env=prod
  
  # pod에 등록된 라벨 출력
  kubectl get pod --show-labels
  
  # 등록된 라벨 전체 출력
  kubectl get all -l env=prod
  
  # 특정 라벨 제외하고 출력
  kubectl get all -l env!=prod
  
  # and 조건 검색
  kubectl get all -l env=prod,tier=web
  
  ```

---

**Kubernetes .. CKA Exam Questions Challenge .. Part 1**

Q1. Create a new pod called admin-pod with image busybox. Allow the pod to be able to set system_time The container should sleep for 3200 seconds.

> Pod을 만드는데 command 옵션과 securityContext 이 추가된 pod을 만들어라.

- securityContext
  - **Pod** 또는 **Container**의 권한부여, 환경설정, 접근 제어를 제어하는 기능을 제공함.
    Container 프로세스들이 사용하는 사용자(runAsUser)와 그룹(fsGroup), 가용량, 권한 설정, 보안 정책(SELinux/AppArmor/Seccomp)을 설정하기 위해 사용됨
    **Pod의 Spec: 에 설정**되는 항목에 대한 권한을 설정함.

```shell
# yaml 파일 생성
kubectl run admin-pod --image=busybox --commad sleep 3200 --dry-run=client -o yaml > admin.yaml

# yaml 내용에 securityContext 추가
securityContext:
  capabilities:
    add: ["SYS_TIME"]
    
# yaml 파일 적용
kubectl apply -f admin.yaml
kubectl get pod
```

Q2. A kubeconfig file called `test.kubeconfig` has been create in `/root/TEST`. There is something wrong with the configuration. Troubleshoot and fix it.

```shell
cd TEST
cat test.kubeconfig
kubectl config view
# controlplane cluster port 가 6443 인지 확인 해라 
```

Q3. Create a new deployment called web-proj-268, with image nginx:1.16 and 1 replica. Next upgrade the deployment to version 1.17 using rolling update. Make sure that the version upgrade is recorded in the resource annotation.

```shell
# deployment 생성
kubectl create deployment web-proj-268 --image=nginx:1.16
kubectl get deployment
kubectl get pod
kubectl describe deployment web-proj-268

# deployment에 사용된 이미지 변경
kubectl set image deployment web-proj-268 nginx=nginx:1.17 --record
kubectl describe deployment web-proj-268 | grep -i image
kubectl rollout history deployment web-proj-268
```





