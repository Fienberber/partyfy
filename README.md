# partyfy
The UBER of collaborative party game

# To do
- Test the game engine
- The Smart lighting feature

# Usage
```
git clone https://github.com/Fienberber/partyfy
cd partyfy
```
Optional: Create a venv
```
python3 -m venv venv
source venv/bin/activate
```
Install requirements and start the server
```
pip install -r requirements.txt
python3 main.py
```
Now access http://127.0.0.1:8000


You have to create a `smtp_setup.py` file to enable the "change password" feature.

This is the content required:
``` python
smtp_server = "mail.domain.net"
port = 465 
sender_email = "sender_email@domain"
password = "*********"

```

For the secret part, you will need a `secret.py` file:
```python
SECRET_KEY = b'*******************'
```

# Features
This project is a collaborative game. 

The goal of this game is to make evenings with friends more fun.

Invite your friends and let them create there own inputs (private jokes alowed). 

When you have enough inputs (you can create them before the real party) you can PLAY.
Select you party, your players and start. 

It will play by itself (no game master needed). Your browser can read the inputs (if supported). And the participants will be automatically generated. 

You can optionnaly add smart lighting to the game. The lightings are synced to the input types. The types represent what ever you want.
For example a type could be "Quizz" the light would alert everyone that a quizz is comming and then the voice will read the input. 

The possiblilities are quite wide so explore them and have fun. 


Sorry for the french content. We play with french people so it's easier.


