# News Over Coffee

## Springboard Capstone One

### James "Robbie" Gathje

Check out the site! [News Over Coffee](https://news-over-coffee.herokuapp.com/)

## Overview

![Site Welcome](docs/site_welcome.png)

News Over Coffee seeks to present up-to-the-minute news for every user in their chosen countries & languages. In order to do that, we collect top stories by those user preferences from [The News API](https://www.thenewsapi.com/). Collecting top stories from varied sources empowers users to look past the headlines and understand the stories themselves. And collecting in many languages from many countries allows users to step out of their more localized news cycle.

![Top Stories Page](docs/top_stories.png)

Further, News Over Coffee allows users to search for news by keyword or phrase in order to truly dig into a particular story or topic.

![Search Page](docs/search.png)

Lastly, users are able to edit their preferences at any time through the User Preferences link in the dropdown box behind their username in the navbar.

![Edit User Preferences Page](docs/edit.png)

User Flow:

![User Flow Diagram](docs/user_flow_diagram.png)

## A Couple Thank Yous

API: [The News API](https://www.thenewsapi.com/)

I want to give a huge thank you to The News API for maintaining such a massive database of international, multilingual, up-to-the-minute news!

Additionally, a massive thank you goes out to my wife, Carly Gathje, who helped me with design choices every step of the way!

## Technologies Used

News Over Coffee is written in both **Python** (for the back-end) and **JavaScript** (for the front-end). It utilizes the **Flask** web framework to build out the site's routes, **SQLAlchemy with PostgreSQL** for the database, and **bcrypt** for password encryption. Lastly, it uses **Bootstrap** for css styles.

Database Schema:

![Database Schema Diagram](docs/database_schema.png)