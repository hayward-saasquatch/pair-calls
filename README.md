# pair-calls
Scripts for scheduling team pair calls. Can generate a file locally and optionally post on Slack

## Basic Functionality
In it's most basic form this code can be used to generate pair calls reading in historical pairings and a list of users to be paired.
### Setup 
1.  Download/Clone the Repository
2.  Create a directory in the folder called `weeks`
3.  Include any backdated pairings in CSV format using the `yyyy-mm-dd.csv` naming convention for the first day of the week they are in effect. The format of each document should be two columns of names indicating who is paired. 
4.  Create a text file called `names.txt`. Include the names of each team member that you ant included in the pairing. Each person's name should be on a seperate line.

### Usage
Run the script `assign-pairs.py`:
    On Windows: 
    On Linux: (from the directory containing the assign-pairs script) `./assign-pairs.py`

## Advanced Functionality
In addition to being able to simply generate pairings, this code is able to send these pairings to Slack.

### Setup
1. Follow the setup steps from the "Basic Functionality" section.
2. Create a text file in the working directory called `slack-endpoint.txt`
3. (Optional Step) If you plan on posting these paired calls as you or another existing user, skip this step. Otherwise, head over the [Slack Custom Integrations](https://api.slack.com/custom-integrations) page and create a new bot user. Choose your desired username. The username and Token for this bot will be used as part of the endpoint URL in the `slackendpoint.txt` file in the next step.
4. Include the Slack API endpoint you want to use for submitting the data to slack. These typically come in the form `https://slack.com/api/chat.postMessage?token=YOUR-SLACK-TOKEN-HERE&channel=CHANNEL-NAME-OR-ID&as_user=true&username=USERNAME`

    Consult the [Slack API methods docs](https://api.slack.com/methods) for additional details on other methods that are available if you do not plan to simply post the paired calls as a message in a channel.
    
6. (Optional Step) Change the wording of the text submitted
7. Make sure that the directory that contains your scripts, files, and folders related to this project has been set in the `do-pair-calls` script file. 

    e.g. Change the `cd /opt/pair-calls` line to something like `cd ~/pair-calls` which reflects the location of this project's files

### Usage
- To submit previously generated pairings simply run the send-pairs.py file and include the name of the file that includes the existing pairings you would like to sent.
    
    e.g. on linux: `./send-pairs.py 2016-10-10`
- To generate a new pairing and send those to Slack at the same time run the `do-pair-calls` script.
    
    e.g. on linux `./do-pair-calls`



