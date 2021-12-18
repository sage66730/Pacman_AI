Kai Chieh Lo 922245100

Q1:
Question 1 is just a code implementation of the given formulas.
I use another dictionary to store new values then assign to self.values after every iteration.

Q2:
The main problem of this bridge is the agent has to walk east five time consecutively without misbehavior.
Therefore, we should lower the nosie a quite lot since it is affecting the agent exponentially.

Q3:
To encourage risking the cliff, we have to lower the noise.
To encourage going to distant exit, we have to lower the penalty of living.
To encourage agent stay as long as possible, we have to raise living reward like crazy (even over exiting reward)

Q6:
Like question 1, the problem is not about design but implementation.
I did not use the provided counter class so I have to check if we are getting the value for the first time in getQvalue().

Q7:
This epsilon IF statement can be implemented easily with util.flipCoin(), random.choice() and self.computeActionFromQValues().

Q8:
Since we are not controlling noise, the agent can never (at least not highky likely) reach distant exit even the epsilon is 1.

Q9:
I only fix some bugs of my implementation in the computeActionFromQValues() since it is not recognizing terminal states correctly.

Q10:
Like question 1, the problem is not about design but implementation.
The overall structures look alike but the formulas (calculating Q and how to update) are differnt. 