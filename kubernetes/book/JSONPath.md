### :ship: JSONPath

- https://kubernetes.io/ko/docs/reference/kubectl/jsonpath/

JSONPath 템플릿은 중괄호 {}로 둘러싸인 JSONPath 표현식으로 구성

1. 큰따옴표를 사용하여 JSONPath 표현식 내부의 텍스트를 인용한다.
2. 목록을 반복하려면 `range`, `end` 오퍼레이터를 사용한다.
3. 목록에서 뒤로 이동하려면 negative slice 인덱스를 사용한다. negative 인덱스는 목록을 "순환(wrap around)" 하지 않으며, `-index + listLength >= 0` 인 한 유효하다.

---

`kubectl` 및 JSONPath 표현식을 사용하는 예는 다음과 같다.

```shell
kubectl get pods -o json
kubectl get pods -o=jsonpath='{@}'
kubectl get pods -o=jsonpath='{.items[0]}'
kubectl get pods -o=jsonpath='{.items[0].metadata.name}'
kubectl get pods -o=jsonpath="{.items[*]['metadata.name', 'status.capacity']}"
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'

# kubectl은 JSONPath 출력에 대한 정규 표현식을 지원하지 않는다.
# 다음 커맨드는 작동하지 않는다.
kubectl get pods -o jsonpath='{.items[?(@.metadata.name=~/^test$/)].metadata.name}'

# 다음 커맨드는 원하는 결과를 얻는다.
kubectl get pods -o json | jq -r '.items[] | select(.metadata.name | test("test-")).spec.containers[].image'
```

