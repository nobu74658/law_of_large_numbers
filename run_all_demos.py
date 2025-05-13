#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
すべてのデモンストレーションを実行するスクリプト（ルートディレクトリ用）
"""

import os
import sys

# srcディレクトリへのパスを追加
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# srcディレクトリのrun_all_demos.pyをインポート
from run_all_demos import main

if __name__ == "__main__":
    main()