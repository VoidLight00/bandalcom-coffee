#!/usr/bin/env python3
'반달곰 커피 3단계: 최단 경로 탐색'

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch
import os
from collections import deque

def bfs_shortest_path(grid, start, goal):
    'BFS 알고리즘으로 최단 경로 찾기'
    queue = deque([(start, [start])])
    visited = {start}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    while queue:
        pos, path = queue.popleft()
        if pos == goal:
            return path
        
        for dx, dy in directions:
            next_pos = (pos[0] + dx, pos[1] + dy)
            if next_pos in grid and grid[next_pos] and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    return None

def draw_map_with_path(data, path):
    '경로가 포함된 지도 그리기'
    fig, ax = plt.subplots(figsize=(12, 10))
    max_x, max_y = data['x'].max(), data['y'].max()
    
    # 축 설정
    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, 0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('반달곰 커피 최단 경로', fontsize=16, fontweight='bold')
    
    # 그리드
    for i in range(1, max_x + 2):
        ax.axvline(x=i - 0.5, color='gray', alpha=0.3, linewidth=0.5)
        ax.axhline(y=i - 0.5, color='gray', alpha=0.3, linewidth=0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    
    # 건설현장
    for _, site in data[data['ConstructionSite'] == 1].iterrows():
        ax.add_patch(patches.Rectangle((site['x'] - 0.45, site['y'] - 0.45), 0.9, 0.9,
                                      facecolor='gray', alpha=0.5, edgecolor='darkgray'))
    
    # 구조물
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
    
    # 경로 그리기
    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.8)
        ax.plot(path_x, path_y, 'ro', markersize=5, alpha=0.6)
    
    # 범례
    ax.legend(handles=[
        Patch(facecolor='brown', edgecolor='darkred', label='Apartment/Building'),
        Patch(facecolor='green', edgecolor='darkgreen', label='BandalgomCoffee'),
        Patch(facecolor='lightgreen', edgecolor='darkgreen', label='MyHome'),
        Patch(facecolor='gray', edgecolor='darkgray', label='Construction Site'),
        plt.Line2D([0], [0], color='red', linewidth=3, label='Shortest Path')
    ], loc='lower right')
    
    return fig, ax

def main():
    '메인 함수'
    print('🚶 반달곰 커피 3단계: 최단 경로 탐색')
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
    
    # 시작점과 도착점 찾기
    my_home = merged_data[merged_data['struct_name'] == 'MyHome']
    coffees = merged_data[merged_data['struct_name'] == 'BandalgomCoffee']
    
    if my_home.empty or coffees.empty:
        print('오류: 시작점 또는 도착점을 찾을 수 없습니다.')
        return
    
    start = (my_home.iloc[0]['x'], my_home.iloc[0]['y'])
    print(f'시작점 (내 집): {start}')
    
    # 그리드 맵 생성
    grid = {(row['x'], row['y']): row['ConstructionSite'] != 1 
            for _, row in merged_data.iterrows()}
    
    # 가장 가까운 커피숍 찾기
    paths = [(bfs_shortest_path(grid, start, (c['x'], c['y'])), (c['x'], c['y'])) 
             for _, c in coffees.iterrows()]
    shortest = min((p for p in paths if p[0]), key=lambda x: len(x[0]))
    
    if shortest[0]:
        print(f'도착점 (반달곰 커피): {shortest[1]}')
        print(f'최단 경로 길이: {len(shortest[0]) - 1} 걸음')
        print('\n경로 좌표:')
        for i, (x, y) in enumerate(shortest[0]):
            print(f'  {i+1}. ({x}, {y})')
        
        # 지도 그리기 및 저장
        fig, ax = draw_map_with_path(merged_data, shortest[0])
        plt.tight_layout()
        output_path = os.path.join(os.path.dirname(base_path), 'results', 'map_final.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'\n최종 지도가 {output_path}로 저장되었습니다.')
    else:
        print('경로를 찾을 수 없습니다.')

if __name__ == '__main__':
    main()