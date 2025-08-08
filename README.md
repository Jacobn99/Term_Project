Civilization was designed in three weeks as a class project for the Principles of Programming and Computer Science class at Carnegie Mellon University. The game, 
which is inspired the 'Sid Meries Civilization' series, is a top-down turn-based strategy experience that tasks two players to build empires
and conquer each other's civilizations. Players construct settlements to harvest resources, build combat units, and attack other units/settlements.
Programmed in Python, the game combines the CMU-Graphics framework with Numpy and Pillow to efficiency store and modify frame data.

The game map is rendered in an isometric grid pattern with pixeled graphics to achieve a semi-3D feel. The game map is viewed in a top-down perspective, 
with 9x9 grid of tiles being shown on screen. Map elements are spread across a 30x30 grid, so the player must use the arrow keys to move their 
perspective to other parts of the map. 

The game is populated with three tile types--forest, grass, and rock--which have their respective resources choosen from a pool of probabilities based on tile type. 
Food and production are the two resources that can be harvested in the game and they are visually respresented by apple and gear icons respectively. 
These icons are overlayed over the tiles the are present in. For example a rock, which is a production heavy and food scarce tile, may have two gear 
icons displayed over its sprite but only 1 apple, thus implying a harvest would yield two production and one food.

Players begin the game with a settler unit, which can be moved by clicking the tile of the settler followed by the desired grid position to settle. 
After positioning the settler, players can hover over it's location and press 'S' to create a settlement. 

In order to harvest resources, player must place a settlement and select tiles to harvest using their "population". A settlement's population
starts at two, thus limiting the player to two tiles to harvest. Tiles selected for harvest yield the resources shown over their sprite
every turn. Food contributes to increasing population, while production can be used to build more settlements and combat units to hinder
their opponents progress.

The game has three units: settlers, warriors, and spearmen. Settlers build settlements; warriors can plunder settlements and kill enemy units;
and spearmen are stronger, yet more costly versions of warriors. Units can be built by left-clicking a settlement to open the settlement UI 
and navigating to the production menu. Then the desired unit can then be selected. A constucted unit can then be moved once per-turn
around the map by selected a desired tile with the mouse.

When attacking with combat units, the player must click the unit they want to attack followed by the unit/settlement they want to inflict
damage upon. Hovering over a unit will show its remaining health points (HP). After a unit/settlement's health bar reach 0 HP, they will be
deleted from the game. The game is won when a player conquers all of their opponents settlements.
