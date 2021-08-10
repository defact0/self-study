# 선택정렬
#
# 실행 결과
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#

array = [7,5,9,0,3,1,6,2,4,8]

for i in range(len(array)):
    min_index = i # 가장 작은 원소의 인덱스
    for j in range(i+1,len(array)):
        if array[min_index] > array[j]:
            min_index = j
    array[i], array[min_index] = array[min_index], array[i] # 스와프

print(array)

# 첫번째 정렬
#  i = 0, min_index = 3, j = 9
#  상황일 때 배열 array[0]=7 과 array[3]=0 의 값이 교환된다.
# http://pythontutor.com 에서 코드를 돌려보자