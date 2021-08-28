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
root@controlplane:~# kubectl create -f pod.yaml
pod/webapp created
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

Q6. ...