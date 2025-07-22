#!/usr/bin/env python3
'반달곰 커피 2단계: 지도 시각화'

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch
import os

def draw_map(data):
    '지도를 그리고 시각화합니다.'
    fig, ax = plt.subplots(figsize=(12, 10))
    max_x, max_y = data['x'].max(), data['y'].max()
    
    # 축 설정
    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, 0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('반달곰 커피 지도', fontsize=16, fontweight='bold')
    
    # 그리드
    for i in range(1, max_x + 2):
        ax.axvline(x=i - 0.5, color='gray', alpha=0.3, linewidth=0.5)
    for i in range(1, max_y + 2):
        ax.axhline(y=i - 0.5, color='gray', alpha=0.3, linewidth=0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    
    # 건설현장 그리기
    for _, site in data[data['ConstructionSite'] == 1].iterrows():
        ax.add_patch(patches.Rectangle((site['x'] - 0.45, site['y'] - 0.45), 0.9, 0.9,
                                      facecolor='gray', alpha=0.5, edgecolor='darkgray'))
    
    # 구조물 그리기
    shapes = {
        'Apartment': lambda x, y: plt.Circle((x, y), 0.3, facecolor='brown', alpha=0.8, edgecolor='darkred'),
        'Building': lambda x, y: plt.Circle((x, y), 0.3, facecolor='brown', alpha=0.8, edgecolor='darkred'),
        'BandalgomCoffee': lambda x, y: patches.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6,
                                                         facecolor='green', alpha=0.8, edgecolor='darkgreen'),
        'MyHome': lambda x, y: patches.RegularPolygon((x, y), 3, radius=0.35,
                                                     facecolor='lightgreen', alpha=0.8, edgecolor='darkgreen')
    }
    
    for _, row in data.iterrows():
        if row.get('struct_name') in shapes and row['ConstructionSite'] != 1:
            ax.add_patch(shapes[row['struct_name']](row['x'], row['y']))
    
    # 범례
    ax.legend(handles=[
        Patch(facecolor='brown', edgecolor='darkred', label='Apartment/Building'),
        Patch(facecolor='green', edgecolor='darkgreen', label='BandalgomCoffee'),
        Patch(facecolor='lightgreen', edgecolor='darkgreen', label='MyHome'),
        Patch(facecolor='gray', edgecolor='darkgray', label='Construction Site')
    ], loc='lower right')
    
    return fig, ax

def main():
    '메인 함수'
    print('🗺️ 반달곰 커피 2단계: 지도 시각화')
    print('=' * 50)
    
    # 데이터 로드
    base_path = os.path.dirname(os.path.abspath(__file__))
    dfs = [pd.read_csv(os.path.join(base_path, f'{n}.csv')) for n in ['area_map', 'area_struct', 'area_category']]
    for df in dfs:
        df.columns = df.columns.str.strip()
    
    # 데이터 병합
    area_map, area_struct, area_category = dfs
    category_dict = dict(zip(area_category['category'], area_category['struct'].str.strip()))
    area_struct['struct_name'] = area_struct['category'].map(category_dict).fillna('Empty')
    merged_data = pd.merge(area_struct, area_map, on=['x', 'y'])
    
    print(f'데이터 불러오기 완료: {len(merged_data)}개 좌표')
    
    # 구조물 위치 출력
    print('\nCSV 파일에 있는 구조물 위치:')
    for _, row in merged_data[merged_data['category'] != 0].sort_values(['x', 'y']).iterrows():
        if row['struct_name'] != 'Empty':
            struct_name = row['struct_name']
            x = row['x']
            y = row['y']
            print(f'  {struct_name}: ({x}, {y})')
    
    # 지도 그리기 및 저장
    fig, ax = draw_map(merged_data)
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(base_path), 'results', 'map.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'\n지도가 {output_path}로 저장되었습니다.')

if __name__ == '__main__':
    main()