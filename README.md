# Netflix 사용자 데이터 분석 및 전처리

1. 주제 선정
- 넷플릭스 유저, 수익 기반 수익성 증대 방안
2. 목표 설정
- 대륙별, 성별, 연령별 수익 증가 방안
3. 주요 이해관계자
- 넷플릭스 경영진, 마케팅 부서 팀
4. 데이터셋 선택
    - 넷플릭스 유저베이스: https://www.kaggle.com/datasets/arnavsmayan/netflix-userbase-dataset
    - 국가별 넷플릭스 구독 비용: https://www.kaggle.com/datasets/prasertk/netflix-subscription-price-in-different-countries
5. 데이터 분석 및 전처리
    - Monthly Revenue 열 삭제
    - 등급에 대한 국가별 지불금액 컬럼 생성
    - Join Date, Last Payment Date 형식 변경
    - Plan Duration 열 삭제
    - Age 열 범주화
    - Country열 대륙별 범주화
    - 국가별 보유 프로그램 수 매칭 후 열 삽입
6. 대시보드 구성 및 설계
    - 대시보드 도구 태블로 사용
    - 대륙에 대해 등급별 수익의 합
    - 성별에 대해 사용 디바이스별 수익의 합
7. 프로젝트 타임라인 설정 및 팀원 역할 분담
    
    금  데이터/ 주제선정
    
    월  전처리
    
    화  전처리 태블로
    
    수  PPT  만들기
    
    목 오전 발표준비 및 확인 오후 발표
    
    - 팀원 역할분담
        - 권지혁: 등급에 대한 국가별 지불금액 컬럼 생성
        - 강나현: 나이 열 범주화
        - 조희찬: 국가 / 대륙 범주화 및 컬럼 생성
        - 하선영: 날짜 형식 변경, 발표
