// Two variables are passed through to search.js from inline HTML scripts.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user-selected
// language and country. See /news/search.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

let PAGE_NUMBER_OF_RESULTS = 1;

document.addEventListener('DOMContentLoaded', async function() {
	const FETCH_BUTTON = document.getElementById('fetch');
	const FETCH_CONTAINER = document.getElementById('fetch-container');
	const LOADING_CONTAINER = document.getElementById('loading');
	const SEARCH_FORM = document.getElementById('search-form');
	const SEARCH_TERM_INPUT = document.getElementById('search-term');
	const SEARCH_TIMEFRAME_INPUT = document.getElementById('search-days');
	const STORIES_CONTAINER = document.getElementById('stories');
	const USER_SEARCH_SETTINGS = document.getElementById(
		'user-search-settings'
	);

	SEARCH_FORM.addEventListener('submit', async function(event) {
		event.preventDefault();
		USER_SEARCH_SETTINGS.style.display = 'None';
		LOADING_CONTAINER.style.display = '';
		STORIES_CONTAINER.innerText = '';
		PAGE_NUMBER_OF_RESULTS = 1;
		let searchTerm = SEARCH_TERM_INPUT.value;
		let searchTimeframe = SEARCH_TIMEFRAME_INPUT.value;
		let response = await getTopStoriesBySearchTerm(
			searchTerm,
			searchTimeframe,
			userLanguageCodes.join(','),
			userCountryCodes.join(','),
			PAGE_NUMBER_OF_RESULTS
		);
		let articleCardCollection = [];
		for (let articleData of response.data.data) {
			let articleCard = generateNewsArticleHTML(articleData);
			articleCardCollection.push(articleCard);
		};
		LOADING_CONTAINER.style.display = 'None';
		USER_SEARCH_SETTINGS.style.display = '';
		FETCH_CONTAINER.style.display = '';
		appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);
	});

	FETCH_BUTTON.addEventListener('click', async function() {
		LOADING_CONTAINER.style.display = '';
		PAGE_NUMBER_OF_RESULTS ++;
		let searchTerm = SEARCH_TERM_INPUT.value;
		let searchTimeframe = SEARCH_TIMEFRAME_INPUT.value;
		let response = await getTopStoriesBySearchTerm(
			searchTerm,
			searchTimeframe,
			userLanguageCodes.join(','),
			userCountryCodes.join(','),
			PAGE_NUMBER_OF_RESULTS
		);
		let articleCardCollection = [];
		for (let articleData of response.data.data) {
			let articleCard = generateNewsArticleHTML(articleData);
			articleCardCollection.push(articleCard);
		};
		LOADING_CONTAINER.style.display = 'None';
		appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);
	});
});
