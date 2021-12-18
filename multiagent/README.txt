Kai Chieh Lo 922245100
(no team-up)

Q1:
My evalution compose 3 weighted score:
    1. Distance to ghost: It is a safe strategy to not get near to ghost (near is defined as distance of  1)
    2. If the action eats a food 
    3. Distance to the closest food
These 3 scores are weighted to ensure priority. For example the -10000 ensures pacman to always avoid ghost first.
So the logic of the pacman can be described as: avoid ghost > eat food > look for nearest food

Q2:
I implement 2 sub-routines for maximizer and minimizer.
If next agent is pacman call maximaizer. Otherwise, minimizer.
If it is a leaf node or it reaches the depth, evaluate state.

Q4:
Similar to Q2 but I change the min function in minimizer to maen function (since probabilities are universal) and call it expactimax.

Q5:
This evalution is improve from Q1, composing 5 weighted score:
    conditional score:
        1. (scare time only) Eat ghost: It is an agressive stratrgy to prioritize killing ghosts for score
        2. (none scare time only) Distance to ghost: It is a safe strategy to not get near to ghost (near is defined as distance of  1)
    usual score:    
        1. Amount of capsules remaining
        2. Amount of food remaining
        3. Distance (maze distance) to the closest food (if there is no any food remaining, give 10000 as prize for winning)
These 5 scores are weighted to ensure priority. For example the -10000 ensures pacman to always avoid ghost first.
So the logic of the pacman can be described as: avoid/kill ghost > eat capsule > eat food > look for nearest food

Time consumption:
I spent aroun 10-12 hours for this homework, most of them were spend on optimizing Q5.
