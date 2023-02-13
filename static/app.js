const ARTICLE_CARD_LINK_TEXT = 'Read More';

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
	containingBootstrapColumn.className = 'col-12 col-md-6 col-xl-4 my-3';
	let articleCard = document.createElement('div');
	articleCard.className = 'card h-100';
	let cardImage = document.createElement('img');
	cardImage.src = articleData.image_url;
	cardImage.className = 'card-img-top h-50';
	let cardBody = document.createElement('div');
	cardBody.className = 'card-body';
	let cardTitle = document.createElement('h5');
	cardTitle.innerText = articleData.title;
	cardTitle.className = 'card-title';
	let cardSourceSubtitle = document.createElement('h6');
	cardSourceSubtitle.innerText = `${articleData.source} | ${articleData.published_at.slice(0, 10)}`;
	cardSourceSubtitle.className = 'card-subtitle text-secondary';
	let cardText = document.createElement('p');
	cardText.innerText = articleData.description;
	cardText.className = 'card-text';
	let cardSourceLink = document.createElement('a');
	cardSourceLink.href = articleData.url;
	cardSourceLink.innerText = ARTICLE_CARD_LINK_TEXT;
	cardSourceLink.className = 'btn btn-primary';
	cardBody.append(cardTitle);
	cardBody.append(cardSourceSubtitle);
	cardBody.append(cardText);
	cardBody.append(cardSourceLink);
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
