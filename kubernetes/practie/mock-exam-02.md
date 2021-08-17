Mock Exam - 2

- Mock Test Link - https://uklabs.kodekloud.com/topic/mock-exam-2-4/
- https://github.com/kodekloudhub/certified-kubernetes-administrator-course



Tip

- 시험 터미널에 붙여 넣기 단축키 
  - <shift> + <insert>
- 치트시트 [링크](https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/)



Solution

1. Take a backup of the etcd cluster and save it to `/opt/etcd-backup.db`.

   - Backup Completed

   > etcd 클러스터를 백업하고 요구하는 경로에 저장해라
   >
   > - 공식 홈페이지에 검색하여 참고하자 ([링크](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#snapshot-using-etcdctl-options))

   ```shell
   # 솔루션 영상에서 나온 /etc/kubernetes/manifests/etcd.yaml 파일내용이랑 시뮬레이션이랑 내용이 다르다
   cat /etc/kubernetes/manifests/etcd.yaml
   
   spec:
     containers:
     - command:
       - etcd
       - --cert-file=/etc/kubernetes/pki/etcd/server.crt
       - --key-file=/etc/kubernetes/pki/etcd/server.key
       - --listen-client-urls=https://127.0.0.1:2379,https://10.5.228.12:2379
       - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
       
   # etcd.yaml에 나온 정보와 공식 홈페에지에 있는 Snapshot using etcdctl options 내용을 참고해서 백업을 한다
   ETCDCTL_API=3 etcdctl snapshot save --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=127.0.0.1:2379 /opt/etcd-backup.db
   ```

   

2. Create a Pod called `redis-storage` with image: `redis:alpine` with a Volume of type `emptyDir` that lasts for the life of the Pod.

   - Pod named 'redis-storage' created
   - Pod 'redis-storage' uses Volume type of emptyDir
   - Pod 'redis-storage' uses volumeMount with mountPath = /data/redis

   > emptyDir를 사용하는 Pod을 만들고 관련된 조건은 문제를 참고해라

   ```yaml
   cat << EOF | kubectl apply -f -
   apiVersion: v1
   kind: Pod
   metadata:
      creationTimestamp: null
      labels:
        run: redis-storage
      name: redis-storage
   spec:
    volumes:
    - name: redis-storage
      emptyDir: {}
    
    containers:
    - image: redis:alpine
      name: redis-storage
      resources: {}
      volumeMounts:
      - name: redis-storage
        mountPath: /data/redis
    dnsPolicy: ClusterFirst
    restartPolicy: Always
   status: {}
   EOF
   ```

   

3. Create a new pod called `super-user-pod` with image `busybox:1.28`. Allow the pod to be able to set `system_time`.

   - The container should sleep for 4800 seconds.
   - Pod: super-user-pod
   - Container Image: busybox:1.28
   - SYS_TIME capabilities for the conatiner?

   > 위 조건에 맞게 Pod를 만들어라
   >
   > - `system_time` 이라는 단어를 보고 `securityContext`를 연상해야 할 듯
   > - `capabilities`를 찾아 Pod를 작성해야 한다. ([링크](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-capabilities-for-a-container))
   > - `command`옵션을 잊지말고 추가 해야 한다.
   >   위에 링크된 페이지에서 command 키워드 검색하면 어떻게 입력하는지 찾아 볼 수 있다.

   ```yaml
   # super-user-pod 를 생성
   cat << EOF | kubectl apply -f -
   apiVersion: v1
   kind: Pod
   metadata:
     creationTimestamp: null
     name: super-user-pod
   spec:
     containers:
     - image: busybox:1.28
       name: super-user-pod
       command: ["sleep", "4800"]
       securityContext:
         capabilities:
           add: ["SYS_TIME"]
   EOF
   
   # super-user-pod 정상 동작하는지 확인
   kubectl get pod
   ```

   

4. A pod definition file is created at `/root/CKA/use-pv.yaml`. Make use of this manifest file and mount the persistent volume called `pv-1`. Ensure the pod is running and the PV is bound.

   - mountPath: `/data`
   - persistentVolumeClaim Name: `my-pvc`
   - persistentVolume Claim configured correctly
   - pod using the correct mountPath
   - pod using the persistent volume claim?

   > Pod의 설정을 확인하고 PVC에 관련되어 오류가 없는지 확인해라
   >
   > 1) pv 확인
   > 2) pvc 확인
   > 3) pod 확인

   ```shell
   # PV가 있는지 확인한다.
   kubectl get pv
   
   # PVC가 있는지 확인한다.
   kubectl get pvc
   
   # PVC가 없으니 생성한다.
   #  PV의 CAPACITY가 10Mi 인 것을 확인한다.
   #  또한 ACCESS MODES가 RWO(ReadWriteOnce) 인 것을 확인한다.
   cat << EOF | kubectl apply -f -
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: my-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 10Mi      
   EOF
   
   # 생성된 pvc가 pv와 잘 연결되어 있는지 체크
   kubectl get pv
   # 상태가 Bound 이면 정상
   kubectl get pvc
   
   # 문제에서 제시한 use-pv.yaml 의 내용을 아래와 같이 수정한다
   apiVersion: v1
   kind: Pod
   metadata:
     creationTimestamp: null
     labels:
       run: use-pv
     name: use-pv
   spec:
     containers:
     - image: nginx
       name: use-pv
       volumeMounts:
       - mountPath: "/data"
         name: mypod
     volumes:
     - name: mypod
       persistentVolumeClaim:
         claimName: my-pvc
   
   # 수정된 use-pv.yaml 파일을 시스템에 적용한다.
   kubectl apply -f use-pv.yaml
   
   # pod이 정상적으로 생성되어있는지 체크
   kubectl get pod
   
   # watch 명령으로 실시간 상태 체크 가능
   watch kubectl get pod
   ```

   

5. Create a new deployment called `nginx-deploy`, with image `nginx:1.16` and `1` replica. Record the version. Next upgrade the deployment to version `1.17` using rolling update. Make sure that the version upgrade is recorded in the resource annotation.

   - Deployment : nginx-deploy. Image: nginx:1.16
   - Image: nginx:1.16
   - Task: Upgrade the version of the deployment to 1:17
   - Task: Record the changes for the image upgrade

   > nginx-deploy 이름으로 deployment 작업해라 그리고 nginx 버전업을 하는 rolling update를 수행해라
   >
   > [중요] deployment 작업은 `--record` 옵션을 반드시  써야 한다.

   ```shell
   
   # To create a deployment definition file nginx-deploy:
   kubectl create deployment nginx-deploy --image=nginx:1.16 --dry-run=client -o yaml > deploy.yaml
   
   # [중요] To create a resource from definition file and to record:
   #   --record 옵션을 붙이지 않으면 history를 볼 수 없다.
   kubectl apply -f deploy.yaml --record
   
   # record 옵션으로 기록된 REVISION 정보 확인!
   kubectl rollout history deployment nginx-deploy
   
   # To upgrade the image to next given version:
   kubectl set image deployment/nginx-deploy nginx=nginx:1.17 --record
   
   # To view the history of deployment nginx-deploy:
   kubectl rollout history deployment nginx-deploy
   ```

   작업 로그

   ```shell
   # deployment 정보
   # NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
   # deployment.apps/nginx-deploy   1/1     1            1           34s
   
   # deployment 기록 확인
   kubectl rollout history deployment nginx-deploy
   # REVISION  CHANGE-CAUSE
   # 1         kubectl apply --filename=nginx-deploy.yaml --record=true
   
   # deployment 에 배포된 nginx 버전 변경
   kubectl set image deployment.apps/nginx-deploy nginx=nginx:1.17 --record
   
   # deployment 기록 확인(REVISION 2가 추가)
   kubectl rollout history deployment nginx-deploy
   # REVISION  CHANGE-CAUSE
   # 1         kubectl apply --filename=nginx-deploy.yaml --record=true
   # 2         kubectl set image deployment.apps/nginx-deploy nginx=nginx:1.17 --record=true
   ```

   

6. Create a new user called `john`. Grant him access to the cluster. John should have permission to `create, list, get, update and delete pods` in the `development` namespace . The private key exists in the location: `/root/CKA/john.key` and csr at `/root/CKA/john.csr`.

   - `Important Note`: As of kubernetes 1.19, the CertificateSigningRequest object expects a `signerName`.
   - Please refer the documentation to see an example. The documentation tab is available at the top right of terminal.
   - CSR: john-developer Status:Approved
   - Role Name: developer, namespace: development, Resource: Pods
   - Access: User 'john' has appropriate permissions

   > 1. 디렉토리에 john.csr  john.key 파일이 있는지 확인
   >
   > 2. kubectl api-version 체크
   >
   >    ```shell
   >    kubectl api-versions | grep certif
   >    # certificates.k8s.io/v1
   >    # certificates.k8s.io/v1beta1
   >    ```
   >
   > 3. 공식문서 [참고](https://kubernetes.io/ko/docs/tasks/tls/managing-tls-in-a-cluster/#%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4-api%EB%A1%9C-%EB%B3%B4%EB%82%BC-%EC%9D%B8%EC%A6%9D%EC%84%9C-%EC%84%9C%EB%AA%85-%EC%9A%94%EC%B2%AD-%EA%B0%9D%EC%B2%B4-%EB%A7%8C%EB%93%A4%EA%B8%B0)
   >
   >    1. `john.yaml`파일 생성 후 공식문서의 예제를 붙여 넣기
   >
   >    ```yaml
   >    apiVersion: certificates.k8s.io/v1
   >    kind: CertificateSigningRequest
   >    metadata:
   >      name: john-developer
   >    spec:
   >      signerName: kubernetes.io/kube-apiserver-client
   >      request: <base64처리한 값>
   >      usages:
   >      - digital signature
   >      - key encipherment
   >      - client auth
   >      groups:
   >      - system:authenticated
   >    ```
   >
   > 4. john.csr의 base64 변환 값 출력
   >
   >    ```shell
   >    cat john.csr | base64 | tr -d "\n"
   >    LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZEQ0NBVHdDQVFBd0R6RU5NQXNHQTFVRUF3d0VhbTlvYmpDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRApnZ0VQQURDQ0FRb0NnZ0VCQU01LzhaZS9nMDA1UkJTWWZMelpFcFF1Y2RXUUlLenpBeWdlOVRLRW9HbjRxWVE4Cjh5MUFRTGpxVWhVVnd4V0ZyeXl5OTFvQm5GY0xuRE1VQnRlcUVRM01Qd0xjeHN1aExHSXhlWHRMek0rZGZQQ2MKeSs2UXYzSk1aWDJJVXEwMUZqSDJ6Y3Y2OEVqVENvblFEdU12ZDlBcFVjZVB5RFIrTHhIZTFlc2tRbW1qdlRFYgpaM0Q3YXA2cmhEc242NW1WRUhxU1p5K3RIZ2VmVGNrc2FFOEhIMG5SeE9nWU9PM1JScnBpYzRwMUg4TWxDbGpxCkZoWityczFHdFRuZU9TVXBQdDNGR0o0aThnNmZaV3RmM3lmZXQ5Z1FNRGlOc3ZiRFVpMFBpSWhyL1pGbnRHN00KRlBSQmIrZnVGZW1US1lObUhkWFhwZFdGMGxzSE9OMHo3VjFUS1FjQ0F3RUFBYUFBTUEwR0NTcUdTSWIzRFFFQgpDd1VBQTRJQkFRREhKRm5LSkNxQ1B3bHZEQ2h6K2x3RlpCYjdTT1ZKUXFuR3c3QkhtanVhTFhPdlhkcW0yMko5CmdObTlTRSt4ZXNMV1dyeEtsTDJqYUFubm5Vd0loTGpYMGpRNDZZUVVSR29DUUVjRHkvWXp0aW5rV0IrcFJnUlUKcmtPMVhUdmRCUHFQRFBqazBFemthMzlGRFhrN2duSXNCbUJ3K0tuZm9tOG1GNHBVc0JYTDVNeW1GNk5vcitYdwpuTC90QlhzNWh6aTVPT2N6Q3g1SmZ6ZEhUaWttdE9XMG9pZUdjQmo0dUx5MmZsaWMwOFdrMzRvS2NmNWtSZGRWCk1zdEhvNmIxTDZjYVA4cGQySjg2RVlzZGhkdnM1Mm5sajUzeEJxWHRvazRaR0lJZVN4TkF2T3k4MUZpRTBFMDUKL0Z6eXJDODZNTFZDM0JrWlc2QmU0c1VjM0NVUWtIc0IKLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tCg==
   >    ```
   >
   >    
   >
   > 5. john.yaml 파일에 base64 내용 추가하기
   >
   > 6. yaml 적용하기
   >
   >    ```shell
   >    kubectl apply -f john.yaml
   >    ```
   >
   > 7. create 확인 및 certificate approve 하기
   >
   >    ```shell
   >    kubectl get csr
   >    # NAME             CONDITION
   >    # john-developer   Pending
   >    
   >    kubectl certificate approve john-developer
   >    # certificatesigningrequest.certificates.k8s.io/john-developer approved
   >    
   >    kubectl get csr
   >    # NAME             CONDITION
   >    # john-developer   Approved,Issued
   >    ```
   >
   > 8. Role & Rolebinding 추가하기
   >
   >    ```shell
   >    # create role = developer
   >    kubectl create role developer --resource=pods --verb=create,list,get,update,delete --namespace=development
   >    
   >    # create rolebinding = developer-role-binding
   >    kubectl create rolebinding developer-role-binding --role=developer --user=john --namespace=development
   >    
   >    # 추가된 결과 확인
   >    kubectl -n development describe rolebindings.rbac.authorization.k8s.io developer-role-binding 
   >    # Name:         developer-role-binding
   >    # Labels:       <none>
   >    # Annotations:  <none>
   >    # Role:
   >    #   Kind:  Role
   >    #   Name:  developer
   >    # Subjects:
   >    #   Kind  Name  Namespace
   >    #   ----  ----  ---------
   >    #   User  john  
   >    ```
   >
   >    
   >
   > 9.  권한 체크하기
   >
   >    ```shell
   >    kubectl auth can-i update pods --as=john --namespace=development
   >    # yes
   >    ```
   >
   >    

   

   

7. Create a nginx pod called `nginx-resolver` using image `nginx`, expose it internally with a service called `nginx-resolver-service`. Test that you are able to look up the service and pod names from within the cluster. Use the image: `busybox:1.28` for dns lookup. Record results in `/root/CKA/nginx.svc` and `/root/CKA/nginx.pod`

   - Pod: nginx-resolver created
   - Service DNS Resolution recorded correctly
   - Pod DNS resolution recorded correctly

   ```shell
   # To create a pod nginx-resolver and expose it internally:
   kubectl run nginx-resolver --image=nginx
   
   kubectl expose pod nginx-resolver --name=nginx-resolver-service --port=80 --target-port=80 --type=ClusterIP
   
   # To create a pod test-nslookup. Test that you are able to look up the service and pod names from within the cluster:
   kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup nginx-resolver-service
   
   kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup nginx-resolver-service > /root/CKA/nginx.svc
   
   # Get the IP of the nginx-resolver pod and replace the dots(.) with hyphon(-) which will be used below.
   kubectl get pod nginx-resolver -o wide
   
   # kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup <P-O-D-I-P.default.pod> > /root/CKA/nginx.pod
   # 10.50.192.1 이 아니고 10-50-192-1 으로 입력
   kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup 10-50-192-1.default.pod > /root/CKA/nginx.pod
   ```

   

8. Create a static pod on `node01` called `nginx-critical` with image `nginx` and make sure that it is recreated/restarted automatically in case of a failure.

   - Use `/etc/kubernetes/manifests` as the Static Pod path for example.

   - static pod configured under /etc/kubernetes/manifests ?
   - Pod nginx-critical-node01 is up and running

   ```shell
   # To create a static pod called nginx-critical by using below command:
   kubectl run nginx-critical --image=nginx --dry-run=client -o yaml > static.yaml
   
   # Copy the contents of this file or use scp command to transfer this file from controlplane to node01 node.
   scp static.yaml node01:/root/
   
   # To know the IP Address of the node01 node:
   kubectl get nodes -o wide
   
   # Perform SSH
   ssh node01
   #OR ssh <IP of node01>
   
   # /etc/kubernetes/manifests 경로가 없다면 만들어라
   mkdir -p /etc/kubernetes/manifests
   
   # kubelet 상태로 config.yaml 파일 찾기
   systemctl status kubelet
   # --config=/var/lib/kubelet/config.yaml 을 찾을 수 있다
   
   # config.yaml에 staticPodPath 필드가 없으면 추가
   # 위치는 /etc/kubernetes/manifests/ 이다.
   vi /var/lib/kubelet/config.yaml
   
   # master 노드에서 전송했던 static.yaml 파일을 manifests 으로 복사한다.
   cp /root/static.yaml /etc/kubernetes/manifests/
   
   # static.yaml 파일 내용을 nginx-critical 으로 수정한다. 이미지는 nginx
   vi /etc/kubernetes/manifests/static.yaml
   
   # master 노드로 돌아와 pod 상태를 확인한다.
   kubectl get pods
   ```
   
   

