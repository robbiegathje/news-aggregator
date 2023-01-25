// The parameters for getTopStories() are based on the query string expectations
// of the internal API. The same is true for other "getStories" functions below.
async function getTopStories(language, locale, page=1) {
	let response = await axios.get(
		'/api/top-stories',
		{params: {
			language,
			locale,
			page
		}}
	);
	return response;
};

async function getTopStoriesBySearchTerm(
	search, days, language, locale, page=1
	) {
	let response = await axios.get(
		'/api/top-stories',
		{params: {
			search,
			days,
			language,
			locale,
			page
		}}
	);
	return response;
};

async function getAllStories(language, page=1) {
	let response = await axios.get(
		'/api/all-stories',
		{params: {
			language,
			page
		}}
	);
	return response;
};

async function getAllStoriesBySearchTerm(search, days, language, page=1) {
	let response = await axios.get(
		'/api/all-stories',
		{params: {
			search,
			days,
			language,
			page
		}}
	);
	return response;
};

function generateNewsArticleHTML(articleData) {
	let containingBootstrapColumn = document.createElement('div');
	containingBootstrapColumn.className = 'col-4';
	let articleCard = document.createElement('div');
	articleCard.className = 'card';
	let cardImage = document.createElement('img');
	cardImage.src = articleData.image_url;
	cardImage.className = 'card-img-top';
	let cardBody = document.createElement('div');
	cardBody.className = 'card-body';
	let cardTitle = document.createElement('h5');
	cardTitle.innerText = articleData.title;
	cardTitle.className = 'card-title';
	let cardText = document.createElement('p');
	cardText.innerText = articleData.description;
	cardText.className = 'card-text';
	let cardSource = document.createElement('a');
	cardSource.href = articleData.url;
	cardSource.innerText = articleData.source;
	cardSource.className = 'btn btn-primary';
	cardBody.append(cardTitle);
	cardBody.append(cardText);
	cardBody.append(cardSource);
	articleCard.append(cardImage);
	articleCard.append(cardBody);
	containingBootstrapColumn.append(articleCard)
	return containingBootstrapColumn;
};

function appendAllNewsArticles(articleCardCollection, DOMContainer) {
	for (let articleHTML of articleCardCollection) {
		DOMContainer.append(articleHTML);
	};
};
