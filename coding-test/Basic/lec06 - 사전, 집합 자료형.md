6강 파이썬 문법: 사전, 집합 자료형 ([링크](https://youtu.be/Mkk8WOCAlqQ))

---

사전 자료형

- 키(key)와 값(Value)의 쌍을 데이터로 가지는 자료형
- 변경 불가능한(Immutable) 자료형을 키로 사용
- 사전 자료형은 해시 테이블(Hash Table)을 이용하므로 <u>데이터의 조회 및 수정에 있어서 O(1)의 시간에 처리</u>할 수 있다.



```python
print("--- 사전 자료형 ---")

data = dict()
data['사과'] = 'Apple'
data['바나나'] = 'Banana'
data['코코넛'] = 'Coconut'

print(data)

if '사과' in data:
  print("'사과'를 키로 가지는 데이터가 존재")
```



- key() = 키 데이터만 뽑아서 리스트로 이용
- value() = 값 데이터 만을 뽑아서 리스트로 이용



```python
print("--- 사전 자료형 ---")

data = dict()
data['사과'] = 'Apple'
data['바나나'] = 'Banana'
data['코코넛'] = 'Coconut'

# 키 데이터만 담은 리스트
key_list = data.keys()
# 값 데이터만 담은 리스트
value_list = data.values()
print(key_list)
print(value_list)

# 각 키에 따른 값을 하나씩 출력
for key in key_list:
  print(key +" = "+ data[key])


# 다른 방법으로 사전 자료형 초기화하기
print("--- 다른 방법으로 사전 자료형 초기화하기 ---")
data2 = {
  '쌀': 80,
  '보리': 90
}

print(data2)

# keys()는 Object형태로 반환되기 때문에 list 형태로 변환시킨다.
key_list2 = list(data2.keys())
print(key_list2)
```



집합 자료형

- 중복을 허용하지 않음, 순서가 없는 것이 특징
- set() 을 이용하여 리스트 혹은 문자열을 이용해 초기화
- 중괄호 안에 각 원소를 콤마 기준으로 구분하여 삽입, 초기화 할 수 있다.
- 데이터 조회 및 수정에 있어 O(1)의 시간에 처리할 수 있다.

```python
print("--- 집합 자료형 ---")

# 초기화 방법 1
data = set([1, 1, 2, 3, 4, 4, 5])

# 중복되는 원소들이 제거되어 출력된다.
print(data)

# 초기화 방법 2
data = {1, 1, 2, 3, 4, 4, 5}

# 중복되는 원소들이 제거되어 출력된다.
print(data)
```



집합 연산으로 종류

- 합집합 : A or B 에 속하는 원소로 이루어진 집합
- 교집합 : A and B 에 속하는 원소로 이루어진 집합
- 차집합 : A 원소 중에서 B에 속하지 않는 원소들로 이루어진 집합

```python
a = set([1,2,3,4,5])
b = set([3,4,5,6,7])

#합집합
print(a|b)
#교집합
print(a&b)
#차집합
print(a-b)
```



- 원소 추가 : add()
- 원소 여러 개 추가 : updata()
- 특정 원소 삭제 : remove()

```python
data = set([1,2,3])
print(data)

# 새로운 원소 추가
data.add(4)
print(data)

# 새로운 원소 여러 개 추가
data.update([5,6])
print(data)

# 특정한 값을 갖는 원소 삭제
data.remove(3)
print(data)
```



사전 자료형과 집합 자료형의 특징

- 리스트나 튜플은 순서가 있어 **인덱싱**을 통해 자료형 값을 얻을 수 있었다.
- <u>사전자료형과 집합자료형은 순서가 없기 때문에 인덱싱이 없다</u>
  - 사전의 키(key) 또는 집합의 원소(element)를 이용해 O(1)의 시간 복잡도로 조회 한다.
