#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中心極限定理のデモンストレーション
一様分布 U[0,1] からのサンプル平均の分布を調査
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def generate_sample_means(sample_size, num_experiments):
    """
    指定されたサンプルサイズで複数回の実験を行い、各実験のサンプル平均を返す
    
    Parameters:
    -----------
    sample_size : int
        各実験でのサンプルサイズ
    num_experiments : int
        実行する実験の回数
        
    Returns:
    --------
    numpy.ndarray
        各実験のサンプル平均の配列
    """
    # 各実験のサンプル平均を格納する配列
    sample_means = np.zeros(num_experiments)
    
    # 指定された回数の実験を実行
    for i in range(num_experiments):
        # 一様分布 U[0,1] からサンプルを生成
        samples = np.random.uniform(0, 1, sample_size)
        
        # サンプル平均を計算して格納
        sample_means[i] = np.mean(samples)
    
    return sample_means

def plot_sample_means_distribution(sample_sizes, num_experiments=10000):
    """
    異なるサンプルサイズでのサンプル平均の分布をプロットする
    
    Parameters:
    -----------
    sample_sizes : list
        調査するサンプルサイズのリスト
    num_experiments : int
        各サンプルサイズで実行する実験の回数
    """
    # グラフの行数と列数を計算
    n_rows = (len(sample_sizes) + 1) // 2
    n_cols = 2 if len(sample_sizes) > 1 else 1
    
    # グラフの作成
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows))
    
    # 1次元の場合は2次元に変換
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1 or n_cols == 1:
        axes = axes.reshape(n_rows, n_cols)
    
    # 一様分布 U[0,1] の理論的な平均と標準偏差
    theoretical_mean = 0.5
    theoretical_std = 1 / np.sqrt(12)  # 一様分布 U[0,1] の標準偏差
    
    # 各サンプルサイズでの分布をプロット
    for i, sample_size in enumerate(sample_sizes):
        row = i // 2
        col = i % 2
        
        # サンプル平均を生成
        sample_means = generate_sample_means(sample_size, num_experiments)
        
        # ヒストグラムをプロット
        axes[row, col].hist(sample_means, bins=50, density=True, alpha=0.7, 
                           label=f'Sample Means (n={sample_size})')
        
        # サンプル平均の標準偏差（理論値）
        std_of_mean = theoretical_std / np.sqrt(sample_size)
        
        # 対応する正規分布の確率密度関数をプロット
        x = np.linspace(0.3, 0.7, 1000)
        normal_pdf = stats.norm.pdf(x, theoretical_mean, std_of_mean)
        axes[row, col].plot(x, normal_pdf, 'r-', linewidth=2, 
                           label=f'Normal PDF\n(μ={theoretical_mean}, σ={std_of_mean:.4f})')
        
        # 実際のサンプル平均の平均と標準偏差を計算
        actual_mean = np.mean(sample_means)
        actual_std = np.std(sample_means)
        
        # グラフの設定
        axes[row, col].set_title(f'Distribution of Sample Means (n={sample_size})')
        axes[row, col].set_xlabel('Sample Mean')
        axes[row, col].set_ylabel('Density')
        axes[row, col].legend()
        axes[row, col].grid(True, alpha=0.3)
        
        # 統計情報をグラフに追加
        stats_text = (f'Actual Mean: {actual_mean:.4f}\n'
                     f'Actual Std: {actual_std:.4f}\n'
                     f'Theoretical Std: {std_of_mean:.4f}')
        axes[row, col].text(0.05, 0.95, stats_text, transform=axes[row, col].transAxes,
                           verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
    
    # 使用していないサブプロットを非表示にする
    for i in range(len(sample_sizes), n_rows * n_cols):
        row = i // 2
        col = i % 2
        fig.delaxes(axes[row, col])
    
    plt.tight_layout()
    plt.savefig('../images/central_limit_theorem.png')
    plt.show()
    
    print("\n考察:")
    print("1. サンプルサイズが大きくなるにつれて、サンプル平均の分布は正規分布に近づいています。")
    print("2. サンプルサイズが大きくなるにつれて、サンプル平均の標準偏差は小さくなっています。")
    print("3. 実際の標準偏差は理論値（σ/√n）に非常に近いことがわかります。")
    print("4. これは中心極限定理を示しており、元の分布が一様分布であっても、サンプル平均の分布は正規分布に近づきます。")

if __name__ == "__main__":
    # 乱数のシードを固定（再現性のため）
    np.random.seed(42)
    
    # 調査するサンプルサイズ
    sample_sizes = [1, 2, 5, 10, 30, 100]
    
    # サンプル平均の分布をプロット
    plot_sample_means_distribution(sample_sizes)