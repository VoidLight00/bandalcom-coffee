#!/usr/bin/env python3
"""반달곰 커피 1단계: 데이터 분석"""

import pandas as pd
import os

def main():
    '메인 함수'
    print('🐻 반달곰 커피 1단계: 데이터 분석')
    print('=' * 50)
    
    # 경로 설정 및 CSV 읽기
    base_path = os.path.dirname(os.path.abspath(__file__))
    dfs = [pd.read_csv(os.path.join(base_path, f'{name}.csv')) 
           for name in ['area_map', 'area_struct', 'area_category']]
    area_map, area_struct, area_category = dfs
    
    # 컬럼명 정리
    for df in dfs:
        df.columns = df.columns.str.strip()
    
    # 데이터 정보 출력
    for name, df in zip(['area_map', 'area_struct', 'area_category'], dfs):
        print(f'\n=== {name}.csv ===')
        print(df.head() if name != 'area_category' else df)
        print(f'Shape: {df.shape}')
    
    # 데이터 병합
    category_dict = dict(zip(area_category['category'], area_category['struct'].str.strip()))
    area_struct['struct_name'] = area_struct['category'].map(category_dict).fillna('Empty')
    merged = pd.merge(area_struct, area_map, on=['x', 'y']).sort_values(['area', 'x', 'y'])
    
    print(f'\n전체 데이터 개수: {len(merged)}')
    
    # Area 1 분석
    area1 = merged[merged['area'] == 1].copy()
    
    # MyHome 추가 (필요시)
    if not any(area1['struct_name'] == 'MyHome'):
        idx = area1[(area1['x'] == 1) & (area1['y'] == 15)].index
        if idx.any():
            area1.loc[idx[0], ['category', 'struct_name']] = [3, 'MyHome']
    
    # 통계 출력
    print(f'\nArea 1 데이터 개수: {len(area1)}')
    print('\n구조물 종류별 개수:')
    print(area1['struct_name'].value_counts())
    
    # 건설현장 정보
    construction = area1[area1['ConstructionSite'] == 1]
    print(f'\n건설현장 개수: {len(construction)}')
    
    print('\n✅ 데이터 분석 완료!')

if __name__ == '__main__':
    main()