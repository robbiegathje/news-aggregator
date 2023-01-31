// Two variables are passed through to top-stories.js from inline HTML scripts.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user-selected
// language and country. See /news/top-stories.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

let PAGE_NUMBER_OF_RESULTS = 1;

document.addEventListener('DOMContentLoaded', async function() {
	const FETCH_BUTTON = document.getElementById('fetch');
	const FETCH_CONTAINER = document.getElementById('fetch-container');
	const LOADING_CONTAINER = document.getElementById('loading');
	const STORIES_CONTAINER = document.getElementById('stories');

	let response = await getTopStories(
		userLanguageCodes.join(','), userCountryCodes.join(',')
	);
	let articleCardCollection = [];
	for (let articleData of response.data.data) {
		let articleCard = generateNewsArticleHTML(articleData);
		articleCardCollection.push(articleCard);
	};
	LOADING_CONTAINER.style.display = 'None';
	FETCH_CONTAINER.style.display = '';
	appendAllNewsArticles(articleCardCollection, STORIES_CONTAINER);

	FETCH_BUTTON.addEventListener('click', async function() {
		LOADING_CONTAINER.style.display = '';
		PAGE_NUMBER_OF_RESULTS ++;
		let response = await getTopStories(
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
