module.exports = {
	waitForConditionTimeout : 10000,
	
	throwOnMultipleElementsReturned : true,
	
    smokeTestNR: {
        NR_num: '',
        name_choice1: 'ZZZZZZZ 1 TEST NAME DO NOT EXAMINE'
    },
	
    searchScreenTopHold:{
        NR_num: ''
    },

    IDIRCredU : process.env.IDIRCredU,

    IDIRCredP : process.env.IDIRCredP,

    KeycloakCredP : process.env.KeycloakCredP,

    KeycloakCredU : process.env.KeycloakCredU,

    TestCC : process.env.TestCC,

    TestCVD : process.env.TestCVD,

    keycloakAuthURL : process.env.keycloakAuthURL,

    keycloakAuthBody : process.env.keycloakAuthBody,

    token : '',

    extractorTimeOut : 1000,

    exactMatch : 'AIR PACIFIC LIMITED',

    conditionExample : 'INSURANCE',

    trademarkResult : 'Litigation Life Benefit Insurance',

    historyExample : 'GITSELASU FLORISTS LIMITED'
};