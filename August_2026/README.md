# Jane Street August 2026 Puzzle

This is my solution to Jane Street's August 2026 puzzle, "Andy's Afternoon Amble".

## What the puzzle is

Andy the ant lives on a small ball shape made of 4 white hexagons and 4 black triangles (a truncated tetrahedron). He only ever walks between white hexagons, since he thinks the black triangles might be pits. Every afternoon he wakes up on a white hexagon, calls it home, and takes a random walk, picking one of the 3 neighboring white hexagons at each step with equal chance. He stops as soon as he lands back on home.

This time his ball bounces onto an endless flat floor tiled with black and white hexagons, and he falls off onto it without noticing. He does the same walk using the same rule. He remembers the turns he takes though, left, right, or straight back, not the actual directions. The question is the chance that by the time his walk ends, the sequence of turns he took proves he can't still be on the small ball, meaning the pattern only makes sense if he's on the endless floor.

Puzzle page: [Jane Street's puzzle archive](https://www.janestreet.com/puzzles/archive/)

## What I did

This puzzle references an older one from July 2022, "Andy's Morning Stroll", where Andy lives on a soccer ball instead. I solved that one first for fun and to see if it gave me any hints.

On the soccer ball, the white hexagons and how they connect form what's called a positive recurrent Markov chain. That let me use Kac's return time formula to work out the expected number of steps for Andy's walk to end, which comes out to 20. I then built a small model of the infinite hexagon floor using axial coordinates, a standard way to lay out a hex grid with numbers, and worked out the chance his walk on the floor takes more steps than 20. I got 0.4480326, which matched the answer Jane Street had already posted for that puzzle, so I knew my approach worked before moving to the real one.

For the real puzzle, the ball only has 4 white hexagons, and each one connects to all 3 others. That's just a complete graph on 4 points, so I represented the ball that way instead of dealing with the actual 3D shape.

The main trick is that Andy remembers turns, not directions. So for both the ball graph and the hexagon floor, I set up a fixed order around each point so that "left" and "right" could always be worked out just from which edge he arrived on, no matter where he was.

Then I ran the same sequence of random turns on both worlds at the same time. Andy is really on the floor, so his walk ends whenever he gets back to home there. What I'm checking at each step is whether the ball version would also be home at that same point. If yes, nothing gave him away yet. If only one of the two is home, that's the exact point where the turns he's taken could only make sense on the floor, not the ball. Adding up the chance of that happening gives the answer.

## Files

- `andys_morning_stroll_2022.py` - solves the older July 2022 puzzle as a warm up. Works out the expected number of steps on the soccer ball, then the chance the floor version takes more steps than that.
- `andys_afternoon_amble_2026.py` - the actual solver. Builds the ball as a 4 point graph, sets up the left/right/back rule for both worlds, then walks both together and adds up the chance of a mismatch.

## How to run it

You need Python, nothing else.

Run either file directly:


`python JS_07-2022_BFS.py`\
`python JS_08-Algorithm.py`


The first one prints the return-count numbers and the final probability. The second one prints the detected probability and how much probability is still unresolved after 7777 steps (a tiny bit is left over since the walk can technically run forever, this just tells you how much of the total is still unaccounted for).

## Answer

### 0.55
