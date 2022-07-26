## Tetris Game 


# Table of Components 

1. Installation & Running 
2. Checkpoints 
3. Usage of the Program 


# Installation and Running 

*Installation* 
- activate your conda environment 
- make sure the required libraries (random, copy, pygame) are Installed 
 
*Running*   
The program is divided into 3 files containing python code: 'main', 'Tetris', and 'Tetrominoes'. While the 'Tetrominoes' class manages the construction of new Tetrominoes, the 'Tetris' class manages all other pre-requirements and interactions possible. 'Main' contains the actual game loop which is accessing the functions from the other classes. The game can be started by running the 'main' file. 


# Checkpoints 

*Requirements* 
- familiarize with Pygame library             # done 
- use keys to move and turn obstacles around  # done 
- display current score                       # done 
- increase pace and level over time           # done     
- function to hold obstacle for later         # done 
- function to pause game                      # done 

*Additional implementations* 
- shadow of obstacles 
- next function 
- hard & soft drop 
- music 

*Optional add-ons to include* 
- instructions to pause 
- user name 
- start from a higher level 
- high score 
- control music volume independently from general volume 
- extra sound for landing, when hold was used 


# Usage of the Program 

*How the game works*   
After starting the game Tetrominoes - 7 differently shaped (and colored) obstacles - will "fall from the sky". Your goal is to place them on top of each other in such a way that they fit together ideally perfectly, which means that there are no spaces left between them which are covered by lines further up. Whenever the current Tetromino touches the groundline (bottom of screen or another Tetromino) the next Tetromino is released from the top of the screen. You get points for making lines be fully filled up with Tetrominoes without spaces in between which makes them disappear. When more lines were removed the game's speed aka. The speed of the Tetrominoes falling down increases and the player receives more points for filling rows. The game ends as soon as the Tetrominoes build up such a high tower that they reach the top of the game’s interface.  

*Control of the game*   
With the usage of the left and right arrow the Tetrominoes can be moved left or right. Pressing the arrow up rotates the Tetrominoes clockwise. Pressing 'P' pauses the game, afterwards 'C' can be pressed to continue and 'Q' to quit the game. Pressing the arrow down lets the Tetrominoes speed up as they fall down, the so-called soft drop, while pressing the space key lets them drop immediately (hard drop). There is the option to hold a Tetromino for later by pressing 'shift', pressing the same key again will release the Tetromino from the hold position while entering the current one.  