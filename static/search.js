// Two variables are passed through to search.js from inline HTML scripts.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user-selected
// language and country. See /news/search.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

let PAGE_NUMBER_OF_RESULTS = 1;

document.addEventListener('DOMContentLoaded', async function () {
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

	SEARCH_FORM.addEventListener('submit', async function (event) {
		event.preventDefault();
		USER_SEARCH_SETTINGS.classList.add('d-none');
		LOADING_CONTAINER.classList.remove('d-none');
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
		if (response.data.meta['found'] === 0) {
			FETCH_CONTAINER.classList.add('d-none');
			let containingBootstrapColumn = document.createElement('div');
			containingBootstrapColumn.className =
				'col justify-content-center text-center';
			let noResultsMessage = document.createElement('h5');
			noResultsMessage.className = 'display-5';
			noResultsMessage.innerText = 'No Results Found.';
			containingBootstrapColumn.append(noResultsMessage);
			STORIES_CONTAINER.append(containingBootstrapColumn);
		} else {
			for (let articleData of response.data.data) {
				let articleCard = generateNewsArticleHTML(articleData);
				articleCardCollection.push(articleCard);
			}
			FETCH_CONTAINER.classList.remove('d-none');
			appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);
		}
		LOADING_CONTAINER.classList.add('d-none');
		USER_SEARCH_SETTINGS.classList.remove('d-none');
	});

	FETCH_BUTTON.addEventListener('click', async function () {
		LOADING_CONTAINER.classList.remove('d-none');
		PAGE_NUMBER_OF_RESULTS++;
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
		}
		LOADING_CONTAINER.classList.add('d-none');
		appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);
	});
});
