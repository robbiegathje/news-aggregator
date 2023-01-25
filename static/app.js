console.log(userLanguageCodes);
console.log(userCountryCodes);

// Two variables are passed through to app.js from inline HTML scripts when
// necessary for the page being displayed.
// The variables are userLanguageCodes and userCountryCodes.
// Each is an Array[] containing two-character strings''
// representing either a language or country code for each user selected
// language and country. See /news/top-stories.html & /news/search.html for
// the originating scripts that utilize back-end user data
// directly from the database such that user preferences are always current.

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
	return response
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
	return response
};

async function getAllStories(language, page=1) {
	let response = await axios.get(
		'/api/all-stories',
		{params: {
			language,
			page
		}}
	);
	return response
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
	return response
};
