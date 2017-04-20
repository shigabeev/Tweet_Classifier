# Tweet Classifier
<p>Qualitative analysis software that will make assumptions on topics that twitter user is often talking about.
</p>

<h2>Usage:</h2>
<p>To try, open terminal and type:</p>
<pre>$ python3 classify.py twitter_account </pre>
<p>It will parse first 200 tweets from selected "twitter_account" and return number of tweets belonging to each category.</p>
<p>For classification you need just 3 files: DB.json, labels.txt and Classify.py</p>
<h2>Learning</h2>
<p>This script uses Naive bayes classification to determine category. You can manage input categories by changing
contents of "classes" folder.
<br>Use get_tweets.py to parse tweets from selected twitter accounts.
<pre>$ python3 get_tweets.py twitter_account </pre>
<br>Collected tweets will be saved to raw_data/twitter_account_tweets.csv.
</p>
<p>You can use this program to gender or any else classification. But keep in mind that it works with little amount of classes
and hardly rely on quality of input.
</p>
<p>After collecting the data, run
<pre>$ python3 learn.py</pre>
It will change the DB.json and labels.txt. Now classification will be performed on new data.
</p>
