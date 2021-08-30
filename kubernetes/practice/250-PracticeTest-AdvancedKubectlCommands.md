Practice Test - Advanced Kubectl Commands

- https://uklabs.kodekloud.com/topic/practice-test-advanced-kubectl-commands-2/

---

Q1. Get the list of nodes in JSON format and store it in a file at `/opt/outputs/nodes.json`.

```shell
kubectl get nodes -o json > /opt/outputs/nodes.json
```

---

Q2.Get the details of the node `node01` in json format and store it in the file `/opt/outputs/node01.json`.

```shell
kubectl get node node01 -o json > /opt/outputs/node01.json
```

---

Q3. Use JSON PATH query to fetch node names and store them in `/opt/outputs/node_names.txt`.

```shell
# root@controlplane:~# kubectl get nodes -o=jsonpath='{.items[*].metadata.name}'
# controlplane
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}' > /opt/outputs/node_names.txt
```

---

Q4. Use JSON PATH query to retrieve the `osImages` of all the nodes and store it in a file `/opt/outputs/nodes_os.txt`.

- The `osImages` are under the `nodeInfo` section under `status` of each node.

```shell
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}' > /opt/outputs/nodes_os.txt
```

---

Q5. A kube-config file is present at `/root/my-kube-config`. Get the user names from it and store it in a file `/opt/outputs/users.txt`.

- Use the command `kubectl config view --kubeconfig=/root/my-kube-config` to view the custom kube-config.

```shell
kubectl config view --kubeconfig=my-kube-config -o jsonpath="{.users[*].name}" > /opt/outputs/users.txt
```

---

Q6. A set of Persistent Volumes are available. Sort them based on their capacity and store the result in the file `/opt/outputs/storage-capacity-sorted.txt`.

```shell
kubectl get pv --sort-by=.spec.capacity.storage > /opt/outputs/storage-capacity-sorted.txt
```

---

Q7. That was good, but we don't need all the extra details. Retrieve just the first 2 columns of output and store it in `/opt/outputs/pv-and-capacity-sorted.txt`.

- The columns should be named `NAME` and `CAPACITY`. Use the `custom-columns` option and remember, it should still be sorted as in the previous question.

```shell
kubectl get pv --sort-by=.spec.capacity.storage -o=custom-columns=NAME:.metadata.name,CAPACITY:.spec.capacity.storage > /opt/outputs/pv-and-capacity-sorted.txt
```

---

Q8.Use a JSON PATH query to identify the context configured for the `aws-user` in the `my-kube-config` context file and store the result in `/opt/outputs/aws-context-name`.

```shell
kubectl config view --kubeconfig=my-kube-config -o jsonpath="{.contexts[?(@.context.user=='aws-user')].name}" > /opt/outputs/aws-context-name
```



