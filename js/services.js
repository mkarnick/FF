
myApp.factory('Service_Shared', function() {
	 var Service_Shared = 'initSavedData'
	 Service_Shared.set = function (data) {
	   	savedData = data;
	 }
	 Service_Shared.get = function () {
	  	return savedData;
	 }

	 return Service_Shared

});


// Create a service to populate the Team filter drop-down
myApp.factory('Data_TeamList', function($http) {
	var Data_TeamList = {};
	Data_TeamList.get = function(inLeague, inYear, callback) {
		$http.get('http://karnick.me/' + inLeague + '/' + inYear + '/teamlist').success(function(data) {
			callback(data);
		});
	};
	return Data_TeamList;
});

//http://games.espn.go.com/ffl/scoreboard?leagueId=716644&matchupPeriodId=1



myApp.factory('Data_Scoreboard', function($http) {
	var Data_Scoreboard = {};
	Data_Scoreboard.get = function(inLeague, inWeek, callback) {
		$http.get('http://karnick.me/' + inLeague + '/scores/' + inWeek).success(function(data) {
			callback(data);
		});
	};
	return Data_Scoreboard;
});

// Create a service to retrieve all rosters
myApp.factory('Data_AllRosters', function($http) {
	var Data_AllRosters = {};
	Data_AllRosters.get = function(inLeague, inYear, callback) {

		$http.get('http://karnick.me/' + inLeague + '/roster/' + inYear).success(function(data) {
			callback(data);
		});
	};
	return Data_AllRosters;
});



// Create a service to retrieve all rosters
myApp.factory('Data_Subdomain', function($http) {
	var Data_Subdomain = {};
	Data_Subdomain.get = function(requestedUrl, callback) {
		$http.get(requestedUrl + '/getsub').success(function(data) {
			callback(data);
		});
	};
	return Data_Subdomain;
});


// Create a service to retrieve chat info
myApp.factory('Data_Chat', function($http) {
	var Data_Chat = {};
	Data_Chat.get = function(inSub, callback) {
		$http.get('http://karnick.me/chat/get/' + inSub).success(function(data) {
			callback(data);
		});
	};
	Data_Chat.post = function(inSub, inChatText, onSuccess) {
		$http.post('chat/submit', {subname:inSub, author:'author', chatText:inChatText}).
			  success(onSuccess).
			  error();
	}
	return Data_Chat;
});

myApp.factory('SignupService',function($http) {
	var SignupService = {};
  
	var result = 0
	SignupService.post = function(inSub, inLeague, inEmail, onSuccess, onFailure) {
		$http.post('/signup', {subname:inSub, leagueId:inLeague, email:inEmail}).
			  success(onSuccess).
			  error(onFailure);
	}

	return SignupService

	})


myApp.factory('LoginService',function($http) {
	var LoginService = {};
  
	var result = 0
	LoginService.post = function(inUser, inPassword, onSuccess, onFailure) {
		$http.post('/login', {username:inUser, password:inPassword}).
			  success(onSuccess).
			  error(onFailure);
	}

	LoginService.get = function(inUser, callback) {
	$http.get('/userinfo/' + inUser).success(function(data) {
			callback(data);
		});
	}



	return LoginService

	})
