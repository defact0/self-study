15강 구현 유형 문제 풀이 ([링크](https://youtu.be/QhMY4t2xwG0))

---

![lec15-01](.\img\lec15-01.png)

![lec15-02](.\img\lec15-02.png)

![lec15-03](.\img\lec15-03.png)

답안 예시

```python
# H 입력 받기
h = int(input())

count = 0
for i in range(h+1):
    for j in range(60):
        for k in range(60):
            # 매 시각 안에 '3'이 포함되어 있다면 카운트 증가
            if '3' in str(i) + str(j) + str(k):
                count += 1
                
print(count)

# 5
# 11475
```



---



![lec15-04](.\img\lec15-04.png)

![lec15-05](.\img\lec15-05.png)

![lec15-06](.\img\lec15-06.png)

![lec15-07](.\img\lec15-07.png)

문제 해결 아이디어

- 요구사항 대로 충실히 구현하면 되는 문제
- 나이트의 8가지 경로를 하나 씩 확인하며 각 위치로 이동이 가능한지 확인
  - 리스트를 이용하여 8가지 방향에 대한 방향 벡터를 정의

답안예시

```python
# 현재 나이트의 위치 입력받기
input_data = input()
row = int(input_data[1])

# ord(c)는 문자의 유니코드 값을 돌려주는 함수이다.
# >>> ord('a')
#     97
column = int(ord(input_data[0])) - int(ord('a')) + 1

# 나이트가 이동할 수 있는 8가지 방향 정의
steps = [(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1)]

# 8가지 방향에 대하여 각 위치로 이동이 가능한지 확인
result = 0
for step in steps:
    # 이동하고자 하는 위치 확인
    next_row = row + step[0]
    next_column = column + step[1]
    # 해당 위치로 이동이 가능하다면 카운트 증가
    if next_row >=1 and next_row <=8 and next_column >=1 and next_column <= 8:
        result += 1
        
print(result)

# a1
# 2
```



---



![lec15-08](.\img\lec15-08.png)

- 문자는 순서대로 정렬을 하고, 1+5+7=13을 출력한다.

![lec15-09](.\img\lec15-09.png)

문제해결 아이디어

- 요구 사항대로 충실히 구현하면 되는 문제
- 문자열이 입력되었을 때 문자를 하나 씩 확인
  - 숫자인 경우 따로 합계를 계산
  - 알파벳인 경우 별도의 리스트에 저장
- 결과적으로 **리스트에 저장된 알파벳을 정렬해 출력하고, 합계를 뒤에 붙여 출력하면 정답**

답안예시

```python
data = input()
result = []
value = 0

# 문자를 하나씩 확인
for x in data:
    # 알파벳인 경우 결과 리스트에 삽입
    if x.isalpha():
        result.append(x)
    # 숫자는 따로 더하기
    else:
        value += int(x)
        
# 알파벳을 오름차순으로 정렬
result.sort()

# 숫자가 하나라도 존재하는 경우 가장 뒤에 삽입
if value != 0:
    result.append(str(value))
    
# 최종 결과 출력(리스트를 문자열로 변환하여 출력)
print(''.join(result))


# k1ka5cb7
# abckk13
```



