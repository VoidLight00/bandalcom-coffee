# 🐻 반달곰 커피 (Bandalcom Coffee) Map Project

반달곰 커피 지도 프로젝트 - BFS 알고리즘을 사용한 최단 경로 탐색 시각화

## 📋 프로젝트 개요

이 프로젝트는 15x15 격자 지도에서 집에서 가장 가까운 반달곰 커피숍까지의 최단 경로를 찾는 프로그램입니다.

### 주요 기능
- CSV 데이터 분석 및 처리 (pandas)
- 지도 시각화 (matplotlib)
- BFS 알고리즘을 활용한 최단 경로 탐색
- 건설현장을 피해서 이동하는 경로 계산

## 🗂️ 파일 구조

```
src/
├── caffee_map.py         # 1단계: 데이터 분석
├── map_draw.py           # 2단계: 지도 시각화
├── map_direct_save.py    # 3단계: 최단 경로 탐색
├── area_map.csv          # 지도 좌표 및 건설현장 정보
├── area_struct.csv       # 구조물 위치 정보
└── area_category.csv     # 구조물 카테고리 정보
```

## 🚀 실행 방법

### 필요 라이브러리
```bash
pip install pandas matplotlib
```

### 개별 실행
```bash
# 1단계: 데이터 분석
python caffee_map.py

# 2단계: 지도 시각화
python map_draw.py

# 3단계: 최단 경로 탐색
python map_direct_save.py
```

## 📊 출력 결과

1. **map.png**: 전체 지도 시각화
   - 아파트/빌딩 (갈색 원)
   - 반달곰 커피 (녹색 사각형)
   - 내 집 (연한 녹색 삼각형)
   - 건설현장 (회색 사각형)

2. **map_final.png**: 최단 경로가 표시된 지도
   - 빨간색 선으로 최단 경로 표시

## 🎯 구조물 위치

- MyHome: (14, 2)
- BandalgomCoffee: (2, 12), (3, 12)
- 여러 아파트와 빌딩
- 건설현장 (이동 불가 지역)

## 📐 알고리즘

BFS(Breadth-First Search) 알고리즘을 사용하여:
1. 시작점(집)에서 모든 가능한 경로 탐색
2. 건설현장을 피해서 이동
3. 가장 가까운 커피숍까지의 최단 경로 계산

## 📝 코드 스타일

- PEP 8 가이드라인 준수
- 함수명: snake_case
- 문자열: 작은따옴표(') 사용
- 들여쓰기: 공백 4칸

## 📄 라이선스

이 프로젝트는 교육 목적으로 작성되었습니다.