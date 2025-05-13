#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中心極限定理の確認 - 左右非対称な分布（指数分布）を用いた実験
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time

def generate_sample_means(sample_size, num_experiments, scale=1.0):
    """
    指定されたサンプルサイズで複数回の実験を行い、各実験のサンプル平均を返す
    
    Parameters:
    -----------
    sample_size : int
        各実験でのサンプルサイズ
    num_experiments : int
        実行する実験の回数
    scale : float
        指数分布のスケールパラメータ（1/λ）
        
    Returns:
    --------
    numpy.ndarray
        各実験のサンプル平均の配列
    """
    # 各実験のサンプル平均を格納する配列
    sample_means = np.zeros(num_experiments)
    
    # 指定された回数の実験を実行
    for i in range(num_experiments):
        # 指数分布からサンプルを生成
        samples = np.random.exponential(scale=scale, size=sample_size)
        
        # サンプル平均を計算して格納
        sample_means[i] = np.mean(samples)
    
    return sample_means

def plot_sample_means_distribution(sample_sizes, num_experiments=10000, scale=1.0):
    """
    異なるサンプルサイズでのサンプル平均の分布をプロットする
    
    Parameters:
    -----------
    sample_sizes : list
        調査するサンプルサイズのリスト
    num_experiments : int
        各サンプルサイズで実行する実験の回数
    scale : float
        指数分布のスケールパラメータ（1/λ）
    """
    # 指数分布の理論的な平均と標準偏差
    theoretical_mean = scale
    theoretical_std = scale  # 指数分布の標準偏差はスケールパラメータに等しい
    
    # グラフの行数と列数を計算
    n_rows = (len(sample_sizes) + 1) // 2
    n_cols = 2 if len(sample_sizes) > 1 else 1
    
    # グラフの作成
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    
    # 1次元の場合は2次元に変換
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1 or n_cols == 1:
        axes = axes.reshape(n_rows, n_cols)
    
    # 各サンプルサイズでの分布をプロット
    for i, sample_size in enumerate(sample_sizes):
        row = i // 2
        col = i % 2
        
        # 開始時間を記録
        start_time = time.time()
        
        # サンプル平均を生成
        sample_means = generate_sample_means(sample_size, num_experiments, scale)
        
        # 終了時間を記録
        end_time = time.time()
        
        # 実行時間を計算
        execution_time = end_time - start_time
        
        # ヒストグラムをプロット
        hist_data = axes[row, col].hist(sample_means, bins=50, density=True, alpha=0.7, 
                                       label=f'Sample Means (n={sample_size})')
        
        # サンプル平均の標準偏差（理論値）
        std_of_mean = theoretical_std / np.sqrt(sample_size)
        
        # 対応する正規分布の確率密度関数をプロット
        x_min = max(0, theoretical_mean - 4 * std_of_mean)  # 指数分布は正の値のみなので、0未満は除外
        x_max = theoretical_mean + 4 * std_of_mean
        x = np.linspace(x_min, x_max, 1000)
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
                     f'Theoretical Std: {std_of_mean:.4f}\n'
                     f'Execution Time: {execution_time:.2f}s')
        axes[row, col].text(0.95, 0.95, stats_text, transform=axes[row, col].transAxes,
                           verticalalignment='top', horizontalalignment='right',
                           bbox=dict(boxstyle='round', alpha=0.1))
    
    # 使用していないサブプロットを非表示にする
    for i in range(len(sample_sizes), n_rows * n_cols):
        row = i // 2
        col = i % 2
        fig.delaxes(axes[row, col])
    
    # 全体のタイトルを追加
    plt.suptitle(f'Central Limit Theorem with Exponential Distribution (λ={1/scale:.2f})', 
                fontsize=16, y=1.02)
    
    plt.tight_layout()
    plt.savefig('central_limit_theorem_exponential.png', bbox_inches='tight')
    plt.show()
    
    print("\n考察:")
    print("1. サンプルサイズが小さい場合（n=1, 2, 5）、サンプル平均の分布は指数分布の形状を保持しており、左右非対称です。")
    print("2. サンプルサイズが大きくなる（n=10, 30, 50, 100）につれて、分布は徐々に対称的な形状になり、正規分布に近づいています。")
    print("3. n=30以上では、サンプル平均の分布はほぼ正規分布と一致しています。")
    print("4. 実際の標準偏差は理論値（σ/√n）に非常に近いことがわかります。")
    print("5. これは中心極限定理が左右非対称な分布（この場合は指数分布）に対しても成り立つことを示しています。")
    print("6. 元の分布が非対称であっても、サンプルサイズが十分大きければ、サンプル平均の分布は正規分布に近づきます。")

def main():
    """
    メイン関数
    """
    # 乱数のシードを固定（再現性のため）
    np.random.seed(42)
    
    # 指数分布のスケールパラメータ（1/λ）
    scale = 2.0  # 平均 = 2.0, 標準偏差 = 2.0
    
    # 調査するサンプルサイズ
    sample_sizes = [1, 2, 5, 10, 30, 50, 100]
    
    # 各サンプルサイズで実行する実験の回数
    num_experiments = 10000
    
    # サンプル平均の分布をプロット
    plot_sample_means_distribution(sample_sizes, num_experiments, scale)

if __name__ == "__main__":
    main()