# Golf Scoreboard

### Rudy's Cup


#### To update requirements use (for proper eb formatting)
```
pip list --format=freeze > requirements.txt
```


#### EB Notes
```
eb init -p python-3.8 golfscoreboard --region us-east-2
eb init
eb create flask-env
eb open
eb ssh
```
```
scp -i /home/bwood/.ssh/laxbets-keypair /home/bwood/Desktop/Fun/RudysCup/data/playerScores.csv ec2-user@18.189.11.176:/tmp/
ssh -i /home/bwood/.ssh/laxbets-keypair ec2-user@18.189.11.176
sudo mv playerScores.csv /var/app/current/data/
```
?
sudo chmod ugo+rwx <dir or file>
