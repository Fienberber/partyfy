# partyfy
The UBER of collaborative party game

# To do
- Add the change password page
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


# Features

## Light animation
When a new input is displayed it can change the light color. 

### Technical solution
The web client is going to make a request (undefined right now) for each input type. 

## Database technical solution 
¯\\(◉‿◉)/¯

## Web server
Flask because python is easy. 

## Process 
The web server is just going to send the data from the database to the client. The rest (text to speech, lighting, ...) will be handled by the client (js). 



# Web pages 

### Login
Login page. 

### Party selection 
Page accessed by a player. It list the parties your in and the people invited to this party.

If your are the creator you can access extra setting 

If you are just invited, you can select a party to add inputs

You can create a party.


### Party creation/edit
Page accessed by a player to create or modify party settings. 
Like : 
- name
- invited players
- input types
  * name 
  * post request (light)

### Input creation
This page allow the player to create inputs for the party. 

The UI will allow the user to see the full input list (his input). 

On the creation side, you can select n random people OR just write whatever you want. A button will be added to read the input as it will during the game. 

### Game page

Just display the input content (can add the random players list). 

The player can go to the next one and the previous one. 

The inputs will change automatically depending on the number of inputs.


# Database

## Party 
| Name  |  Type | Ex  |
|---|---|---|
| party_id  | number [unique] |   |
| title  | string  |   |
| creator_id  | number  |   |


## PartyPlayer
| Name  |  Type | Ex  |
|---|---|---|
| party_id  | number |   |
| player_id  | number  |   |


## Player
| Name  |  Type | Ex  |
|---|---|---|
| player_id  | number [unique] |   |
| first_name  | string  |   |
| last_name  | string  |   |
| can_create_party  | bool | for beta stage  |



## Input
| Name  |  Type | Ex  |
|---|---|---|
| input_id  | number [unique] |   |
| title  | string  |   |
| type_id  | type_id  |   |
| party_id  | party_id  |   |
| repeat  | number [-1 infinity, n for n repetitions]  |   |
| random_target  | number | (number of people targeted by the random selector)  |
| input_content | string |   |


## InputType 
| Name  |  Type | Ex  |
|---|---|---|
| id  | number [unique]  |   |
| type_name  | string  |   |
| party_id  | number |   |
| url  | string [optional] |   |


