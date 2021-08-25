Practice Test - Certificates API

- https://uklabs.kodekloud.com/topic/practice-test-certificates-api-2/

---

Q1. A new member `akshay` joined our team. He requires access to our cluster. The Certificate Signing Request is at the `/root` location.

- ok

---

Q2. Create a **CertificateSigningRequest** object with the name `akshay` with the contents of the `akshay.csr` file

- CSR akshay created
- Right CSR is used

```shell
#
# vi csr.yaml
#
---
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: akshay
spec:
  groups:
  - system:authenticated
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQXY4azZTTE9HVzcrV3JwUUhITnI2TGFROTJhVmQ1blNLajR6UEhsNUlJYVdlCmJ4RU9JYkNmRkhKKzlIOE1RaS9hbCswcEkwR2xpYnlmTXozL2lGSWF3eGVXNFA3bDJjK1g0L0lqOXZQVC9jU3UKMDAya2ZvV0xUUkpQbWtKaVVuQTRpSGxZNDdmYkpQZDhIRGFuWHM3bnFoenVvTnZLbWhwL2twZUVvaHd5MFRVMAo5bzdvcjJWb1hWZTVyUnNoMms4dzV2TlVPL3BBdEk4VkRydUhCYzRxaHM3MDI1ZTZTUXFDeHUyOHNhTDh1blJQCkR6V2ZsNVpLcTVpdlJNeFQrcUo0UGpBL2pHV2d6QVliL1hDQXRrRVJyNlMwak9XaEw1Q0ErVU1BQmd5a1c5emQKTmlXbnJZUEdqVWh1WjZBeWJ1VzMxMjRqdlFvbndRRUprNEdoayt2SU53SURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBQi94dDZ2d2EweWZHZFpKZ1k2ZDRUZEFtN2ZiTHRqUE15OHByTi9WZEdxN25oVDNUUE5zCjEwRFFaVGN6T21hTjVTZmpTaVAvaDRZQzQ0QjhFMll5Szg4Z2lDaUVEWDNlaDFYZnB3bnlJMVBDVE1mYys3cWUKMkJZTGJWSitRY040MDU4YituK24wMy9oVkN4L1VRRFhvc2w4Z2hOaHhGck9zRUtuVExiWHRsK29jQ0RtN3I3UwpUYTFkbWtFWCtWUnFJYXFGSDd1dDJveHgxcHdCdnJEeGUvV2cybXNqdHJZUXJ3eDJmQnErQ2Z1dm1sVS9rME4rCml3MEFjbVJsMy9veTdqR3ptMXdqdTJvNG4zSDNKQ25SbE41SnIyQkZTcFVQU3dCL1lUZ1ZobHVMNmwwRERxS3MKNTdYcEYxcjZWdmJmbTRldkhDNnJCSnNiZmI2ZU1KejZPMUU9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
  
  
#
# csr.yaml created
#
root@controlplane:~# kubectl apply -f csr.yaml 
certificatesigningrequest.certificates.k8s.io/akshay created
```

---

Q3. What is the Condition of the newly created Certificate Signing Request object?

```shell
root@controlplane:~# kubectl get csr
NAME        AGE    SIGNERNAME                                    REQUESTOR                  CONDITION
akshay      116s   kubernetes.io/kube-apiserver-client           kubernetes-admin           Pending
csr-l92xq   10m    kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   Approved,Issued
```

- `Pending`

---

Q4. Approve the CSR Request

```shell
#
# certificate approve akshay
#
root@controlplane:~# kubectl certificate approve akshay
certificatesigningrequest.certificates.k8s.io/akshay approved

#
# get csr
#
root@controlplane:~# kubectl get csr
NAME        AGE     SIGNERNAME                                    REQUESTOR                  CONDITION
akshay      2m45s   kubernetes.io/kube-apiserver-client           kubernetes-admin           Approved,Issued
csr-l92xq   11m     kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   Approved,Issued
```

---

Q5. How many CSR requests are available on the cluster?

```shell
root@controlplane:~# kubectl get csr
NAME        AGE     SIGNERNAME                                    REQUESTOR                  CONDITION
akshay      2m45s   kubernetes.io/kube-apiserver-client           kubernetes-admin           Approved,Issued
csr-l92xq   11m     kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   Approved,Issued
```

- 2

---

Q6. During a routine check you realized that there is a new CSR request in place. What is the name of this request?

```shell
root@controlplane:~# kubectl get csr
NAME          AGE     SIGNERNAME                                    REQUESTOR                  CONDITION
agent-smith   15s     kubernetes.io/kube-apiserver-client           agent-x                    Pending
akshay        4m21s   kubernetes.io/kube-apiserver-client           kubernetes-admin           Approved,Issued
csr-l92xq     12m     kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   Approved,Issued
```

- `agent-smith`

---

Q7. Hmmm.. You are not aware of a request coming in. What groups is this CSR requesting access to?

- Check the details about the request. Preferebly in YAML.

```shell
root@controlplane:~# kubectl get csr agent-smith -o yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  creationTimestamp: "2021-08-24T21:06:32Z"
  managedFields:
  - apiVersion: certificates.k8s.io/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:spec:
        f:groups: {}
        f:request: {}
        f:signerName: {}
        f:usages: {}
    manager: kubectl-create
    operation: Update
    time: "2021-08-24T21:06:32Z"
  name: agent-smith
  resourceVersion: "1388"
  uid: 24ff11ca-aea0-471a-b029-4fc787ef88e0
spec:
  groups:
  - system:masters
  - system:authenticated
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1dEQ0NBVUFDQVFBd0V6RVJNQThHQTFVRUF3d0libVYzTFhWelpYSXdnZ0VpTUEwR0NTcUdTSWIzRFFFQgpBUVVBQTRJQkR3QXdnZ0VLQW9JQkFRRE8wV0pXK0RYc0FKU0lyanBObzV2UklCcGxuemcrNnhjOStVVndrS2kwCkxmQzI3dCsxZUVuT041TXVxOTlOZXZtTUVPbnJEVU8vdGh5VnFQMncyWE5JRFJYall5RjQwRmJtRCs1eld5Q0sKeTNCaWhoQjkzTUo3T3FsM1VUdlo4VEVMcXlhRGtuUmwvanYvU3hnWGtvazBBQlVUcFdNeDRCcFNpS2IwVSt0RQpJRjVueEF0dE1Wa0RQUTdOYmVaUkc0M2IrUVdsVkdSL3o2RFdPZkpuYmZlek90YUF5ZEdMVFpGQy93VHB6NTJrCkVjQ1hBd3FDaGpCTGt6MkJIUFI0Sjg5RDZYYjhrMzlwdTZqcHluZ1Y2dVAwdEliT3pwcU52MFkwcWRFWnB3bXcKajJxRUwraFpFV2trRno4MGxOTnR5VDVMeE1xRU5EQ25JZ3dDNEdaaVJHYnJBZ01CQUFHZ0FEQU5CZ2txaGtpRwo5dzBCQVFzRkFBT0NBUUVBUzlpUzZDMXV4VHVmNUJCWVNVN1FGUUhVemFsTnhBZFlzYU9SUlFOd0had0hxR2k0CmhPSzRhMnp5TnlpNDRPT2lqeWFENnRVVzhEU3hrcjhCTEs4S2czc3JSRXRKcWw1ckxaeTlMUlZyc0pnaEQ0Z1kKUDlOTCthRFJTeFJPVlNxQmFCMm5XZVlwTTVjSjVURjUzbGVzTlNOTUxRMisrUk1uakRRSjdqdVBFaWM4L2RoawpXcjJFVU02VWF3enlrcmRISW13VHYybWxNWTBSK0ROdFYxWWllKzBIOS9ZRWx0K0ZTR2poNUw1WVV2STFEcWl5CjRsM0UveTNxTDcxV2ZBY3VIM09zVnBVVW5RSVNNZFFzMHFXQ3NiRTU2Q0M1RGhQR1pJcFVibktVcEF3a2ErOEUKdndRMDdqRytocGtueG11RkFlWHhnVXdvZEFMYUo3anUvVERJY3c9PQotLS0tLUVORCBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0K
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - digital signature
  - key encipherment
  - server auth
  username: agent-x
status: {}
```

- `spec.groups` 부분을 보면 `system:masters`을 확인 할 수 있다.

---

Q8. That doesn't look very right. Reject that request.

```shell
root@controlplane:~# kubectl certificate deny agent-smith
certificatesigningrequest.certificates.k8s.io/agent-smith denied
```

---

Q9. Let's get rid of it. Delete the new CSR object

```shell
root@controlplane:~# kubectl delete csr agent-smith
certificatesigningrequest.certificates.k8s.io "agent-smith" deleted
```

