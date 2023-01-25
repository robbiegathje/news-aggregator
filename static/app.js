console.log(userLanguageCodes);
console.log(userCountryCodes);

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
