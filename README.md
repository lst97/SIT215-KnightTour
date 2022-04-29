# Knight Tour
This project is for Deakin SIT-215 Group 6 assessment using different approachs, including State Space Backtracking, Warnsdorff's Algorithm and Neural Network.

The complexit of each algorithm is Warnsdorff < Neural Network < Backtracking

For more information please visit:
| Algorithm | URL |
| ------ | ------ |
| ANN | https://github.com/NiloofarShahbaz/knight-tour-neural-network |
| Backtracking | https://www.youtube.com/watch?v=CQ3nDMcchdA |
| Warnsdorff | https://www.geeksforgeeks.org/warnsdorffs-algorithm-knights-tour-problem |

## Usage
+ **With GUI**
  + Install `pygame` and `numpy` library
  + run `main.py`
  + You can change the speed, color in `gui.py`
+ **Without GUI**
  + Add those code to bottom of `algorithm.py`
  + run `algorithm.py`
```python
# ANN
algo = KTAlgorithm.ANN(6)
algo.solve(0, 0, 1)
print(algo._solved_pool)

# BT
algo = KTAlgorithm.BT(6)
algo.solve(0, 0, 1)
print(algo._solved_pool)

# Warnsdorff
algo = KTAlgorithm.Warnsdorff(6)
algo.solve(0, 0, 1)
print(algo._solved_pool)
```
## Output
Only one solution will be calculated, for example in a 6 x 6 board
```
Searching for solution using Artificial Neural Networks...
Possible solution found (degree=2)...Droped!
Possible solution found (degree=2)...Droped!
Possible solution found (degree=2)...Valid!
[[(0, 0), (1, 2), (0, 4), (2, 3), (1, 5), (3, 4), (5, 5), (4, 3), (5, 1), (3, 0), (1, 1), (0, 3), (2, 4), (0, 5), (1, 3), (2, 5), (4, 4), (5, 2), (4, 0), (3, 2), (5, 3), (4, 5), (3, 3), (4, 1), (2, 0), (0, 1), (2, 2), (1, 4), (3, 5), (5, 4), (4, 2), (5, 0), (3, 1), (1, 0), (0, 2), (2, 1)]]
Searching for solution using BackTracking Algorithm...
[[[0, 0], [2, 1], [4, 2], [5, 4], [3, 5], [1, 4], [0, 2], [2, 3], [4, 4], [2, 5], [0, 4], [1, 2], [2, 4], [0, 5], [1, 3], [0, 1], [2, 0], [4, 1], [5, 3], [4, 5], [3, 3], [5, 2], [4, 0], [3, 2], [1, 1], [0, 3], [1, 5], [3, 4], [5, 5], [4, 3], [5, 1], [3, 0], [2, 2], [1, 0], [3, 1], [5, 0]]]
Searching for solution using Warnsdorff's Algorithm...
[[[0, 0], [1, 2], [0, 4], [2, 5], [4, 4], [5, 2], [4, 0], [2, 1], [0, 2], [1, 0], [3, 1], [5, 0], [4, 2], [5, 4], [3, 3], [1, 4], [3, 5], [2, 3], [1, 5], [0, 3], [1, 1], [3, 0], [5, 1], [4, 3], [5, 5], [3, 4], [2, 2], [4, 1], [5, 3], [4, 5], [2, 4], [0, 5], [1, 3], [3, 2], [2, 0], [0, 1]]]
```
## GUI example
![25x25](https://github.com/lst97/SIT215-KnightTour/blob/main/GUI_25x25.png?raw=true)
