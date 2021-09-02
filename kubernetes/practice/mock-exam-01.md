Mock Exam - 1

- Mock Test Link - https://uklabs.kodekloud.com/topic/mock-exam-1-4/
- https://github.com/kodekloudhub/certified-kubernetes-administrator-course



Tip

- 시험 터미널에 붙여 넣기 단축키 
  - <shift> + <insert>
- 치트시트 [링크](https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/)



Solution

1. Deploy a pod named `nginx-pod` using the `nginx:alpine` image.

   - Name: nginx-pod
   - Image: nginx:alpine

   ```shell
   # 그냥 아래 명령 한줄로 Pod를 만든다.
   kubectl run nginx-pod --image=nginx:alpine
   
   # 또는,  `nginx-pod.yaml`을 만들지 않고 직접 붙여넣기 해서 pod을 생성하는 방법도 있다.
   root@controlplane:~# cat << EOF | kubectl apply -f -
   > apiVersion: v1
   > kind: Pod
   > metadata:
   >   creationTimestamp: null
   >   labels:
   >     run: nginx-pod
   >   name: nginx-pod
   > spec:
   >   containers:
   >   - image: nginx:alpine
   >     name: nginx-pod
   >     resources: {}
   >   dnsPolicy: ClusterFirst
   >   restartPolicy: Always
   > status: {}
   > EOF
   pod/nginx-pod created
   root@controlplane:~# 
   ```

   

2. Deploy a `messaging` pod using the `redis:alpine` image with the labels set to `tier=msg`.

   - 
     Pod Name: messaging
   - Image: redis:alpine
   - Labels: tier=msg

   ```shell
   # 1번 문제와 동일하나 `labels`를 추가하여 pod를 만드는 문제
   kubectl run messaging --image=redis:alpine --labels=tier=msg
   ```

   

3. Create a namespace named `apx-x9984574`.

   - Namespace: apx-x9984574

   ```shell
   # 네임스페이스는 create 명령을 사용하여 만든다.
   kubectl create namespace apx-x9984574
   ```

   

4. Get the list of nodes in JSON format and store it in a file at `/opt/outputs/nodes-z3444kd9.json`.

   ```shell
   # JSON 포맷은 `-o json` 옵션을 통해 출력 할 수 있고 이것을 리눅스의 출력 리다이렉션을 통해 특정 파일에 저장을 하는 문제
   kubectl get nodes -o json > /opt/outputs/nodes-z3444kd9.json
   ```

   

5. Create a service `messaging-service` to expose the `messaging` application within the cluster on port `6379`.

   - Service: messaging-service
   - Port: 6379
   - Type: ClusterIp
   - Use the right labels

   ```shell
   # 기존에 생성된 messaging pod에 messaging-service 이라는 이름의 Service 리소스를 설정하기
   kubectl expose pod messaging --port=6379 --name messaging-service
   ```

   - [참고](https://kubernetes.io/ko/docs/tutorials/stateless-application/expose-external-ip-address/)

   

6. Create a deployment named `hr-web-app` using the image `kodekloud/webapp-color` with `2` replicas.

   - 
     Name: hr-web-app
   - Image: kodekloud/webapp-color
   - Replicas: 2

   ```yaml
   # 풀이1
   kubectl create deployment hr-web-app --image=kodekloud/webapp-color --replicas=2
   
   # 풀이2
   cat << EOF | kubectl apply -f -
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     creationTimestamp: null
     labels:
       app: hr-web-app
     name: hr-web-app
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: hr-web-app
     strategy: {}
     template:
       metadata:
         creationTimestamp: null
         labels:
           app: hr-web-app
       spec:
         containers:
         - image: kodekloud/webapp-color
           name: webapp-color
           resources: {}
   status: {}
   EOF
   ```

   

7. Create a static pod named `static-busybox` on the master node that uses the `busybox` image and the command `sleep 1000`.

   - 
     Name: static-busybox
   - Image: busybox

   ```shell
   # 이거는 어떻게 풀든지 오답으로 채점되는 것 같다.
   kubectl run --restart=Never --image=busybox static-busybox --dry-run=client -oyaml --command -- sleep 1000 > ./static-busybox.yaml
   
   kubectl apply -f static-busybox.yaml
   ```

   

   ```yaml
   cat << EOF | kubectl apply -f -
   apiVersion: v1
   kind: Pod
   metadata:
     creationTimestamp: null
     labels:
       run: static-busybox
     name: static-busybox
   spec:
     containers:
     - command:
       - sleep
       - "1000"
       image: busybox
       name: static-busybox
       resources: {}
     dnsPolicy: ClusterFirst
     restartPolicy: Always
   status: {}
   EOF
   ```

   

8. Create a POD in the `finance` namespace named `temp-bus` with the image `redis:alpine`.

   - Name: temp-bus
   - Image Name: redis:alpine

   ```shell
   kubectl run temp-bus --image=redis:alpine -n finance
   ```

   

9. A new application `orange` is deployed. There is something wrong with it. Identify and fix the issue.

   ```shell
   kubectl describe pod orange
   # Error가 발생하는 부분을 찾다보면 init containers 부분에
   # Reason: Error라고 써져 있는데 Command 부분에 sleeeep 이라고 잘못 입력된 것을
   # 확인 할 수 있다. 이 부분을 수정해야 한다.
   
   
   kubectl get pod orange -o yaml > orange.yaml
   vi orange.yaml
   # Export the running pod using below command and correct the spelling of the command sleeeep to sleep
   
   kubectl delete pod orange
   kubectl create -f orange.yaml
   ```

   

10. Expose the `hr-web-app` as service `hr-web-app-service` application on port `30082` on the nodes on the cluster.

    The web application listens on port `8080`.

    - 
      Name: hr-web-app-service
    - Type: NodePort
    - Endpoints: 2
    - Port: 8080
    - NodePort: 30082

    ```yaml
cat << EOF | kubectl apply -f -
    apiVersion: v1
    kind: Service
    metadata:
      creationTimestamp: null
      labels:
        app: hr-web-app
      name: hr-web-app-service
    spec:
      ports:
      - port: 8080
        protocol: TCP
        targetPort: 8080
        nodePort: 30082
      selector:
        app: hr-web-app
      type: NodePort
    status:
      loadBalancer: {}
    EOF
    ```
    
    

11. Use JSON PATH query to retrieve the `osImage`s of all the nodes and store it in a file `/opt/outputs/nodes_os_x43kj56.txt`.

    The `osImages` are under the `nodeInfo` section under `status` of each node.

    

    - node 정보를 json 형태로 출력 해 본다.

      ```shell
      # 아래 명령을 통해 출력되는 json full 구조에서 jsonpath를 직접 찾는 연습이 필요
      kubectl get nodes -o json
      
      # "osImage": "Ubuntu 18.04.5 LTS",
      kubectl get nodes -o json | grep "osImage"
      ```

    - 공식 홈페이지에서 `jsonpath`로 검색하여 정보를 찾는다 [링크](https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/)

      ```shell
      # 모든 노드의 외부IP를 조회
      # kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'
      # 위 예제를 참고 하여 아래와 같이 명령을 완성 시킨다.
      
      kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}' > /opt/outputs/nodes_os_x43kj56.txt
      ```

      

    

12. Create a `Persistent Volume` with the given specification.

    - Volume Name: pv-analytics
    - Storage: 100Mi
    - Access modes: ReadWriteMany
    - Host Path: /pv/data-analytics

    ```yaml
    cat << EOF | kubectl apply -f -
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: pv-analytics
    spec:
      capacity:
        storage: 100Mi
      volumeMode: Filesystem
      accessModes:
        - ReadWriteMany
      hostPath:
          path: /pv/data-analytics
    EOF
    ```
    
    

