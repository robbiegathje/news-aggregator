// Two variables are passed through to search.js from inline HTML scripts.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user-selected
// language and country. See /news/search.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

document.addEventListener('DOMContentLoaded', async function() {
	const LOADING_CONTAINER = document.getElementById('loading');
	const SEARCH_FORM = document.getElementById('search-form');
	const SEARCH_TERM_INPUT = document.getElementById('search-term');
	const STORIES_CONTAINER = document.getElementById('stories');
	const USER_SEARCH_SETTINGS = document.getElementById(
		'user-search-settings'
	);

	SEARCH_FORM.addEventListener('submit', async function(event) {
		event.preventDefault();
		USER_SEARCH_SETTINGS.style.display = 'None';
		LOADING_CONTAINER.style.display = '';
		STORIES_CONTAINER.innerText = '';
		let searchTerm = SEARCH_TERM_INPUT.value;
		let response = await getTopStoriesBySearchTerm(
			searchTerm,
			7,
			userLanguageCodes.join(','),
			userCountryCodes.join(',')
		);
		let articleCardCollection = [];
		for (let articleData of response.data.data) {
			let articleCard = generateNewsArticleHTML(articleData);
			articleCardCollection.push(articleCard);
		};
		LOADING_CONTAINER.style.display = 'None';
		USER_SEARCH_SETTINGS.style.display = '';
		appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);
	});
});
