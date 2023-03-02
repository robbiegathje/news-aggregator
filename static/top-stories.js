// Two variables are passed through to top-stories.js from inline HTML scripts.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user-selected
// language and country. See /news/top-stories.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

let PAGE_NUMBER_OF_RESULTS = 1;

document.addEventListener('DOMContentLoaded', async function () {
	const FETCH_BUTTON = document.getElementById('fetch');
	const FETCH_CONTAINER = document.getElementById('fetch-container');
	const LOADING_CONTAINER = document.getElementById('loading');
	const STORIES_CONTAINER = document.getElementById('stories');

	let response = await getTopStories(
		userLanguageCodes.join(','),
		userCountryCodes.join(',')
	);
	let articleCardCollection = [];
	if (response.data.meta['found'] === 0) {
		FETCH_CONTAINER.classList.add('d-none');
		let containingBootstrapColumn = document.createElement('div');
		containingBootstrapColumn.className =
			'col justify-content-center text-center';
		let noResultsMessage = document.createElement('h5');
		noResultsMessage.className = 'display-5';
		noResultsMessage.innerText = 'No Top Stories found today.';
		let userSuggestion = document.createElement('aside');
		userSuggestion.className = 'display-9';
		userSuggestion.innerText =
			'However, this may be due to your chosen languages not being commonly spoken in your selected countries. If that is the case, please change your user preferences.';
		containingBootstrapColumn.append(noResultsMessage);
		containingBootstrapColumn.append(userSuggestion);
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

	FETCH_BUTTON.addEventListener('click', async function () {
		LOADING_CONTAINER.classList.remove('d-none');
		PAGE_NUMBER_OF_RESULTS++;
		let response = await getTopStories(
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
