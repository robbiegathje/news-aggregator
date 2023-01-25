// Two variables are passed through to top-stories.js from inline HTML scripts.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user-selected
// language and country. See /news/top-stories.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

STORIES_CONTAINER = document.getElementById('stories');

document.addEventListener('DOMContentLoaded', async function() {
	response = await getTopStories(
		userLanguageCodes.join(','), userCountryCodes.join(',')
	);
	articleCardCollection = [];
	for (let articleData of response.data.data) {
		articleCard = generateNewsArticleHTML(articleData);
		articleCardCollection.push(articleCard);
	};
	appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);
});
