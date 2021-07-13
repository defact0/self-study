 9강 파이썬 문법: 반복문 ([링크](https://youtu.be/x7dIUaefI0A))

---

- 특정한 소스코드를 반복 실행하고자 할 때 사용
- while문과 for문이 있는데, 코테에서 보면 for문이 더 간결한 경우가 많다.

```python
# 1부터 9까지 모든 정수의 합 구하기
i = 1
result = 0

# i가 9보다 작거나 같을 때 아래 코드를 반복적으로 실행
while i <= 9:
  result += i
  i += 1

print(result)


# 1부터 9까지 홀수의 합 구하기
i = 1
result = 0

while i <= 9:
  if i%2 == 1:
    result += i
  i += 1

print(result)
```



#### 반복문에서의 무한 루프

- 끊임없이 반복되는 반복 구문
  - 코딩 테스트에서는 구현할 일은 거의 없다.

```python
# 반복문을 탈출 할 수 없다.
x = 10

while x > 5:
  print(x)
```



#### for 문

- 특정한 변수를 이용하여 'in' 뒤에 오는 데이터(리스트, 튜플 등)에 포함되어 있는 원소를 첫 번째 인덱스부터 차례대로 하나 씩 방문 한다.

```python
for 변수 in 리스트:
    실행할 소스코드
```



- for문에서 연속적인 값을 차례대로 순회 할 때는 range()를 주로 사용
  - 이때 range(시작 값, 끝 값 = 1) 형태로 사용
  - 인자를 하나만 넣으면 자동으로 시작 값은 0이 된다.

```python
print("-- 기본 for 문 ---")
# 기본 for 문
array = [9,8,7,6,5]

for x in array:
    print(x)
    
# rage()
print("-- rage()예제 ---")
result = 0

for i in range(1, 10):
    result += i
    
print(result)
```

