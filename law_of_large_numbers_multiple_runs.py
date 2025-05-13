#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大数の法則の確認 - 複数回の実験を実行して結果を比較
一様分布 U[0,1] に従う乱数を用いた数値実験
"""

import numpy as np
import matplotlib.pyplot as plt

def experiment(n):
    """
    一様分布 U[0,1] から n 個の乱数を生成し、0.4以下の割合を返す
    
    Parameters:
    -----------
    n : int
        実験回数
        
    Returns:
    --------
    float
        勝率（0.4以下の値の割合）
    """
    # 一様分布 U[0,1] から n 個の乱数を生成
    random_values = np.random.uniform(0, 1, n)
    
    # 0.4以下の値を「勝ち」とする
    wins = np.sum(random_values <= 0.4)
    
    # 勝率を計算
    win_rate = wins / n
    
    return win_rate

def run_multiple_experiments(num_runs=5):
    """
    複数回の実験を実行し、結果をプロットする
    
    Parameters:
    -----------
    num_runs : int
        実行する実験の回数
    """
    # 実験回数のリスト
    n_values = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
    
    # グラフの作成
    plt.figure(figsize=(12, 8))
    
    # 各実験の結果を格納する配列
    all_win_rates = np.zeros((num_runs, len(n_values)))
    
    # 複数回の実験を実行
    for run in range(num_runs):
        # 各実験回数で実験を実行
        win_rates = []
        for i, n in enumerate(n_values):
            win_rate = experiment(n)
            win_rates.append(win_rate)
            all_win_rates[run, i] = win_rate
            
        # 各実験の結果をプロット
        plt.plot(n_values, win_rates, 'o-', alpha=0.5, label=f'Run {run+1}')
    
    # 平均値を計算してプロット
    avg_win_rates = np.mean(all_win_rates, axis=0)
    plt.plot(n_values, avg_win_rates, 'ko-', linewidth=2, label='Average')
    
    # 理論値の水平線を追加
    plt.axhline(y=0.4, color='r', linestyle='--', linewidth=2, label='Theoretical Value (0.4)')
    
    # グラフの設定
    plt.xscale('log')  # x軸を対数スケールに
    plt.xlabel('Number of Experiments (n)')
    plt.ylabel('Win Rate')
    plt.title('Law of Large Numbers: Multiple Experimental Runs')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # y軸の範囲を理論値の周辺に設定
    plt.ylim(0.3, 0.5)
    
    # グラフの保存
    plt.savefig('law_of_large_numbers_multiple_runs.png')
    
    # グラフの表示
    plt.show()
    
    # 各実験回数における標準偏差を計算
    std_devs = np.std(all_win_rates, axis=0)
    
    # 結果を表示
    print("\n実験結果の統計:")
    print(f"{'n':>10} | {'平均勝率':>10} | {'標準偏差':>10} | {'理論値との差':>15}")
    print("-" * 50)
    for i, n in enumerate(n_values):
        print(f"{n:10d} | {avg_win_rates[i]:10.6f} | {std_devs[i]:10.6f} | {abs(avg_win_rates[i] - 0.4):15.6f}")
    
    print("\n考察:")
    print("1. 実験回数 n が増えるにつれて、勝率は理論値の0.4に近づいていきます。")
    print("2. 実験回数 n が増えるにつれて、異なる実験間のばらつき（標準偏差）が小さくなります。")
    print("3. n = 1000程度から勝率は理論値に近づき始め、n = 10000以上ではかなり安定します。")
    print("4. これらの結果は大数の法則を示しており、試行回数が増えるほど、観測される確率は理論的な確率に収束します。")

if __name__ == "__main__":
    # 乱数のシードを固定（再現性のため）
    np.random.seed(42)
    
    # 複数回の実験を実行
    run_multiple_experiments(num_runs=5)