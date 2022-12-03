The directory of files: 

api.py is the actual API behind the monopoly. It contains and reads hard coded monopoly rules such as the default board, prices and initializations of dictionary objects reflecting details of a game and respectively modifies game dictionaries.

properties.csv is a file of convenience that stores the hard-coded property details in a convenient location for editing. If we get the time we can be creative and move past monopoly. It serves as a placeholder for now.

board.jpg is simply an image reference of the monopoly board. I can be if someone wants to spend a second editing and if we are REALLY FUCKING LOW ON TIME!!! WE DONT WANT TO GO DOWN THAT SHITTY ROUTE!!! Let's try a graph rendering thing or something! Just there.

database.py is a far-reaching file that manages our MongoDB pymongo collections that hold every single thing, from accounts to current game boards, in the server. This will be the last thign called by any and all service. Should be our most closely guarded area by security. Don't let anything down here that we don't want want in there.
Don't EVER trust our users. Especially Jesse, that sly dog.

docker-compose.yml manages our Docker Desktop implementation. It's a big deal, generally don't touch it unless not only we need Websockets but something needs to be modified in here to accept Websockets. Only a trained eye should touch this. Obviously users have nothing here to touch, so don't let them near it. lol.

Dockerfile is the 'make' file which manages the services that not only our container offers but is the main connector for our network. Keep it safe.

templator.py generates the python string HTML files to be served to the client by our server. They should have everything including image links. The images requests are fine being presented by the server; that's totally cool. We could also host commands here but that can be done in future. Hopefully by Cole cuts.

README.md is a helpful index for each unit in this project. Should be periodically updated to record progress. Comment collection.

requirements.txt is a text file for our Docker Desktop to use when booting the server. It simply enumerates the required libraries that need to be downloaded for the server to be ran. This is to be tested extensively and rarely touched. If it works, never touch this file under any circumstances. Not to move it, not to rename it, not to edit whatsoever.

server.py is the file using Flask web framework to interpret request and remove the important information, call relevant functions and other services for use as a free application.

test.py is just a testing workbench and a small archive of old code.

jack.py is a multi-tool that takes commands from server.py, modifies the database's game objects based on what api.py recommends.

functions.js controls websocket structures