## Tetris Game 


*Possible improvements* 
- improve the level system 
- hold function (sometimes c, other times space key removes them from hold position) 
- !! docstrings 
- add game state winning  
- control PEP style 
 

# Project description 

This program allows you to play Tetris, a single player game probably everyone has some memories from. This is why we chose to implement it as our Project. To do so we thought of essential features for a game to count as a real Tetris game and ranked them into the categories 'necessary' and 'nice-to-have'. Our research has shown us that pygame is a useful library which comes with many features that allow for easier implementation of the game´s components. 
 

# Table of Components 

1. Installation & Running 
2. Checkpoints 
3. Usage of the Program 
3. Code Tests 
5. Learning Achievements 
6. Challenges 


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
With the usage of the left and right arrow the Tetrominoes can be moved left or right. Pressing the arrow up rotates the Tetrominoes clockwise. Pressing 'P' pauses the game, afterwards 'C' can be pressed to continue and 'Q' to quit the game. Pressing the arrow down lets the Tetrominoes speed up as they fall down, the so-called soft drop, while pressing the space key lets them drop immediately (hard drop). There is the option to hold a Tetromino for later by pressing 'C', pressing the same key again will release the Tetromino from the hold position while entering the current one.  


# Learning achievements 

We first needed to get familiar with the pygame library since we didn't come in contact with it before. After watching a couple of youtube tutorials we got a glance of the functions provided and the rest was figured out by googling as we went. As a first draft we programmed a game with just the typical Tetrominoes falling down and then added the other features one by one. While doing so we improved our knowledge about classes in python and how to program the most conveniently.  

 
# Challenges 

We were surprised by how much one could get stuck in a little thing and just not being able to get it solved for way too long. For us this was the case with the bag system of choosing a new Tetromino, to understand you can imagine a bag which has each of the 7 Tetrominoes in it once. When a new Tetronino is needed it is picked out of this bag, once chosen it is removed. This process is repeated until no more Tetrominoes are in the bag (or it is game over), then the bag is newly filled with the seven Tetrominoes. By proceeding this way, it is made sure that each of the Tetrominoes appears at least every 13 occurrences.  

Now to what caused us a headache: first of all, it took us quite some time to find a practical way to implement random choosing from the bag. We started by creating a copy of the list containing the different Tetromino objects, picking one of those randomly and popping it afterwards. The problem with this was that the indices were not consistent anymore. Hence, we looked for another way and came up with the idea to create a list just containing the indices, shuffle it, pick the first element of this list as an index for the list containing the Tetrominoes and pop the element from the index-list afterwards. Once the index-list was empty it should be newly filled with numbers from 0 to 6 and the process should be repeated. The problem was that within the function the if condition checking for whether the list was not empty was never true, which caused the program to always go in the else part, where the bag was newly filled, which was simply like there existed to bag. Until we figured out that .... was the reason for the program to not perform in the way we intended it to do, it took way too long. Once it did, the next and hold function were not working properly anymore. So, solving one problem caused two new ones. 