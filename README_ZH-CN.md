
<div align="center">
  <img src="assets/logo.png" width=128></img>
  <p><strong>Next Generation Competitive Programming</strong></p>

[English](README.md) | [简体中文](README_ZH-CN.md)

[![Python 3.10](https://shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3109/)
[<img src="https://img.shields.io/badge/license-MIT-blue">](https://github.com/PurePassersBy/ShacoGym)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](https://github.com/PurePassersBy/ShacoGym)
[![lint](https://github.com/PurePassersBy/ShacoGym/actions/workflows/flake8_lint.yml/badge.svg)](https://github.com/PurePassersBy/ShacoGym/actions/workflows/flake8_lint.yml)
</div>


ShacoGym 旨在为下一代程序设计竞赛探索一种新的比赛机制。传统的程序设计竞赛，如 [codeforces](https://codeforces.com/) 和 [atcoder](https://atcoder.jp/)，要求选手使用最优化算法求解确定性问题。与之相对地，选手在 ShacoGym 需要解决具有以下特点的全新问题：

- :rainbow: **交互性的**
    - 每个问题都是一个交互式环境，你需要去实现一个智能体与环境交互，尽可能获得更高的奖励。
    - 在问题的开始，你没有足够完整的信息去充分解题，你需要在和问题的交互中，去探索并收集信息。根据你每次执行的动作不同，你可能会获得完全不同的信息。
- :zap: **非确定性的**
    - 在这里，没有确定性的标准答案（没有 AC 和 WA！），你只需要想办法在交互中提高你的奖励。
- :fire: **非最优化的**
    - 可能没有一个最优解法。


## 开始

```bash
conda create -n shacogym python=3.10
conda activate shacogym
pip install -r requirements.txt
```

## 解决问题

下面是一个求解 *Bandit* 问题的基线方法。 你可以从[这里](gym/problems/bandit/bandit.md)了解这个问题。

```bash
python entry.py --problem_name bandit --solution_file ./gym/problems/bandit/baseline.py
```

你可以复制 `baseline.py` 并且改进里面的算法，从而获得更高的奖励。请确保你参照基线方法，实现了一些必要的函数接口。

## 痛并快乐着

你可以亲自参与到问题的求解过程中，把问题当成一个游戏。[井字棋](gym/problems/tictactoe/tictactoe.md) 可以作为你在 ShacoGym 旅途的起点。

```bash
python entry.py --mode play --problem_name tictactoe
```

## 解题协议

这里有一些解题协议我们需要遵守:
1. 请不要下载除了在 `requirements.txt` 以外的第三方库。
2. 请不要尝试去破解代码本身。
3. 请不要翻阅实现问题的源代码。
