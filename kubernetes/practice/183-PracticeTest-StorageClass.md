Practice Test - Storage Class

- https://uklabs.kodekloud.com/topic/practice-test-storage-class-3/

---

Q1. How many `StorageClasses` exist in the cluster right now?

```shell
root@controlplane:~# kubectl get sc
No resources found
```

- `0`

---

Q2. How about now? How many Storage Classes exist in the cluster?

- We just created a few new Storage Classes. Inspect them.

```shell
root@controlplane:~# kubectl get sc
NAME                        PROVISIONER                     RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-storage               kubernetes.io/no-provisioner    Delete          WaitForFirstConsumer   false                  19s
portworx-io-priority-high   kubernetes.io/portworx-volume   Delete          Immediate              false                  19s
root@controlplane:~#
```

- `2`개의 스토리지 클래스가 존재

---

Q3. What is the name of the `Storage Class` that does not support `dynamic` volume provisioning?

> 로컬 스토리지 클래스는 비프로비저닝을 사용하며 동적 프로비저닝을 지원하지 않는다.

- `local-storage`

---

 Q4. What is the `Volume Binding Mode` used for this storage class (the one identified in the previous question).

```shell
root@controlplane:~# kubectl describe sc local-storage
Name:            local-storage
IsDefaultClass:  No
Annotations:     kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"local-storage"},"provisioner":"kubernetes.io/no-provisioner","volumeBindingMode":"WaitForFirstConsumer"}

Provisioner:           kubernetes.io/no-provisioner
Parameters:            <none>
AllowVolumeExpansion:  <unset>
MountOptions:          <none>
ReclaimPolicy:         Delete
VolumeBindingMode:     WaitForFirstConsumer   <--------여기부분을 확인
Events:                <none>
```

- `WaitForFirstConsumer`

----

Q5. What is the `Provisioner` used for the storage class called `portworx-io-priority-high`?

```shell
root@controlplane:~# kubectl describe sc portworx-io-priority-high
Name:            portworx-io-priority-high
IsDefaultClass:  No
Annotations:     kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"portworx-io-priority-high"},"parameters":{"priority_io":"high","repl":"1","snap_interval":"70"},"provisioner":"kubernetes.io/portworx-volume"}

Provisioner:           kubernetes.io/portworx-volume    <---- 여기부분을 확인
Parameters:            priority_io=high,repl=1,snap_interval=70
AllowVolumeExpansion:  <unset>
MountOptions:          <none>
ReclaimPolicy:         Delete
VolumeBindingMode:     Immediate
Events:                <none>
root@controlplane:~#
```

- `portworx-volume`

---

Q6. Is there a `PersistentVolumeClaim` that is consuming the `PersistentVolume` called `local-pv`?

```shell
root@controlplane:~# kubectl get pvc
No resources found in default namespace.
```

- `No`

---

Q7. Let's fix that. Create a new `PersistentVolumeClaim` by the name of `local-pvc` that should bind to the volume `local-pv`.

- Inspect the pv `local-pv` for the specs.
  - PVC: local-pvc
  - Correct Access Mode?
  - Correct StorageClass Used?
  - PVC requests volume size = 500Mi?

```shell
cat << EOF | kubectl apply -f -
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: local-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 500Mi
EOF
```

---

Q8. What is the status of the newly created Persistent Volume Claim?

```shell
root@controlplane:~# kubectl get pvc local-pvc
NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS    AGE
local-pvc   Pending                                      local-storage   38s
```

- `Pending`

---

Q9. Why is the PVC in a pending state despite making a valid request to claim the volume called `local-pv`?

- Inspect the PVC events.

```shell
root@controlplane:~# kubectl describe pvc local-pvc | grep -A3 Events
Events:
  Type    Reason                Age                  From                         Message
  ----    ------                ----                 ----                         -------
  Normal  WaitForFirstConsumer  9s (x12 over 2m43s)  persistentvolume-controller  waiting for first consumer to be created before binding
```

- `A Pod consuming the volume is not scheduled`

---

Q10. The Storage Class called `local-storage` makes use of `VolumeBindingMode` set to `WaitForFirstConsumer`. This will delay the binding and provisioning of a PersistentVolume until a Pod using the PersistentVolumeClaim is created.

- ok

----

Q11. Create a new pod called `nginx` with the image `nginx:alpine`. The Pod should make use of the PVC `local-pvc` and mount the volume at the path `/var/www/html`.

- The PV `local-pv` should in a bound state.
  - Pod created with the correct Image?
  - Pod uses PVC called local-pvc?
  - local-pv bound?
  - nginx pod running?
  - Volume mounted at the correct path?

```shell
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    volumeMounts:
      - name: local-persistent-storage
        mountPath: /var/www/html
  volumes:
    - name: local-persistent-storage
      persistentVolumeClaim:
        claimName: local-pvc
EOF
```

---

Q12. What is the status of the `local-pvc` Persistent Volume Claim now?

```shell
root@controlplane:~# kubectl get pvc
NAME        STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS    AGE
local-pvc   Bound    local-pv   500Mi      RWO            local-storage   7m19s
```

- `Bound`

---

Q13. Create a new Storage Class called `delayed-volume-sc` that makes use of the below specs:

- `provisioner`: kubernetes.io/no-provisioner
  `volumeBindingMode`: WaitForFirstConsumer
  - 
    Storage Class uses: kubernetes.io/no-provisioner ?
  - Storage Class volumeBindingMode set to WaitForFirstConsumer ?

```shell
# ---------------------------------------------
# apply StorageClass
cat << EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: delayed-volume-sc
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF

# ---------------------------------------------
# get StorageClass
root@controlplane:~# kubectl get sc
NAME                        PROVISIONER                     RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
delayed-volume-sc           kubernetes.io/no-provisioner    Delete          WaitForFirstConsumer   false                  8s
local-storage               kubernetes.io/no-provisioner    Delete          WaitForFirstConsumer   false                  10m
portworx-io-priority-high   kubernetes.io/portworx-volume   Delete          Immediate              false                  10m
```

