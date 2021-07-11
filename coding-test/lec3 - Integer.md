3강 파이썬 문법 수 자료형 ([링크](https://youtu.be/INg6kdOEEVc))

---

정수형

```python
# 양의 정수
a = 1000
print(a)

# 음의 정수
a = -7
print(a)

# 0
a = 0
print(a)

# 실행결과
1000
-7
0
```

실수형

```python
# 양의 실수
a = 157.93
print(a)

# 음의 실수
a = -1837.2
print(a)

# 소수부가 0일 때 0을 생략
a = 5.
print(a)

# 정수부가 0일 때 0을 생략
a = -.7
print(a)

# 실행결과
157.93
-1837.2
5.0
-0.7
```

지수 표현 방식

```python
# 1,000,000,000의 지수 표현 방식
a = 1e9
# a = int(1e9) 
print(a)

# 752.5
a = 75.25e1
print(a)

# 3.954
a = 3954e-3
print(a)

# 실행결과
1000000000.0
752.5
3.954
```

실수값을 제대로 비교하기

```python
# round() 함수를 이용한다.
a = 0.3 + 0.6
print(round(a, 4))

if round(a, 4) == 0.9:
    print(True)
else:
    print(False)

# 실행결과
0.9
True
```

수 자료형의 연산

```python
a = 7
b = 3

# 나누기
print(a / b)

# 나머지
print(a & b)

# 몫
print(a // b)

a = 5
b = 3

# 거듭제곱
print(a ** b)

# 제곱근
print(a ** 0.5)

# 실행결과
2.3333333333333335
3
2
125
2.23606797749979
```

