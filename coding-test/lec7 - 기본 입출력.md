7강 파이썬 문법: 기본 입출력 ([링크](https://youtu.be/EmVu4na4fRY))

---

- input() 함수는 한 줄의 문자열을 입력 받는 함수
- map() 함수는 리스트의 모든 원소에 각각 특정한 함수를 적용

```python
# 공백을 기준으로 구분된 데이터를 입력 받을 때는 다음과 같이 사용
list(map(int, input().split()))

# 공백을 기준으로 구분된 데이터의 개수가 많지 않다면 단순히 다음과 같이 사용
a, b, c = map(int, input().split())
```



<u>★ 코딩 테스트에서 많이 쓰이는 입력 형태</u>

```python
# 데이터의 개수 입력
n = int(input())
# 각 데이터를 공백을 기준으로 구분하여 입력
data = list(map(int, input().split()))

data.sort(reverse=True)
print(data)

# 테스트
# 5
# 10 40 20 30 50
# [50, 40, 30, 20, 10]
```



선언한 변수 개수 보다 많이 입력하거나 적게 입력하면 오류가 발생

```python
# n, m, k를 공백 기준으로 구분하여 입력
n, m, k = map(int, input().split())

print(n, m, k)
```



<u>★ 빠르게 입력을 받아야 하는 경우</u>

- sys.stdin.readline() 메서드를 이용
  - 단, 입력 후 엔터(Enter)가 줄 바꿈 기호로 입력되므로 rstrip() 메서드를 함께 사용

```python
import sys

# 문자열 입력 받기
data = sys.stdin.readline().rstrip()
print(data)
```



- print()는 기본적으로 출력 이후에 줄 바꿈을 수행한다.
  - 줄 바꿈을 원치 않는 경우 `end` 속성을 이용할 수 있다.

```python
# 출력할 변수들
a = 1
b = 2
print(a, b)
print(7, end=" ")
print(8, end=" ")

# 출력할 변수
answer = 7
print("정답은 "+str(answer)+" 입니다!")

# 1 2
# 7 8 정답은 7 입니다.!
```



f-string 예제

```python
#파이썬 3.6 부터 사용가능한 기능
# - 중괄호 안에 변수명을 기입하여 간단히 문자열과 정수를 함께 넣을 수 있다.
answer = 7
print(f"정답은 {answer}입니다?")

# 정답은 7입니다?
```

