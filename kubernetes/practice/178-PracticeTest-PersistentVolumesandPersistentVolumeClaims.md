Practice Test - Persistent Volumes and Persistent Volume Claims

- https://uklabs.kodekloud.com/topic/practice-test-persistent-volume-claims-2/

---

Q1. We have deployed a POD. Inspect the POD and wait for it to start running.

- ok

---

Q2. The application stores logs at location `/log/app.log`. View the logs.

```shell
kubectl exec webapp -- cat /log/app.log
```

---

Q3. If the POD was to get deleted now, would you be able to view these logs.

- No

---

Q4. Configure a volume to store these logs at `/var/log/webapp` on the host.

- Name: webapp
- Image Name: kodekloud/event-simulator
- Volume HostPath: /var/log/webapp
- Volume Mount: /log

```shell
# -------------------------------------------
# 기존 Pod 삭제
root@controlplane:~# kubectl delete pod webapp
pod "webapp" deleted

# -------------------------------------------
# Pod 생성
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: webapp
spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator
    env:
    - name: LOG_HANDLERS
      value: file
    volumeMounts:
    - mountPath: /log
      name: log-volume

  volumes:
  - name: log-volume
    hostPath:
      # directory location on host
      path: /var/log/webapp
      # this field is optional
      type: Directory
EOF

# -------------------------------------------
# Pod 확인
root@controlplane:~# kubectl get pod
NAME     READY   STATUS    RESTARTS   AGE
webapp   1/1     Running   0          25s
```

---

Q5. Create a `Persistent Volume` with the given specification.

- Volume Name: pv-log
- Storage: 100Mi
- Access Modes: ReadWriteMany
- Host Path: /pv/log
- Reclaim Policy: Retain

```shell
# -------------------------------------------
# PV 생성
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /pv/log
EOF

# -------------------------------------------
# PV 확인
root@controlplane:~# kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   
pv-log   100Mi      RWX            Retain           Available
```

---

Q6. Let us claim some of that storage for our application. Create a `Persistent Volume Claim` with the given specification.

- Volume Name: claim-log-1
- Storage Request: 50Mi
- Access Modes: ReadWriteOnce

```shell
# -------------------------------------------
# PVC 생성
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-log-1
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Mi
EOF
      
# -------------------------------------------
# PVC 확인
root@controlplane:~# kubectl get pvc
NAME          STATUS    VOLUME   CAPACITY   
claim-log-1   Pending                       
```

---

Q7. What is the state of the `Persistent Volume Claim`?

- `Pending`

---

Q8. What is the state of the `Persistent Volume`?

- `Available`
  - kubectl get pv명령으로 확인하면 된다.

---

Q9. Why is the claim not bound to the available `Persistent Volume`?

```shell
root@controlplane:~# kubectl get pv,pvc
NAME                      CAPACITY   ACCESS MODES   RECLAIM POLICY
persistentvolume/pv-log   100Mi      RWX            Retain        

NAME                                STATUS    ACCESS MODES
persistentvolumeclaim/claim-log-1   Pending               
```

- ACCESS MODES 가 일치하지 않음
  - 그래서 정답은 `Access Modes Mismatch` 가 된다.

---

Q10. Update the Access Mode on the claim to bind it to the PV.
Delete and recreate the `claim-log-1`.

- Volume Name: claim-log-1
- Storage Request: 50Mi
- PVol: pv-log
- Status: Bound

```shell


# ----------------------------------
# pvc claim-log-1 삭제
root@controlplane:~# kubectl delete pvc claim-log-1
persistentvolumeclaim "claim-log-1" deleted

# ----------------------------------
# pvc claim-log-1 재생성
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-log-1
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 50Mi
EOF


# ----------------------------------
# pvc claim-log-1 삭제
root@controlplane:~# kubectl get pvc
NAME          STATUS   VOLUME   CAPACITY   ACCESS MODES
claim-log-1   Bound    pv-log   100Mi      RWX         
```

- `spec.accessModes`의 값을 `ReadWriteMany`으로 설정 후 PVC를 생성하면 PV와 정상적으로 연결되어 상태가 `Bound`인 것을 확인 할 수 있다.

---

Q11. You requested for `50Mi`, how much capacity is now available to the PVC?

```shell
root@controlplane:~# kubectl get pvc
NAME          STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
claim-log-1   Bound    pv-log   100Mi      RWX                           115s
```

- 현재 요청 가능한 `CAPACITY`는 `100Mi`  이다.

---

Q12. Update the `webapp` pod to use the persistent volume claim as its storage.
Replace `hostPath` configured earlier with the newly created `PersistentVolumeClaim`.

- Name: webapp
- Image Name: kodekloud/event-simulator
- Volume: PersistentVolumeClaim=claim-log-1
- Volume Mount: /log

```shell
# -------------------------------------
# 현재 실행하고 있는 webapp POD를 수정해라
root@controlplane:~# kubectl get pod
NAME     READY   STATUS    RESTARTS   AGE
webapp   1/1     Running   0          16m

# -------------------------------------
# webapp 삭제
root@controlplane:~# kubectl delete pod webapp 
pod "webapp" deleted

# -------------------------------------
# pod/webapp created
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: webapp
spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator
    env:
    - name: LOG_HANDLERS
      value: file
    volumeMounts:
    - mountPath: /log
      name: log-volume

  volumes:
  - name: log-volume
    persistentVolumeClaim:
      claimName: claim-log-1
EOF
      

# -------------------------------------
# pod 확인
root@controlplane:~# kubectl get pod
NAME     READY   STATUS    RESTARTS   AGE
webapp   1/1     Running   0          21s
```

---

Q13. What is the `Reclaim Policy` set on the Persistent Volume `pv-log`?

```shell
root@controlplane:~# kubectl describe pv pv-log 
Name:            pv-log
Labels:          <none>
Annotations:     pv.kubernetes.io/bound-by-controller: yes
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    
Status:          Bound
Claim:           default/claim-log-1
Reclaim Policy:  Retain
Access Modes:    RWX
VolumeMode:      Filesystem
Capacity:        100Mi
Node Affinity:   <none>
Message:         
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /pv/log
    HostPathType:  
Events:            <none>
```

- Reclaim Policy:  `Retain`

---

Q14. What would happen to the PV if the PVC was destroyed?

- The PV is not deleted but not available

---

Q15. Try deleting the PVC and notice what happens.

```shell
# -----------------------------------------------------
# Try deleting the PVC
root@controlplane:~# kubectl delete pvc claim-log-1 
persistentvolumeclaim "claim-log-1" deleted

# -----------------------------------------------------
# get pvc
root@controlplane:~# kubectl get pvc
NAME          STATUS        VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
claim-log-1   Terminating   pv-log   100Mi      RWX                           14m

```

- `The PVC is stuck in 'terminating' state`

---

Q16. Why is the PVC stuck in `Terminating` state?

- `The PVC is being used by a POD`

---

Q17. Let us now delete the `webapp` Pod.

- Once deleted, wait for the pod to fully terminate.
- Name: webapp

```shell
root@controlplane:~# kubectl delete pod webapp 
pod "webapp" deleted

root@controlplane:~# kubectl get pod,pvc
No resources found in default namespace.
```

---

Q18. What is the state of the PVC now?

- `deleted`

---

Q19. What is the state of the Persistent Volume now?

- `Released`

```shell
root@controlplane:~# kubectl get pod,pvc,pv
NAME                      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                 STORAGECLASS   REASON   AGE
persistentvolume/pv-log   100Mi      RWX            Retain           Released   default/claim-log-1                           34m
```

