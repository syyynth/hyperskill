This is the *Algorithms with IMDB* project I made myself.


<p>We all know how hard it is to choose a movie for a party with friends! Why not invent an algorithm that will help you with the task? Create a small program that sorts movies according to the rating of your choice and learn the basics of time complexity analysis and various searching and sorting algorithms.</p><br/><br/>Learn more at <a href="https://hyperskill.org/projects/213?utm_source=ide&utm_medium=ide&utm_campaign=ide&utm_content=project-card">https://hyperskill.org/projects/213</a>

Here's the link to the project: https://hyperskill.org/projects/213

Check out my profile: https://hyperskill.org/profile/1254124

---
It's a static program, that just prints titles (movies.txt) with a rating 6. To change the rating/algorithm, you can do it manually in the code.
Currently: merge sort + binary search, rating = 6<br>
`binary_search(merge_sort(data), 6)`

Or, you can run `python.exe algorithms.py PATH SORT SEARCH RATING`<br>
PATH: path to the file<br>
SORT: bubble, merge<br>
SEARCH: binary, linear<br>
RATING: any number<br>

Example:
```python
python.exe .\algorithms.py movies.csv bubble binary 6.6
```

```text
Aladdin and the Wonderful Lamp - 6.6
Rescued by Rover - 6.6
The '?' Motorist - 6.6
For Love of Gold - 6.6
The Man and the Woman - 6.6
A Corner in Wheat - 6.6
Døden - 6.6
Her Awakening - 6.6
The Musketeers of Pig Alley - 6.6
Atlantis - 6.6
The Battle of Gettysburg - 6.6
Brewster's Millions - 6.6
Ditya bolshogo goroda - 6.6
The Life of General Villa - 6.6
Little Lord Fauntleroy - 6.6
Men and Women - 6.6
Alias Jimmy Valentine - 6.6
The Cheat - 6.6
The Cub - 6.6
The Gentleman from Indiana - 6.6
The Golden Chance - 6.6
The Italian - 6.6
Jeanne Doré - 6.6
Kindling - 6.6
Liliya Belgii - 6.6
On the Firing Line with the Germans - 6.6
Zucker und Zimt - 6.6
Bobby Bumps and His Goatmobile - 6.6
The Count - 6.6
The Fireman - 6.6
The Floorwalker - 6.6
Gloria's Romance - 6.6
The Good Bad-Man - 6.6
The Intrigue - 6.6
Little Mary Sunshine - 6.6
```
