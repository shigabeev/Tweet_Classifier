# Tweet Classifier
<p>Qualitative analysis software that will make assumptions on topics that twitter user is often talking about.</p>

## Usage:
<p>Right now, scripts are in raw format and designed to do only limited amount of tasks.
 To change income parameters you'll have to change the code, probably.</p>
<ol>
    <li>To parse data from twitter use get_tweets.py from console.
        <br>It takes username as a command line argument and saves .csv file to /raw_data</li>
    <li>Script for learning process is learn.py. It grabs all the content from /train_data and convert it to DB.json</li>
</ol>