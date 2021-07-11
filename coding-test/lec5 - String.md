5강 파이썬 문법: 문자열, 튜플 자료형 ([링크](https://youtu.be/p6df7qv6jFQ))

---

```python
# 문자열 자료형
print("-------- 문자열 자료형 -------------")
data = 'hello world'
print(data)

data = "Don't you know \\"python\\"?"
print(data)

a = "hello"
b = "world"
print(a + " " + b)

a = "String"
print(a*3)

# 문자열 슬라이싱
a = "ABCDEF"
print(a[2:4])

# 튜플 자료형
# - 한번 선언된 값을 변경할 수 없다.
# - 튜플은 소괄호를 이용
# - 리스트에 비해 공간 효율적
print("-------- 튜플 -------------")
a = (1,2,3,4,5,6,7,8,9)

print(a[3])

print(a[1:4])

# 오류 - 특정한 위치를 변경할 수 없음
# a[2] = 7

# 튜플을 사용하면 좋은 경우
# - 서로 다른 성질의 데이터를 묶어서 관리
# - 데이터의 나열을 해싱(Hashing)의 키 값으로 사용
# - 리스트보다 메모리를 효율적으로 사용해야 할 때
```

