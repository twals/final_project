# Games Shelf

### Video demo: https://youtu.be/Sg-ATyfWmMY

### Description:

The purpose of the Games Shelf is to act as a record of the games you have played. It allows you to jot down thoughts about a game and give a rating out of 10. You can also create a Wishlist to make note of any games you want to play in the future and which platform you might wish to play it on. There are some additional features I wish to add in the future and will outline below. 

Games Shelf was created using Python, Flask, HTML, CSS and Bootstrap. 

### Files

#### app.py

This file imports and configures Flask for use with the website, as well as the CS50 library for SQLite. Other libraries are imported to support in the use of hashes and wrappers. The functions throughout the file allow the following features to be incorporated in the project: 

- User accounts (register, log in and change passwords. Require an account to view content and ensure that the user only sees content relevent to their account)
- Error handling (e.g, user does not select an option when required)
- Displaying and interacting with the content of the site
- Redirecting the user as needed (e.g, to the home page after logging in)

#### final.db

The database for the final project is made up of four tables - users, shelves, games and wishlist. I tried to design these so as to keep any repeated information to a minimum. 

- The users table stores an id, username and hash for the users password. 
- The shelves table stores an id for each entry, user_id (to ensure the user only sees _their_ shelf), game name, user notes and user rating. 
- The games table stores an id for each game, the games name and genre. 
- The wishlist table stores an id for each entry, the name of the game and the platform. 

Despite the decision to reduce repeated information, the name of each game is stored a number of times across the different tables. I will look to recitfy this in the future.

#### static - styles.css

The CSS included for the site is still very basic. I have opted for simple colours and to make the tables readable. I have however included a responsive navbar. I wanted to clean the navbar up a little by utilising some drop bars to group some of the options together. I was unable to get this to work in the timeframe I gave myself and so will look to revisit in the future. 

#### templates

The templates folder holds html files for each of the pages. These all extend the file 'layout.html' to keep them uniform and reduce repetition. The navbar is included on layout.html to ensure it is present everywhere. 

### Next steps

There are some features and adjustments that I was unable to implement on my self-imposed time frame which I hope to come back to. I have alluded to these previously and they are outlined below. 

#### Features

- Ability to view another users shelf (without making changes) if that user has made it available to view.
- Abiltiy to view a single game with an average rating from the sites users and comments that have been made.

#### Adjustments

- The overall aesthetic of the site is basic and I would like to improve this when I am more proficient with CSS / Bootstrap.
- Some aspects could be tidied up, e.g use of drop down menus on the navbar. 






