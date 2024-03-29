This is the *Simple Text Summarization* project I made myself.


<p>The modern world is rapid and dynamic, and every day people read a lot of news about politics, science, entertainment industry, programming, and so on. When there is so much information to digest, it gets really hard to deal with all of it! In this project, you will get familiar with something that might help: simple text summarization technique. This method extracts the most important sentences from the given text and is a great baseline for further experiments with other summarization approaches.</p><br/><br/>Learn more at <a href="https://hyperskill.org/projects/124?utm_source=ide&utm_medium=ide&utm_campaign=ide&utm_content=project-card">https://hyperskill.org/projects/124</a>

Here's the link to the project: https://hyperskill.org/projects/124

Check out my profile: https://hyperskill.org/profile/1254124
Example input:
```python
<?xml version='1.0' encoding='UTF8'?>
<data>
  <corpus>
    <news>
      <value name="head">New Portuguese skull may be an early relative of Neandertals</value>
      <value name="text">Half a million years ago, several different members of our genus, Homo, had spread throughout Europe and Asia, where some would eventually evolve into Neandertals. 
      But which ones has been the subject of intense debate. 
      A newly discovered partial skull is offering another clue to help solve the mystery of the ancestry of Neandertals. 
      Found in 2014 in the Gruta da Aroeira cave in central Portugal with ancient stone hand axes, the skull (3D reconstruction pictured) is firmly dated to 400,000 years old and an archaic member of our genus, according to a study published today in the Proceedings of the National Academy of Sciences. 
      The skull shows a new mix of features not seen before in fossil humans - it has traits that link it to Neandertals, such as a fused brow ridge, as well as some primitive traits that resemble other extinct fossils in Europe. 
      This new combination of features on a well-dated skull may help researchers sort out how different fossils in Europe are related to each other - and which ones eventually evolved into Neandertals.</value>
    </news>
    <news>
      <value name="head">Loneliness May Make Quitting Smoking Even Tougher</value>
      <value name="text">Being lonely may make it harder to quit smoking, a new British study suggests.
      Using genetic and survey data from hundreds of thousands of people, researchers found that loneliness makes it more likely that someone will smoke.
      This type of analysis is called Mendelian randomization.
      ' This method has never been applied to this question before and so the results are novel, but also tentative,'  said co-lead author Robyn Wootton, a senior research associate at the University of Bristol in the United Kingdom.
      ' We found evidence to suggest that loneliness leads to increased smoking, with people more likely to start smoking, to smoke more cigarettes and to be less likely to quit,'  Wootton said in a university news release.
      These data mesh with an observation that during the coronavirus pandemic, more British people are smoking.
      Senior study author Jorien Treur said, ' Our finding that smoking may also lead to more loneliness is tentative, but it is in line with other recent studies that identified smoking as a risk factor for poor mental health.
      A potential mechanism for this relationship is that nicotine from cigarette smoke interferes with neurotransmitters such as dopamine in the brain.' 
      Treur is a visiting research associate from Amsterdam UMC.
      The researchers also looked for a connection between loneliness and drinking but found none.
      Still, if loneliness causes people to smoke, it is important to alert smoking cessation services so they can add this factor as they help people to quit, the study authors said.
      The report was published June 16 in the journal Addiction.</value>
    </news>
  </corpus>
</data>
```

Example output:
```txt
HEADER: New Portuguese skull may be an early relative of Neandertals
TEXT: But which ones has been the subject of intense debate. 
A newly discovered partial skull is offering another clue to help solve the mystery of the ancestry of Neandertals.

HEADER: Loneliness May Make Quitting Smoking Even Tougher
TEXT: Being lonely may make it harder to quit smoking, a new British study suggests. 
This type of analysis is called Mendelian randomization. 
The researchers also looked for a connection between loneliness and drinking but found none.
```
