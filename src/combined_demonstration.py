#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大数の法則と中心極限定理の組み合わせデモンストレーション
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def run_experiment(sample_sizes, num_experiments=1000):
    """
    異なるサンプルサイズでの実験を実行し、結果をプロットする
    
    Parameters:
    -----------
    sample_sizes : list
        調査するサンプルサイズのリスト
    num_experiments : int
        各サンプルサイズで実行する実験の回数
    """
    # 理論値
    theoretical_prob = 0.4
    
    # 結果を格納する配列
    win_rates = np.zeros((len(sample_sizes), num_experiments))
    
    # 各サンプルサイズで実験を実行
    for i, n in enumerate(sample_sizes):
        for j in range(num_experiments):
            # 一様分布 U[0,1] から n 個の乱数を生成
            random_values = np.random.uniform(0, 1, n)
            
            # 0.4以下の値を「勝ち」とする
            wins = np.sum(random_values <= 0.4)
            
            # 勝率を計算
            win_rates[i, j] = wins / n
    
    # グラフの作成
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. 大数の法則: 各サンプルサイズでの平均勝率
    mean_win_rates = np.mean(win_rates, axis=1)
    axes[0, 0].plot(sample_sizes, mean_win_rates, 'o-', linewidth=2)
    axes[0, 0].axhline(y=theoretical_prob, color='r', linestyle='--', 
                      label=f'Theoretical Probability ({theoretical_prob})')
    axes[0, 0].set_xscale('log')
    axes[0, 0].set_xlabel('Sample Size (n)')
    axes[0, 0].set_ylabel('Average Win Rate')
    axes[0, 0].set_title('Law of Large Numbers: Convergence to Theoretical Probability')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # 2. 大数の法則: 各サンプルサイズでの標準偏差
    std_win_rates = np.std(win_rates, axis=1)
    axes[0, 1].plot(sample_sizes, std_win_rates, 'o-', linewidth=2)
    
    # 理論的な標準偏差: sqrt(p(1-p)/n)
    theoretical_std = np.sqrt(theoretical_prob * (1 - theoretical_prob) / np.array(sample_sizes))
    axes[0, 1].plot(sample_sizes, theoretical_std, 'r--', 
                   label='Theoretical Std: sqrt(p(1-p)/n)')
    
    axes[0, 1].set_xscale('log')
    axes[0, 1].set_yscale('log')
    axes[0, 1].set_xlabel('Sample Size (n)')
    axes[0, 1].set_ylabel('Standard Deviation of Win Rate')
    axes[0, 1].set_title('Decreasing Variability with Increasing Sample Size')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # 3. 中心極限定理: 勝率の分布 (小さいサンプルサイズ)
    small_n_index = 2  # サンプルサイズが小さい場合のインデックス
    small_n = sample_sizes[small_n_index]
    
    axes[1, 0].hist(win_rates[small_n_index], bins=30, density=True, alpha=0.7,
                   label=f'Win Rate Distribution (n={small_n})')
    
    # 対応する正規分布
    x = np.linspace(0.2, 0.6, 1000)
    mean = theoretical_prob
    std = np.sqrt(theoretical_prob * (1 - theoretical_prob) / small_n)
    normal_pdf = stats.norm.pdf(x, mean, std)
    axes[1, 0].plot(x, normal_pdf, 'r-', linewidth=2, 
                   label=f'Normal PDF (μ={mean}, σ={std:.4f})')
    
    axes[1, 0].set_xlabel('Win Rate')
    axes[1, 0].set_ylabel('Density')
    axes[1, 0].set_title(f'Central Limit Theorem: Win Rate Distribution (n={small_n})')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # 4. 中心極限定理: 勝率の分布 (大きいサンプルサイズ)
    large_n_index = -1  # サンプルサイズが大きい場合のインデックス
    large_n = sample_sizes[large_n_index]
    
    axes[1, 1].hist(win_rates[large_n_index], bins=30, density=True, alpha=0.7,
                   label=f'Win Rate Distribution (n={large_n})')
    
    # 対応する正規分布
    x = np.linspace(0.35, 0.45, 1000)
    mean = theoretical_prob
    std = np.sqrt(theoretical_prob * (1 - theoretical_prob) / large_n)
    normal_pdf = stats.norm.pdf(x, mean, std)
    axes[1, 1].plot(x, normal_pdf, 'r-', linewidth=2, 
                   label=f'Normal PDF (μ={mean}, σ={std:.4f})')
    
    axes[1, 1].set_xlabel('Win Rate')
    axes[1, 1].set_ylabel('Density')
    axes[1, 1].set_title(f'Central Limit Theorem: Win Rate Distribution (n={large_n})')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('../images/combined_demonstration.png')
    plt.show()
    
    # 結果の統計情報を表示
    print("\n統計情報:")
    print(f"{'サンプルサイズ':>15} | {'平均勝率':>10} | {'標準偏差':>10} | {'理論標準偏差':>15}")
    print("-" * 60)
    for i, n in enumerate(sample_sizes):
        theo_std = np.sqrt(theoretical_prob * (1 - theoretical_prob) / n)
        print(f"{n:15d} | {mean_win_rates[i]:10.6f} | {std_win_rates[i]:10.6f} | {theo_std:15.6f}")
    
    print("\n考察:")
    print("1. 大数の法則: サンプルサイズが大きくなるにつれて、平均勝率は理論値の0.4に収束します。")
    print("2. 標準偏差: サンプルサイズが大きくなるにつれて、勝率のばらつきは理論値に従って減少します。")
    print("3. 中心極限定理: サンプルサイズが大きくなるにつれて、勝率の分布は正規分布に近づきます。")
    print("4. 両方の法則は互いに関連しており、大数の法則は平均値の収束を、中心極限定理は分布の形状を説明しています。")

if __name__ == "__main__":
    # 乱数のシードを固定（再現性のため）
    np.random.seed(42)
    
    # 調査するサンプルサイズ
    sample_sizes = [10, 30, 50, 100, 300, 500, 1000, 3000]
    
    # 実験を実行
    run_experiment(sample_sizes)