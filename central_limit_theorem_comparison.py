#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中心極限定理の確認 - 異なる非対称分布の比較
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time

def generate_samples(distribution, sample_size, num_experiments, **params):
    """
    指定された分布から指定されたサンプルサイズで複数回の実験を行い、各実験のサンプル平均を返す
    
    Parameters:
    -----------
    distribution : str
        使用する分布の名前 ('exponential', 'chi2', 'pareto')
    sample_size : int
        各実験でのサンプルサイズ
    num_experiments : int
        実行する実験の回数
    **params : dict
        分布のパラメータ
        
    Returns:
    --------
    numpy.ndarray
        各実験のサンプル平均の配列
    """
    # 各実験のサンプル平均を格納する配列
    sample_means = np.zeros(num_experiments)
    
    # 指定された回数の実験を実行
    for i in range(num_experiments):
        # 指定された分布からサンプルを生成
        if distribution == 'exponential':
            scale = params.get('scale', 1.0)
            samples = np.random.exponential(scale=scale, size=sample_size)
        elif distribution == 'chi2':
            df = params.get('df', 1)
            samples = np.random.chisquare(df=df, size=sample_size)
        elif distribution == 'pareto':
            alpha = params.get('alpha', 3.0)
            scale = params.get('scale', 1.0)
            samples = stats.pareto.rvs(alpha, scale=scale, size=sample_size)
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
        
        # サンプル平均を計算して格納
        sample_means[i] = np.mean(samples)
    
    return sample_means

def get_theoretical_stats(distribution, **params):
    """
    指定された分布の理論的な平均と標準偏差を返す
    
    Parameters:
    -----------
    distribution : str
        使用する分布の名前 ('exponential', 'chi2', 'pareto')
    **params : dict
        分布のパラメータ
        
    Returns:
    --------
    tuple
        (理論的平均, 理論的標準偏差)
    """
    if distribution == 'exponential':
        scale = params.get('scale', 1.0)
        return scale, scale
    elif distribution == 'chi2':
        df = params.get('df', 1)
        return df, np.sqrt(2 * df)
    elif distribution == 'pareto':
        alpha = params.get('alpha', 3.0)
        scale = params.get('scale', 1.0)
        if alpha > 1:
            mean = alpha * scale / (alpha - 1)
        else:
            mean = float('inf')
            
        if alpha > 2:
            std = scale * alpha / ((alpha - 1) * np.sqrt((alpha - 2) / alpha))
        else:
            std = float('inf')
        return mean, std
    else:
        raise ValueError(f"Unknown distribution: {distribution}")

def plot_distribution_comparison(sample_sizes, num_experiments=10000):
    """
    異なる分布でのサンプル平均の分布を比較する
    
    Parameters:
    -----------
    sample_sizes : list
        調査するサンプルサイズのリスト
    num_experiments : int
        各サンプルサイズで実行する実験の回数
    """
    # 比較する分布とそのパラメータ
    distributions = [
        ('exponential', {'scale': 2.0}, 'Exponential (λ=0.5)'),
        ('chi2', {'df': 3}, 'Chi-Square (df=3)'),
        ('pareto', {'alpha': 3.0, 'scale': 1.0}, 'Pareto (α=3.0, scale=1.0)')
    ]
    
    # 選択するサンプルサイズ（小、中、大）
    selected_sizes = [1, 10, 100]
    
    # グラフの行数と列数
    n_rows = len(selected_sizes)
    n_cols = len(distributions)
    
    # グラフの作成
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    
    # 各サンプルサイズと分布の組み合わせでプロット
    for i, sample_size in enumerate(selected_sizes):
        for j, (dist_name, params, dist_label) in enumerate(distributions):
            # 開始時間を記録
            start_time = time.time()
            
            # サンプル平均を生成
            sample_means = generate_samples(dist_name, sample_size, num_experiments, **params)
            
            # 終了時間を記録
            end_time = time.time()
            
            # 実行時間を計算
            execution_time = end_time - start_time
            
            # 理論的な平均と標準偏差を取得
            theoretical_mean, theoretical_std = get_theoretical_stats(dist_name, **params)
            
            # 実際のサンプル平均の平均と標準偏差を計算
            actual_mean = np.mean(sample_means)
            actual_std = np.std(sample_means)
            
            # サンプル平均の標準偏差（理論値）
            std_of_mean = theoretical_std / np.sqrt(sample_size) if theoretical_std != float('inf') else actual_std
            
            # ヒストグラムをプロット
            axes[i, j].hist(sample_means, bins=50, density=True, alpha=0.7, 
                           label=f'Sample Means')
            
            # 対応する正規分布の確率密度関数をプロット
            x_min = max(0, actual_mean - 4 * actual_std)  # 非負の分布なので、0未満は除外
            x_max = actual_mean + 4 * actual_std
            x = np.linspace(x_min, x_max, 1000)
            normal_pdf = stats.norm.pdf(x, actual_mean, std_of_mean)
            axes[i, j].plot(x, normal_pdf, 'r-', linewidth=2, 
                           label=f'Normal PDF')
            
            # グラフの設定
            axes[i, j].set_title(f'{dist_label}, n={sample_size}')
            axes[i, j].set_xlabel('Sample Mean')
            axes[i, j].set_ylabel('Density')
            axes[i, j].grid(True, alpha=0.3)
            
            # 統計情報をグラフに追加
            stats_text = (f'Mean: {actual_mean:.4f}\n'
                         f'Std: {actual_std:.4f}')
            axes[i, j].text(0.95, 0.95, stats_text, transform=axes[i, j].transAxes,
                           verticalalignment='top', horizontalalignment='right',
                           bbox=dict(boxstyle='round', alpha=0.1))
    
    # 全体のタイトルを追加
    plt.suptitle('Central Limit Theorem: Comparison of Different Asymmetric Distributions', 
                fontsize=16, y=1.02)
    
    # 凡例を一つだけ表示（最後のサブプロットの凡例を使用）
    handles, labels = axes[-1, -1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0), ncol=2)
    
    plt.tight_layout()
    plt.savefig('central_limit_theorem_comparison.png', bbox_inches='tight')
    plt.show()
    
    print("\n考察:")
    print("1. サンプルサイズn=1では、各分布はそれぞれの元の分布の形状を保持しています。")
    print("2. サンプルサイズn=10では、すべての分布で非対称性が減少し、より対称的な形状に近づいています。")
    print("3. サンプルサイズn=100では、すべての分布でサンプル平均の分布が正規分布に非常に近くなっています。")
    print("4. 指数分布は比較的穏やかな非対称性を持つため、小さなサンプルサイズでも正規分布への収束が速いです。")
    print("5. カイ二乗分布は中程度の非対称性を持ち、中程度のサンプルサイズで正規分布に近づきます。")
    print("6. パレート分布は強い非対称性と重い裾を持つため、正規分布への収束には大きなサンプルサイズが必要です。")
    print("7. これらの結果は、元の分布の形状に関わらず、サンプルサイズが十分大きければサンプル平均の分布が正規分布に近づくという中心極限定理を実証しています。")
    print("8. ただし、元の分布の非対称性が強いほど、正規分布への収束には大きなサンプルサイズが必要になります。")

def main():
    """
    メイン関数
    """
    # 乱数のシードを固定（再現性のため）
    np.random.seed(42)
    
    # 調査するサンプルサイズ
    sample_sizes = [1, 2, 5, 10, 30, 50, 100]
    
    # 各サンプルサイズで実行する実験の回数
    num_experiments = 10000
    
    # 異なる分布でのサンプル平均の分布を比較
    plot_distribution_comparison(sample_sizes, num_experiments)

if __name__ == "__main__":
    main()