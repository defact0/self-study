10강 파이썬 문법: 함수와 람다 표현식 ([링크](https://youtu.be/M_wLOmNRBN8))

---

함수 정의하기

```python
def 함수명(매개변수):
    실행할 소스코드
    return 반환 값
```



```python
# 함수예제 1
def add(a, b):
  return a + b

print(add(3,7))

# 함수예제 2
def add2(a, b):
  print('함수의 결과:',a+b)

add2(3,7)
```



global 키워드

- global 키워드로 변수를 지정하면 해당 함수에서는 지역 변수를 만들지 않고, 함수 바깥에 선언된 변수를 바로 참조

```python
a = 0

def func():
    global a
    a += 1
    
for i in range(10):
    func()
    
print(a)

# 10
```



global 키워드를 쓰지 않는 경우

```python
# case 1
a = 20

def func():
    # 밖에 있는 a 변수를 인식하지 못하여
    # a라는 변수를 func()안에서 새로 정의해야 한다.
    a = 0
    a += 1
    print(a)
    
func()
# 결과 = 1


# case 2
a = 20

def func():
    # global 키워드를 사용
    global a
    a += 1
    print(a)
    
func()
# 결과 = 21
```



전역변수로 리스트 객체가 생성되어 있을 경우

```python
array = [1,2,3,4,5]

def func():
    # 오류 없이 6 추가가 가능함
    array.append(6)
    print(array)

func()

# 결과 = [1, 2, 3, 4, 5, 6]
```

만약에 지역변수에 동일한 이름으로 선언된다면 우선순위는 지역변수로 처리하게된다.

```python
# 전역변수
array = [1,2,3,4,5]

def func():
    # 지역변수
    array = [3,4,5]
    array.append(6)
    print("func():")
    print(array)

func()
print("main():")
print(array)

# func():
# [3, 4, 5, 6]
# main():
# [1, 2, 3, 4, 5]
```

지역변수에 global 을 선언하는 경우

```python
array = [1,2,3,4,5]

def func():
    global array
    array = [3,4,5]
    array.append(6)
    print("func():")
    print(array)

func()
print("main():")
print(array)

# func():
# [3, 4, 5, 6]
# main():
# [3, 4, 5, 6]
```

파이썬에서 함수는 여러개의 반환 값을 가질 수 있다.

```python
def op(a,b):
    add_var = a+b
    subtract_var = a-b
    multiply_var = a*b
    divide_var = a/b
    return add_var, subtract_var, multiply_var, divide_var

a, b, c, d = op(7, 3)
print(a, b, c, d)

# 결과 = 10 4 21 2.3333333333333335
```

람다 표현식

- 함수를 간단하게 작성
- 특정한 기능을 수행하는 함수를 한줄에 작성할 수 있는게 특징

```python
def add(a,b):
    return a+b

# 일반적인 add() 메서드
print(add(3,7))

# 람다 표현식으로 구현한 add() 메서드
print((lambda a, b: a+b)(3, 7))
```

- 이름없는 함수라고도 불리기도 한다.

[예시] 내장 함수에서 자주 사용되는 람다함수

```python
array = [('홍길동', 50),('이순신', 32),('아무개', 74)]

def my_key(x):
    return x[1]

print(sorted(array, key=my_key))
print(sorted(array, key=lambda x: x[1]))

# [('이순신', 32), ('홍길동', 50), ('아무개', 74)]
# [('이순신', 32), ('홍길동', 50), ('아무개', 74)]
```

[예시] 여러 개의 리스트에 적용

```python
list1 = [1,2,3,4,5]
list2 = [6,7,8,9,10]

result = map(lambda a, b: a+ b, list1, list2)

print(list(result))

# [7, 9, 11, 13, 15]
```

