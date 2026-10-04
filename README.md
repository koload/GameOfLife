# Conway's Game of Life

An implementation of John Conway's classic "Game of Life," written in Python using the Pygame library.

## What is the Game of Life?
The Game of Life is a famous cellular automaton devised by the British mathematician John Conway in 1970. It is a "zero-player game," meaning its evolution is determined entirely by its initial state, requiring no further input from human players.

The "board" is a grid of square cells, each of which can be in one of two states: **alive** or **dead**. Every cell interacts with its eight neighbors (horizontally, vertically, and diagonally).

## Turing Completeness
Though it has no traditional goals or rules, the Game of Life is **Turing complete**. Because precise streams of gliders can be manipulated to construct logic gates (like AND, OR, and NOT), the system possesses the full computational power of a real computer. In theory, it is possible to build and run any computer program—including another simulation of the Game of Life itself—entirely out of interacting cells on this grid.

## Rules
In each cycle (generation), the entire grid updates simultaneously based on four simple rules:
1. **Underpopulation:** Any live cell with fewer than two live neighbors dies.
2. **Survival:** Any live cell with two or three live neighbors lives on to the next generation.
3. **Overpopulation:** Any live cell with more than three live neighbors dies.
4. **Reproduction:** Any dead cell with exactly three live neighbors becomes a live cell.

From these incredibly simple rules, complex, infinite, and fascinating patterns emerge—such as spaceships, oscillators, and guns.

## Features
- **Manual Drawing:** Left mouse button adds cells, right mouse button removes them (hold `Shift` to draw straight lines).
- **Controls:** Start/Stop buttons to control the flow of time.
- **Built-in Patterns:** Quick insertion of famous structures (Glider, Pulsar, Spaceship, Gosper Gun, Upward Gun).
- **Randomness:** Generate a random board state using a density slider.
