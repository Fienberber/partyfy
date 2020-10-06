# partyfy
The UBER of collaborative party game

# Features

## Name

### Technical solution





# Web pages 

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
  * mqtt_topic

### Input creation
This page allow the player to create inputs for the party. 

The UI will allow the user to see the full input list (his input). 

On the creation side, you can select n random people OR just write whatever you want. A button will be added to read the input as it will during the game. 

### Game page


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
| type  | type_id  |   |
| repeat  | number [-1 infinity, n for n repetitions]  |   |
| random_target  | number | (number of people targeted by the random selector)  |
| input_content | string |   |


## InputType 
| Name  |  Type | Ex  |
|---|---|---|
| type_id  | number [unique]  |   |
| input_id  | number  |   |
| type_name  | string  |   |
| mqtt_topic  | string [optional] |   |


