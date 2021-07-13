8강 파이썬 문법: 조건문 ([링크](https://youtu.be/PCJOT5LHzxE))

---

```python
# 조건문 예제
x = 15

if x >= 10:
  print("x >= 10")

if x >=0:
  print("x >= 0")

if x >=30:
  print("x >= 30")
```

- 코드의 블록(block)을 들여쓰기(indent)로 지정

- 파이썬은 <u>*4개의 공백문자를 사용하는 것을 표준*</u>으로 설정하고 있다.



#### 조건문의 기본 형태

- if ~ elif ~ else
- elif 혹은 else 는 경우에 따라 사용하지 않아도 된다.

```python
if 조건문 1:
    조건문이 1이 True일 때 실행
elif 조건문 2:
    조건문 1에 해당하지 않고, 조건문 2가 True일 때 실행
else:
    위의 모든 조건문이 모두 True 값이 아닌 경우
```

```python
# 조건문 기본예제
a = 5
if a >= 0:
    print("a >= 0")
elif a >= -10:
    print("a >= -10")
else:
    print("-10 > a")
    
# 학점
score = 85

if score >= 90:
    print("학점: A")
elif score >= 80:
    print("학점: B")
elif score >= 70:
    print("학점: C")
else:
    print("학점: F")
```



#### 비교 연산자

- X == Y
  - 대입 연산자(=)
  - <u>같음 연산자(==)</u>
- X != Y
- X > Y
- X < Y
- X >= Y
- X <= Y



#### 논리 연산자

- X and Y = 모두 True 일 때 True
- X or Y = 하나만 True 인 경우 True
- not X = X가 false 인 경우 True



#### 기타 연산자

- 다수의 데이터를 담는 자료형을 위해 in 연산자와 not in 연산자가 제공
  - 리스트, 튜플, 문자열, 딕셔너리 모두에서 사용 가능
- x in 리스트
  - 리스트 안에 x가 들어가 있을 때 참(True)이다.
- x not in 리스트
  - 문자열 안에 x가 들어가 있지 않을 때 참(True)이다.



#### pass 키워드

- 아무것도 처리하고 싶지 않을 때 pass 키워드를 사용
- ex) 디버깅 과정에서 일단 조건문의 형태로만 만들어 놓고 조건문을 처리하는 부분을 비워놓고 싶은 경우

```python
score = 85

if score >= 80:
    pass # 나중에 작성할 소스코드
else:
    print("성적이 80점 미만입니다.")
    
print("프로그램 종료")
```

