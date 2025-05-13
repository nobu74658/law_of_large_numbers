#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
すべてのデモンストレーションを実行するスクリプト
"""

import os
import subprocess
import time

def run_demo(script_name, description):
    """
    デモンストレーションスクリプトを実行する
    
    Parameters:
    -----------
    script_name : str
        実行するPythonスクリプトのファイル名
    description : str
        デモンストレーションの説明
    """
    print("\n" + "=" * 80)
    print(f"実行中: {description}")
    print("=" * 80)
    
    # スクリプトを実行
    start_time = time.time()
    subprocess.run(["python", script_name])
    end_time = time.time()
    
    print(f"\n実行時間: {end_time - start_time:.2f} 秒")
    print("=" * 80)
    
    # ユーザーに次のデモに進む前に一時停止する
    input("\nEnterキーを押して次のデモに進む...")

def main():
    """
    すべてのデモンストレーションを順番に実行する
    """
    # 現在のディレクトリを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 元のディレクトリを保存
    original_dir = os.getcwd()
    
    try:
        # スクリプトのディレクトリに移動
        os.chdir(current_dir)
        
        # 1. 大数の法則（単一実験）
        run_demo("law_of_large_numbers.py", "大数の法則 - 単一実験")
        
        # 2. 大数の法則（複数実験）
        run_demo("law_of_large_numbers_multiple_runs.py", "大数の法則 - 複数実験")
        
        # 3. 中心極限定理
        run_demo("central_limit_theorem.py", "中心極限定理")
        
        # 4. 組み合わせデモンストレーション
        run_demo("combined_demonstration.py", "大数の法則と中心極限定理の組み合わせ")
        
        print("\nすべてのデモンストレーションが完了しました！")
        
    finally:
        # 元のディレクトリに戻る
        os.chdir(original_dir)

if __name__ == "__main__":
    main()