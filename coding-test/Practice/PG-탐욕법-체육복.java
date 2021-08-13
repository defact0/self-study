class Main {
  public static void main(String[] args) {
    int n = 5;
    int[] lost = {2,4};
    int[] reserve = {1,3,5};
    int result = solution(n, lost, reserve);
    System.out.println(result);
  }


  public static int solution(int n, int[] lost, int[] reserve) {
      int[] people = new int[n];
      int answer = n;

      // 0 : 기본 상태(체육복이 있으며 도난도 당하지 않은 상태)
      // 1 : 여분의 체육복이 있는 상태
      // -1 : 체육복을 도난당한 상태
      for (int l : lost) 
          people[l-1]--;
      for (int r : reserve) 
          people[r-1]++;

      // 상태를 다 나타낸 후에 0번부터 체육복 여부를 확인하고 체육복이 없다면 앞 번호나 뒷 번호에게 체육복을 빌리도록 합니다.
      // 단, 1번은 앞 번호가 존재하지 않으므로 뒷 번호에게만 빌릴 수 있고, 마지막 번호는 앞 번호에게만 빌릴 수 있습니다.
      for (int i = 0; i < people.length; i++) {
          if(people[i] == -1) {
              if(i-1>=0 && people[i-1] == 1) {
                  people[i]++;
                  people[i-1]--;
              }else if(i+1< people.length && people[i+1] == 1) {
                  people[i]++;
                  people[i+1]--;
              }else 
                  answer--;
          }
      }
      return answer;
  }

}