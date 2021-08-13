# 문제 설명
#  직사각형을 만드는 데 필요한 4개의 점 중 3개의 좌표가 주어질 때, 나머지 한 점의 좌표를 구하려고 합니다. 
#  점 3개의 좌표가 들어있는 배열 v가 매개변수로 주어질 때, 직사각형을 만드는 데 필요한 나머지 한 점의 좌표를 return 하도록 solution 함수를 완성해주세요. 
#  단, 직사각형의 각 변은 x축, y축에 평행하며, 반드시 직사각형을 만들 수 있는 경우만 입력으로 주어집니다.
# 
# 제한사항
#  - v는 세 점의 좌표가 들어있는 2차원 배열입니다.
#  - v의 각 원소는 점의 좌표를 나타내며, 좌표는 [x축 좌표, y축 좌표] 순으로 주어집니다.
#  - 좌표값은 1 이상 10억 이하의 자연수입니다.
#  - 직사각형을 만드는 데 필요한 나머지 한 점의 좌표를 [x축 좌표, y축 좌표] 순으로 담아 return 해주세요.
#
# 입출력 예시
#  입출력 예 #1
#   세 점이 [1, 4], [3, 4], [3, 10] 위치에 있을 때, [1, 10]에 점이 위치하면 직사각형이 됩니다.
#  
#  입출력 예 #2
#   세 점이 [1, 1], [2, 2], [1, 2] 위치에 있을 때, [2, 1]에 점이 위치하면 직사각형이 됩니다.
#

def solution(v):
    answer = []
    array_x = []
    array_y = []
    
    for x in range(len(v)):
        array_x.append(v[x][0]) # x        
        array_y.append(v[x][1]) # y
        
    array_xx = list(set(array_x))
    array_yy = list(set(array_y))
    
    cnt_x = []
    for ax in array_xx:
        cnt = 0
        for x in array_x:
            if(ax == x):
                cnt += 1
        cnt_x.append((ax, cnt))
    cnt_x = sorted(cnt_x, key=lambda arr: arr[1])
    
    cnt_y = []
    for ay in array_yy:
        cnt = 0
        for y in array_y:
            if( ay == y):
                cnt += 1
        cnt_y.append((ay, cnt))
    cnt_y = sorted(cnt_y, key=lambda arr: arr[1])

    answer.append(cnt_x[0][0])
    answer.append(cnt_y[0][0])
        
    return answer