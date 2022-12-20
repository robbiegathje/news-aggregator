# News Aggregator

## Capstone One Proposal version 1.1

### James "Robbie" Gathje

What goal is this website designed to achieve?<br>
This website is intended to provide daily news & top stories from a variety of sources across the globe.

Who are its intended users (i.e. their demographics)?<br>
Anyone looking for various sources on the same news story or those curious about news all over the world.

What data does it use?<br>
Utilizing [TheNewsAPI](https://www.thenewsapi.com/), the website collects stories from various news outlets including details concerning their language, locality, source, categories, and publish date.

What does its database schema look like?<br>
The database, in the most basic version of the app, contains a users table, a countries table, and a languages table. The users table contains information regarding authentication as well as foreign keys linking to the other two tables used to identify the user's language & locality. (Database Model Diagram is to be created soon.)

What kinds of issues might its API cause?<br>
The API has a daily limit of 150 requests per API Token when in the free tier. This leaves no room for accidentally creating infinite loops. As such, this requires extra caution when writing loops and conditionals that involve the API.

What sensitive information does it secure?<br>
Passwords are secured and must be properly encrypted. Further, a user's preferred language is required. A user can also choose a country to receive news for.

What functionality does it include?<br>
The website has basic log-in/log-out functionality. Its main feature is displaying today's top stories in the user's language and their locality (or globally, by default) with headline links to each source article. Further, it allows the user to search news by keyword.

What does its user flow look like?<br>
The main page displays current top stories for the logged-in-user's locality in the user's preferred language. There is also a search page to query TheNewsAPI by keyword. Lastly, a user can edit their preferred language and locality on their respective user page. (User Flow Diagram is to be created soon.)

What features does it have beyond basic CRUD (Create, Read, Update, Delete)?<br>
The base version of the app is built on search. Both the top stories page for every user and the search by keyword page rely on searching the API's database, not the local one.

What stretch goals / extra features could be achieved / implemented?<br>
There are three primary stretch goals with one bonus.

1. Allowing users to select preferred sources for their top stories page. This is done with relative ease considering we are already searching by language and locale.
2. Enabling users to save articles to read later. This allows for database expansion, i.e. an articles table, and it's another feature beyond basic CRUD.
3. Expanded search including search by category, news source, publish date, or locality.
4. Lastly, as a bonus stretch goal, a page to display top headlines in screenshot format, yet this would require the addition of [ApiFlash](https://apiflash.com/).