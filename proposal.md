# News Aggregator

## Capstone One Initial Proposal

### James "Robbie" Gathje

What goal is this website designed to achieve?<br>
This website is intended to provide daily news & top stories from a variety of sources across the globe.

What are its intended users (i.e. their demographics)?<br>
Anyone looking for various sources on the same news story or those curious about news all over the world.

What data does it use?<br>
Utilizing [TheNewsAPI](https://www.thenewsapi.com/), the website collects stories from various news outlets including details concerning their language, locality, source, categories, and publish date.

What does its database schema look like?<br>
The database contains users, news sources, and saved articles tables. The users table contains information concerning user authentication, and it will be connected to each of the other two tables through their respective middle tables, allowing the user to save articles to read later and/or set preferred news sources to receive when populating their main page with top stories.

What kinds of issues might its API cause?<br>
The API has a daily limit of 150 requests per API Token when in the free tier.

What sensitive information does it secure?<br>
A user's preferred language is required. A user's location is an optionally provided piece of sensitive information, if the user wants to display local news on their main page by default.

What functionality does it include?<br>
The website displays today's top stories in the user's locality (or globally, by default) as headline links to their respective source articles. Further, it allows the user to search news by keyword.

What does its user flow look like?<br>
The main page displays current top stories for the logged-in-user's locality in the user's preferred language from the user's preferred news sources. There is also a search page to query TheNewsAPI by keyword.

What features does it have beyond basic CRUD (Create, Read, Update, Delete)?<br>
Each user is able to save articles to read later. Additionally, every user can set preferred news sources from which they will receive their main page's top stories.

What stretch goals / extra features could be achieved / implemented?<br>
Expanded search including search by category, news source, publish date, or locality would be immediately useful. News source pages displaying that source's top stories woudl be additionally beneficial. Lastly, a page to display top headlines in screenshot format is a further stretch goal, yet this would require the addition of [ApiFlash](https://apiflash.com/).