Kai Chieh Lo
922245100
not teamed up
(It is good to know how limited one person can do. I would try to team up next time)

#position search problems: ################################################################################################################################################
Since I was focusing on the commands provided on website, I realized some codes have to be edited to fit the autograder after I tried to grade them.
The implementation of searches may be a little different, but still with the same generic idea except for corner problems.

#corner problems: #########################################################################################################################################################
I think there is a huge difference between position search problems and corner search problems so I use IF statement to seperate them.
The difference is corner problems may go back to visited points if needed like:

****************************
*f           p            f*
*f************************f* 
****************************

h= min( [d(f1,p), d(f2,p)], d(f3,p), d(f4,p)] )

My general algorithm is:
1. use any search to reach one of the goals
2. clear the visited nodes (pacman may want to go back) so the state is like a new search problem with one less goal. The actions are still kept.
3. do 1. and 2. for n times, n = number of checkpoints (in this case: 4) 

My algorithm takes a lot of tome as the steps gorws so Q6 will take forever, especiall after step 42 (visiting second corner).
The minimum heuristic I implemented gorws dramaticly after visiting a corner, so there would be many nodes with lower priority to be popped first.

#food search problems: ####################################################################################################################################################
I cannot really tell the difference between corner problems and food search problems since what they do is trying to pass every checkpoint (food or corner)
Therefore I plemented the heuristic with similar idea as corner problems 

#hours: ###################################################################################################################################################################
More than 24 hours, since I tried to cheese a little bit by implementing corner/food problems using shorest Hamiltonian path. 
The result in pacman commands were great but did not pass autograder so I come back to normal solution. 