# PROJECT: VIOLET UNICORN (aka Delphi)

Duck and Windmill's HackRU Fall 2017 submission.

## Inspiration

We saw the Vitech dataset and thought it would be great opportunity to apply the skills we have been learning in classes and student groups. Between us three we have basic experience in machine learning, data science, and data visualization, and figured that working with a huge dataset would be the best way to hone those skills.

## What it does

Our project does a couple things. The first step is the data retrieval and manipulation. Data on participants, policies, and activities from Vitech's API is pulled down. To minimize the dataset, the initial retrieval from Vitech's Solr instance is filtered with queries to ensure that only participants with a policy that was connected to an activity are downloaded (This cut down the size of participants and policies from 1.4 million and 1.5 million to around 40,000 each). When the data is downloaded, it's saved into a MongoDB instance to prevent downloading the data on every run. Then we run a few transformations on the datasets to create a final dataset which contains participant info combined with the the type of activity that got them to sign a policy. Each of the transformations are saved in MongoDB as well, to both keep a history of transformations and to prevent running the transformations redundantly.

Once the data is ready, Deplhi does two things. One, we provide a Jupyter Notebook that provides visualizations of the Vitech data. The visualizations help provide insights on how differences in participant demographics affect what campaign activity was most effective. Second, Delphi has a predictor that takes in arbitrary demographics on a test participant and returns what campaign activity would be most likely to result in a new policy.

## How We built it

The entire codebase was written in Python. The data retrieval makes use of the MapReduce paradigm and MongoDB to store everything. The data visualizations are made using Plotly inside a Jupyter Notebook. For the predictor tool we used the Python SK Learn library.

## Challenges We ran into

At first, the huge size of the Vitech data was an issue as estimated run times was around 400 hours. After filtering the policies to only the ones that were connected to a campaign activity, we shrank run time to 8 hours, but that was still too long to be viable. Finally, we realized that Solr allowed join queries and we shrank our participants dataset to be the same size as our policies. This gave us a runtime of <15 minutes, which was workable (We realized too late we could have been running the code on our school server's, which completed the transformations in <5 minutes). We also ran into a lot of bugs in the predictor, as this was the first time we were applying any machine learning techniques. 

## Accomplishments that We're proud of

Getting the transformation runtime into something manageable was a huge success for us, and so was being able to make use of the data in the end with the visualizations and predictor.

## What We learned

We learned that Solr is more powerful than we thought, and we shouldn't be doing big data science on laptops.

## What's next for Delphi

Improve the predictor and get a larger dataset, as well as better hardware so we can work with more data.
