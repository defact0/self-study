### :ship: 스토리지

> 데이터 영속성(persistent)을 위한 저장소

- 저장소 제공(provisioning)
  - PersistentVolume / 데이터를 어떻게 제공할지에 대한 리소스 / 스토리지 생성
  - StorageClass / 관리자가 사용자들에게 제공하는 저장소 종류 (동적 저장소)
- 저장소 사용
  - PersistentVolumeClaim / 데이터를 어떻게 활용할 것인가에 대한 리소스 / 스토리지 활용

PersistentVolume (PV)

- 데이터 저장소 추상화 시킨 리소스
- 구체적인 저장소 정보
  - AWS = EBS(Elastic Block Storage)
  - GCP = PersistentDisk
  - 로컬 호스트 = Volume Path
- 각 환경에 따라 맞는 타입을 선택

hostPath PV

> - 클러스터 레벨의 리소스 (네임스페이스를 사용안함)
> - 상태 정보가 `Available`인 경우, 생성 후 사용하고 있지 않는 상태

```yaml
# PersistentVolume(hostPath) yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-volume
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp

# PersistentVolume(hostPath) create
kubectl apply -f PersistentVolume(hostPath).yaml

# Show PersistentVolume
kubectl get pv
```

- `storageClassName`  저장소 타입의 이름
- `capacity` 저장소의 크기
- `accessModes` 접근모드
  - `ReadWriteOnce` 동시에 1개의 Pod만 접근가능
- `hostPath` 호스트 서버에서 연결될 path

NFS PV

```yaml
apiVersion: v1
kind: PersistentVolume
metadat:
  name: my-nfs
spec:
  storageClassName: nfs
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: <NFS_SERVER_IP>
```

- `storageClassName` 저장소 타입의 이름
- `capacity` 저장소의 크기
- `accessModes` 접근모드
  - `ReadWriteMany` 동시 사용
- `mountOptions` NFS 서버와 마운트를 하기 위한 옵션
- `nfs` nfs 서버정보

awsElastickBlockStore PV

> AWS EBS 리소스를 요청
>
> - 적절한 권한이 부여된 환경에서 동작
> - 볼륨을 생성하고, <volume-id>를 입력 필요

```yaml
apiVersion: v1
kind: PersistentVolume
metadat:
  name: aws-ebs
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    volumeID: <volume-id>
    fsType: ext4
```

그외 다른 PersistentVolume

- azureDisk
- emptyDir
  - Pod와 생명주기를 같이하는 임시 저장소 / 같은 Pod 내 컨테이너들 끼리 정보를 주고받을 때 사용
- downward API
  - 쿠버네티스 리소스 메타 정보를 마운트하여 파일 처럼 읽을 수 있게 제공
- configMap
  - ConfigMap 리소스를 마치 PV 리소스 처럼 마운트 하여 사용

PersistentVolumeClaim (PVC)

> 사용자가 PV를 요청(claim)하는 리소스
>
> - PV의 `storageClassName`와 PVC의 `storageClassName` 이름이 매칭되어 연결된다.
>   - PV가 먼저 준비되어 있어야 한다.

```yaml
# my-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    request:
      storage: 1Gi

# my-pvc created
kubectl apply -f my-pvc.yaml

# Show my-pvc
kubectl get pvc
```

- `resources` 요청할 저장소 크기를 지정
- PVC 리소스 생성 이후에 PV 조회시 STATUS가 `Bound`으로 변경되어 있다.
  - 또한 CLAIM 항목에 my-pvc가 입력된 것을 확인할 수 있다.

```yaml
# use-pvc.yaml
apiVersion: v1
kind: Pod
metadata:
  name: use-pvc
spec:
  containers:
  - name: nginx
  image: nginx
  volumeMounts:
  - mountPath: /test-volume
    name: vol
volumes:
- name: vol
  persistentVolumeClaim:
    claimName: my-pvc
    
# use-pvc create
kubectl apply -f use-pvc.yaml

# test
kubectl exec use-pvc -- sh -c 'echo "hello" > /test-volume/hello.txt'
```

use-pvc 라는 Pod 생성을 통해 <u>Pod에 PVC 연결이 이루어 졌다.</u>
use-pvc 라는 Pod 를 삭제해도 hello.txt 파일은 계속 유지되고 있다.

> Node와 Pod의 생명주기가 다르기 때문에 PV, PVC가 등장하게 되었다.
>
> - Node = 지속적으로 유지, 인프라적인 성격(관리자가 작업해야 한다)
> - Pod  = 누구나 쉽게 생성/삭제가 가능
>
>  PV와 PVC 관계도 Node와 Pod와의 관계와 유사하다.

StorageClass

> 볼륨 생성을 기다릴 필요 없이 동적으로 데이터 저장소를 제공받을 수 있다.
>
> - 데이터 저장소 제공하는 부분을 자동화 시킨 것으로 생각하면된다.
> - PersistentVolume (PV)는 관리자가 직접 작업을 해야 데이터 저장소를 제공할 수 있다.
> - 클러스터 레벨의 리소스 / 네임스페이스를 지정하지 않는다.

- PVC 리소스 생성과 동일하며, STATUS가 `Pending` 상태로 되어 있어도 Pod에서 PVC를 사용하면 동적으로 볼륨이 생성된다.
- PV를 StorageClass가 대신 만들어 준다
  - 일반 사용자가 로컬 호스트 서버의 아무 위치나 디렉토리를 사용할 수 없게 제한 할 수 있다.
  - 사용자는 상세 인프라 정보를 알고있지 않아도 스토리지 자원을 이용할 수 있다.

NFS StorageClass

> 네트워크로 연결될 저장소인 NFS 볼륨을 동적으로 생성할 수 있게 만든다.
>
> - NFS 서버가 필요하다.
> - helm chart를 통해 손쉽게 NFS 서버 생성을 할 수 있다.

```shell
helm install nfs stable/nfs-server-provisioner \
   --set persistence.enabled=true \
   --set persistence.size=10Gi \
   --version 1.1.1 \
   --namespace ctrl
   
# 설치확인
kubectl get pod -n ctrl
kubectl get statefulset -n ctrl
kubectl get svc -n ctrl

# StatefulSet
# - 상태정보를 저장하는 application에서 사용하는 리소스
# - Deployment와 다른 점은 Pod의 순서와 고유성을 보장

# 새로운 nfs StorageClass 생성 확인
kubectl get sc

```

이렇게 하면 웹서버 Pod를 여러개 복제하고 동일한 html 디렉터리를 바라보게 하면 고가용 웹 서비스를 구축 할 수 있다.

MinIO 스토리지

- Object storage 이다. (= AWS의 S3 스토리지도 같은 종류)
- 오픈소스이고 쿠버네티스에서 동작하며 AWS S3 API와 호환된다.
