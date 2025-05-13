#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大数の法則の確認
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

def main():
    # 実験回数のリスト
    n_values = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
    
    # 各実験回数における勝率を格納するリスト
    win_rates = []
    
    # 各実験回数で実験を実行
    for n in n_values:
        win_rate = experiment(n)
        win_rates.append(win_rate)
        print(f"n = {n:7d}, 勝率 = {win_rate:.6f}")
    
    # グラフの作成
    plt.figure(figsize=(10, 6))
    
    # 勝率の推移をプロット
    plt.plot(n_values, win_rates, 'o-', label='Experimental Results')
    
    # 理論値の水平線を追加
    plt.axhline(y=0.4, color='r', linestyle='--', label='Theoretical Value (0.4)')
    
    # グラフの設定
    plt.xscale('log')  # x軸を対数スケールに
    plt.xlabel('Number of Experiments (n)')
    plt.ylabel('Win Rate')
    plt.title('Law of Large Numbers: Relationship between Number of Experiments and Win Rate')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # y軸の範囲を理論値の周辺に設定
    plt.ylim(0.3, 0.5)
    
    # グラフの保存
    plt.savefig('law_of_large_numbers.png')
    
    # グラフの表示
    plt.show()
    
    print("\n考察:")
    print("グラフから、実験回数 n が増えるにつれて勝率が理論値の0.4に近づいていくことがわかります。")
    print("特に n が1000を超えると、勝率は理論値の周辺に安定してきます。")
    print("これは大数の法則を示しており、試行回数が増えるほど、観測される確率は理論的な確率に収束します。")

if __name__ == "__main__":
    # 乱数のシードを固定（再現性のため）
    np.random.seed(42)
    main()