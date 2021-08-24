Practice Test - Backup and Restore Methods

- https://uklabs.kodekloud.com/topic/practice-test-backup-and-restore-methods-2/

---

Q1. We have a working kubernetes cluster with a set of applications running. Let us first explore the setup.

- How many deployments exist in the cluster?

```shell
root@controlplane:~# kubectl get deployments
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
blue   3/3     3            3           77s
red    2/2     2            2           77s
```

- 2

---

Q2. What is the version of ETCD running on the cluster?

- Check the ETCD Pod or Process

```shell
#
# etcd Version
#
root@controlplane:~# kubectl -n kube-system logs etcd-controlplane | grep -i 'etcd Version'
2021-08-24 07:18:07.960652 I | etcdmain: etcd Version: 3.4.13

#
# Image
#
root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep Image:
    Image:         k8s.gcr.io/etcd:3.4.13-0
root@controlplane:~# 
```

- `3.4.13`

---

Q3. At what address can you reach the ETCD cluster from the controlplane node?

- Check the ETCD Service configuration in the ETCD POD

```shell
root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep '\--listen-client-urls'
      --listen-client-urls=https://127.0.0.1:2379,https://10.10.228.3:2379
```

- `https://127.0.0.1:2379`

---

Q4. Where is the ETCD server certificate file located?

- Note this path down as you will need to use it later

```shell
root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep '\--cert-file'
      --cert-file=/etc/kubernetes/pki/etcd/server.crt
```

- `/etc/kubernetes/pki/etcd/server.crt`

---

Q5. Where is the ETCD CA Certificate file located?

- Note this path down as you will need to use it later.

```shell
root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep '\--trusted-ca-file'
      --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```

- `/etc/kubernetes/pki/etcd/ca.crt`

---

Q6. The master nodes in our cluster are planned for a regular maintenance reboot tonight. While we do not anticipate anything to go wrong, we are required to take the necessary backups. Take a snapshot of the **ETCD** database using the built-in **snapshot** functionality.

- Store the backup file at location /opt/snapshot-pre-boot.db
  - Backup ETCD to /opt/snapshot-pre-boot.db

```shell
#
# /opt/snapshot-pre-boot.db 백업 이전
#
root@controlplane:~# cd /opt/
root@controlplane:/opt# ls
cni  containerd

#
# /opt/snapshot-pre-boot.db 백업 이후
#
root@controlplane:/opt# ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 \
> --cacert=/etc/kubernetes/pki/etcd/ca.crt \
> --cert=/etc/kubernetes/pki/etcd/server.crt \
> --key=/etc/kubernetes/pki/etcd/server.key \
> snapshot save /opt/snapshot-pre-boot.db
Snapshot saved at /opt/snapshot-pre-boot.db

#
# /opt/snapshot-pre-boot.db 백업 확인
#
root@controlplane:/opt# ls
cni  containerd  snapshot-pre-boot.db
root@controlplane:/opt# 
```

---

Q7. Great! Let us now wait for the maintenance window to finish. Go get some sleep. (Don't go for real)

- ok

---

Q8. Wake up! We have a conference call! After the reboot the master nodes came back online, but none of our applications are accessible. Check the status of the applications on the cluster. What's wrong?

- `All of the above`

---

Q9. Luckily we took a backup. Restore the original state of the cluster using the backup file.

- Deployments: 2
- Services: 3

```shell
#
# First Restore the snapshot:
#
root@controlplane:/opt# ETCDCTL_API=3 etcdctl  --data-dir /var/lib/etcd-from-backup \
> snapshot restore /opt/snapshot-pre-boot.db
2021-08-24 07:35:50.095289 I | etcdserver/membership: added member 8e9e05c52164694d [http://localhost:2380] to cluster cdf818194e3a8c32


#
# Next, update the /etc/kubernetes/manifests/etcd.yaml:
#  - 맨 마지막 부분에 name: etcd-data 항목을 수정하면된다.
#
root@controlplane:~# vi /etc/kubernetes/manifests/etcd.yaml

  volumes:
  - hostPath:
      path: /var/lib/etcd-from-backup
      type: DirectoryOrCreate
    name: etcd-data


#
# kubectl get all
#
root@controlplane:~# kubectl get all
NAME                        READY   STATUS    RESTARTS   AGE
pod/blue-746c87566d-2wv5d   1/1     Running   0          23m
pod/blue-746c87566d-9svxb   1/1     Running   0          23m
pod/blue-746c87566d-hgxpj   1/1     Running   0          23m
pod/red-75f847bf79-bkgq7    1/1     Running   0          23m
pod/red-75f847bf79-gclh9    1/1     Running   0          23m

NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/blue-service   NodePort    10.98.66.55      <none>        80:30082/TCP   23m
service/kubernetes     ClusterIP   10.96.0.1        <none>        443/TCP        26m
service/red-service    NodePort    10.102.109.250   <none>        80:30080/TCP   23m

NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/blue   3/3     3            3           23m
deployment.apps/red    2/2     2            2           23m

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/blue-746c87566d   3         3         3       23m
replicaset.apps/red-75f847bf79    2         2         2       23m
```

> Note: as the ETCD pod has changed it will automatically restart, and also kube-controller-manager and kube-scheduler. Wait 1-2 to mins for this pods to restart. You can run a `watch "docker ps | grep etcd"` command to see when the ETCD pod is restarted.
>
> Note2: If the etcd pod is not getting `Ready 1/1`, then restart it by `kubectl delete pod -n kube-system etcd-controlplane` and wait 1 minute.
>
> Note3: This is the simplest way to make sure that ETCD uses the restored data after the ETCD pod is recreated. You **don't** have to change anything else.

