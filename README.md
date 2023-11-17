# Mechanical-Turk

Source data used for this article: [https://www.mdpi.com/1099-4300/21/12/1201](https://www.mdpi.com/1099-4300/21/12/1201)

**1989** folder contains the original corpus used for the experiment

**MT** folder contains all the results and codes used to generate figures in the article

In the **MT** folder, you will have multiple subfolders:
- **simple_test**: which corresponds to Shannon's experiment, every line is a result of a worker, the worker only guesses once for each letter, the delimiter is **&** and you'll find those columns:
    - AssignmentId: id of the work in mechanical turk
    - WorkerId: worker's id
    - Answer: the sentence that the worker worked on
    - correct/wrong answer: 0 for a wrong answer and 1 for the correct answer, separated by comma
    - guessed letter: the letter that the worker guessed, separated by comma
    - worker comment: comment left by worker
- **hard_test**: same as simple_test but the worker has to guess the correct letter in order to go to the next letter, the delimiter is **&** and you'll find those columns:
    - AssignmentId: id of the work in mechanical turk
    - WorkerId: worker's id
    - Answer: the sentence that the worker worked on
    - number of guesses: how many times the worker tried before the answer, separated by comma
    - guessed letter: the letter that the worker guessed, separated by comma
    - worker comment: comment left by worker
- **gambling_test**: which corresponds to Cover & King's experiment, every worker has to guess 15 letters, the delimiter is & and you'll find those columns:
    - AssignmentId: id of the work in mechanical turk
    - WorkerId: worker's id
    - Answer: the sentence that the worker worked on
    - Letter guessed: the number of letters the worker guessed
    - Last guessed letter index: position of the last guessed letter, for example, 15 means the worker guessed from index 0 to index 14 (in python terms), 30 means the worker guessed from index 15 to index 29, 45 means the worker guessed from index 30 to index 44, and so on
    - Answer and weights: the correct answer in the first position then the weights that the worker gave for the guessed letter, the sum must be 100. For example, if we have "I,A20,H20,M20,S20,T20", it means that the correct letter is I and the worker gave a weight of 20 to A,H,M,S,T
    - worker comment: comment left by worker

The `analyse_resultV2` function in the `analyseV2.py` may be useful to analyse the results.
