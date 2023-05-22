Markdown is a special plain text formatting language that is extremely popular among developers. It is used in documents, research articles, Github README files, and other things. In this project, you will write an editor that will be able to recognize several tags, structures, and save your results to a file.

Example:

```
Choose a formatter: > header
Level: > 1
Text: > Hello World!
# Hello World!

Choose a formatter: > plain
Text: > Lorem ipsum dolor sit amet, consectetur adipiscing elit
# Hello World!
Lorem ipsum dolor sit amet, consectetur adipiscing elit
Choose a formatter: > new-line
# Hello World!
Lorem ipsum dolor sit amet, consectetur adipiscing elit

Choose a formatter: > ordered-list
Number of rows: > 3
Row #1: > dolor
Row #2: > sit
Row #3: > amet
# Hello World!
Lorem ipsum dolor sit amet, consectetur adipiscing elit
1. dolor
2. sit
3. amet

Choose a formatter: > !done
```