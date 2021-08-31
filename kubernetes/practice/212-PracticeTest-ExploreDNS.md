Practice Test - Explore DNS

- https://uklabs.kodekloud.com/topic/practice-test-coredns-in-kubernetes-2/

---

Q1. Identify the DNS solution implemented in this cluster.

```shell
root@controlplane:~# kubectl get pods -n kube-system
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-74ff55c5b-hzqwj                1/1     Running   0          8m53s
coredns-74ff55c5b-mgk56                1/1     Running   0          8m53s
```

- `CoreDNS`

---

Q2. How many pods of the DNS server are deployed?

```shell
root@controlplane:~# kubectl get deploy -n kube-system
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
coredns   2/2     2            2           10m
```

- `2`

---

Q3. What is the name of the service created for accessing CoreDNS?

```shell
root@controlplane:~# kubectl get service -n kube-system
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   10m
```

- `kube-dns`

---

Q4. What is the IP of the CoreDNS server that should be configured on PODs to resolve services?

- `10.96.0.10`

---

Q5. Where is the configuration file located for configuring the CoreDNS service?

```shell
root@controlplane:~# kubectl -n kube-system describe deployments.apps coredns | grep -A2 Args | grep Corefile
      /etc/coredns/Corefile
```

- `/etc/coredns/Corefile`

---

Q6. How is the Corefile passed in to the CoreDNS POD?

```shell
# configmap = cm
root@controlplane:~# kubectl get cm -n kube-system
NAME                                 DATA   AGE
coredns                              1      12m
extension-apiserver-authentication   6      12m
kube-flannel-cfg                     2      12m
kube-proxy                           2      12m
kube-root-ca.crt                     1      12m
kubeadm-config                       2      12m
kubelet-config-1.20                  1      12m
```

- `Configured as a ConfigMap object`

---

Q7. What is the name of the ConfigMap object created for Corefile?

- `coredns`

---

Q8. What is the root domain/zone configured for this kubernetes cluster?

```shell
root@controlplane:~# kubectl describe configmap coredns -n kube-system
Name:         coredns
Namespace:    kube-system
Labels:       <none>
Annotations:  <none>

Data
====
Corefile:
----
.:53 {
    errors
    health {
       lameduck 5s
    }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {  <------ 여기...
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf {
       max_concurrent 1000
    }
    cache 30
    loop
    reload
    loadbalance
}

Events:  <none>
```

- `cluster.local`

---

Q9. We have deployed a set of PODs and Services in the `default` and `payroll` namespaces. Inspect them and go to the next question.

- ok

---

Q10. What name can be used to access the `hr` web server from the `test` Application?
You can execute a curl command on the `test` pod to test. Alternatively, the test Application also has a UI. Access it using the tab at the top of your terminal named `test-app`.

```shell
root@controlplane:~# kubectl get svc
NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes     ClusterIP   10.96.0.1        <none>        443/TCP        16m
test-service   NodePort    10.109.192.107   <none>        80:30080/TCP   8m57s
web-service    ClusterIP   10.110.13.60     <none>        80/TCP         8m57s
```

- `web-service`

---

Q11. Which of the names CANNOT be used to access the HR service from the test pod?

- `web-serivce.default.pod`

---

Q12. Which of the below name can be used to access the `payroll` service from the test application?

- `web-service.payroll`

---

Q13. Which of the below name CANNOT be used to access the `payroll` service from the test application?

- `web-service.payroll.svc.cluster`

---

Q14. We just deployed a web server - `webapp` - that accesses a database `mysql` - server. However the web server is failing to connect to the database server. Troubleshoot and fix the issue.
They could be in different namespaces. First locate the applications. The web server interface can be seen by clicking the tab `Web Server` at the top of your terminal.

- Web Server: webapp
- Uses the right DB_Host name

```shell
kubectl edit deploy webapp

#Search for DB_Host and Change the DB_Host from mysql to mysql.payroll

spec:
  containers:
  - env:
    - name: DB_Host
      value: mysql.payroll
```



---

Q15. From the `hr` pod `nslookup` the `mysql` service and redirect the output to a file `/root/CKA/nslookup.out`

```shell
kubectl exec -it hr -- nslookup mysql.payroll > /root/CKA/nslookup.out
```

