Practice Test - Monitoring

- https://uklabs.kodekloud.com/topic/practice-test-monitor-cluster-components-2/

---

Q1. We have deployed a few PODs running workloads. Inspect them.

- Wait for the pods to be ready before proceeding to the next question.

```shell
root@controlplane:~# kubectl get pod
NAME       READY   STATUS    RESTARTS   AGE
elephant   1/1     Running   0          108s
lion       1/1     Running   0          108s
rabbit     1/1     Running   0          108s
```

---

Q2. Let us deploy metrics-server to monitor the PODs and Nodes. Pull the git repository for the deployment files.

- Run: `git clone https://github.com/kodekloudhub/kubernetes-metrics-server.git`

```shell
root@controlplane:~# ls
sample.yaml
root@controlplane:~# git clone https://github.com/kodekloudhub/kubernetes-metrics-server.git
Cloning into 'kubernetes-metrics-server'...
remote: Enumerating objects: 24, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 24 (delta 4), reused 0 (delta 0), pack-reused 12
Unpacking objects: 100% (24/24), done.
root@controlplane:~# ls
kubernetes-metrics-server  sample.yaml
root@controlplane:~# cd kubernetes-metrics-server/
root@controlplane:~/kubernetes-metrics-server# ls
README.md                       auth-delegator.yaml  metrics-apiservice.yaml         metrics-server-service.yaml
aggregated-metrics-reader.yaml  auth-reader.yaml     metrics-server-deployment.yaml  resource-reader.yaml
root@controlplane:~/kubernetes-metrics-server# 
```

---

Q3. Deploy the metrics-server by creating all the components downloaded.

- Run the `kubectl create -f .` command from within the downloaded repository.
- Metrics server deployed?

```shell
# ------------------------------------------------
# kubernetes-metrics-server directory
# ------------------------------------------------
root@controlplane:~/kubernetes-metrics-server# ls
README.md                       auth-delegator.yaml  metrics-apiservice.yaml         metrics-server-service.yaml
aggregated-metrics-reader.yaml  auth-reader.yaml     metrics-server-deployment.yaml  resource-reader.yaml

# ------------------------------------------------
# kubectl create -f .
# ------------------------------------------------
root@controlplane:~/kubernetes-metrics-server# kubectl create -f .
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
serviceaccount/metrics-server created
deployment.apps/metrics-server created
service/metrics-server created
clusterrole.rbac.authorization.k8s.io/system:metrics-server created
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created
root@controlplane:~/kubernetes-metrics-server# 
```

---

Q4. It takes a few minutes for the metrics server to start gathering data.

- Run the `kubectl top node` command and wait for a valid output.

```shell
root@controlplane:~/kubernetes-metrics-server# kubectl top node
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
controlplane   385m         0%     1304Mi          0%        
node01         84m          0%     392Mi           0%     
```

---

Q5. Identify the node that consumes the `most` CPU.

```shell
root@controlplane:~# kubectl top node
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
controlplane   400m         0%     1262Mi          0%        
node01         67m          0%     394Mi           0%        

root@controlplane:~# kubectl top node --sort-by='cpu'
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
controlplane   411m         0%     1263Mi          0%        
node01         80m          0%     395Mi           0%        

root@controlplane:~# kubectl top node --sort-by='cpu' --no-headers
controlplane   397m   0%    1264Mi   0%    
node01         67m    0%    395Mi    0%    

root@controlplane:~# kubectl top node --sort-by='cpu' --no-headers | head -1
controlplane   432m   0%    1264Mi   0%    
```

- `controlplane`

---

Q6. Identify the node that consumes the `most` Memory.

```shell
root@controlplane:~# kubectl top node --sort-by='memory' --no-headers | head -1
controlplane   461m   0%    1264Mi   0%    
```

- `controlplane`

---

Q7. Identify the POD that consumes the `most` Memory.

```shell
root@controlplane:~# kubectl top pod --sort-by='memory' --no-headers | head -1
rabbit     158m   252Mi 
```

- `rabbit`

---

Q8. Identify the POD that consumes the `least` CPU.

```shell
root@controlplane:~# kubectl top pod --sort-by='cpu' --no-headers | tail -1
lion       1m     18Mi 
```

- `lion`