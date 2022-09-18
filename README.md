# HTN2022_MR.Goose

Reinforcement learning project made during hack the north 2022

It uses the Q-Learning RL algorithm for the Goose to learn itself and find the best path to reach it's prey(aka UWaterloo student).

We harnessed reinforcement learning strategies in Python to have Mr. Goose learn from every successful attack of a Waterloo student. 
Using libraries such as Tkinter, NumPy, Sys and Pandas we were able to display a visual design with a grid, walls, grass and cages. 

https://user-images.githubusercontent.com/67829842/190891936-b0e03bb4-2f4d-4172-be4e-f04e586c1940.mp4

Detailed rewarding strategy:
- +5 for the final target (terminate round)
- -1 for stepping into the trap (terminate the round)
- -0.8 for going out of the grid
- -0.4 for bumping on the wall
- -0.25 for revisited cell
- -0.01 for blank cell
