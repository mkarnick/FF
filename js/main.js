var myApp = angular.module('myApp', [])

myApp.controller('MainPageCtrl',  ['$scope', 'Service_Shared', 'SignupService', function($scope, Service_Shared, SignupService) {
	window.MY_SCOPE = $scope;
	$scope.signup = function() {
		$scope.showAlert = 1;
		$scope.signupState = "info";
		$scope.signupMsg = "Checking availability...";
		var onSuccess = function(data, status, headers, config) {
			  	$scope.postResult = 1;
			  	$scope.signupState = "success";
			  	$scope.signupMsg = 'Your dashboard was created.';

			  }
		var onFailure = function() {
			  	$scope.postResult = -1;	
			  	$scope.signupState = "danger";
			  	$scope.signupMsg = "Well that didn't work. What did you fuck up?.";
		}
		SignupService.post($scope.inSignupSubname,$scope.inSignupLeagueId, $scope.inSignupEmail, onSuccess, onFailure);

		}

		
}])



myApp.controller('DashCtrl', ['$scope', '$interval', 'Data_TeamList', 'Data_AllRosters','Data_Scoreboard', 'Service_Shared', 'Data_Subdomain', 'SignupService', 'Data_Chat', function($scope, $interval, Data_TeamList, Data_AllRosters, Data_Scoreboard, Service_Shared, Data_Subdomain, SignupService, Data_Chat) {
	window.MY_SCOPE = $scope
	$scope.postResult = 0
	$scope.inWeek = 1
	$scope.signupResult = 0

	$scope.ff_teamList = function() {
		Data_TeamList.get($scope.inLeague, $scope.inYear, function (data) {
			$scope.json_teamList = data;
			$scope.pageLoadPctUpdate();
		})
	}

	$scope.ff_allRosters = function(inYear) {
		Data_AllRosters.get($scope.inLeague, inYear, function (data) {
			$scope.json_allRosters = data;
			$scope.pageLoadPctUpdate();

		})
	}

	$scope.ff_scores = function() {
		Data_Scoreboard.get($scope.inLeague, $scope.inWeek, function (data) {
			$scope.json_scores = data;
			$scope.pageLoadPctUpdate();
		})
	}

	$scope.pageLoadPctUpdate = function()
	{
		$scope.pageLoadItemsDone = $scope.pageLoadItemsDone + 1
		$scope.pageLoadPct = 100*($scope.pageLoadItemsDone / $scope.pageLoadItemsTotal)
	}

	$scope.loadLeagueFromSubdomain = function() {
		Data_Subdomain.get(window.location.origin, function (data) {
			$scope.json_subdomain = data;
			$scope.inSubname = $scope.json_subdomain[0].pk
			$scope.inLeague = data[0].fields.leagueId
			$scope.inYear = 2014;
			$scope.ff_teamList();
			$scope.ff_scores();
			$scope.ff_allRosters(2014);
		})
	}


	$scope.refreshChat = function() {
		Data_Chat.get($scope.inSubname, function (data) {
			$scope.json_chatData = data;
		})
	}
	$interval($scope.refreshChat, 10000);

	$scope.submitChat = function() {
		Data_Chat.post($scope.inSubname, $scope.inChatText, function (data) {
			$scope.json_chatData = data;
			$scope.refreshChat()
		})
	}

	$scope.setScoreWeek = function(inWeek) {
		$scope.inWeek = inWeek;
		$scope.ff_scores();
	}




	$scope.signup = function() {

		$scope.showAlert = 1;
		$scope.signupState = "info";
		$scope.signupMsg = "Checking availability...";
		SignupService.post($scope.inSignupSubname,$scope.inSignupLeagueId, $scope.inSignupEmail, $scope);
		

	}


	$scope.initDashboard = function() {
		$scope.loadLeagueFromSubdomain();
		$scope.pageLoadItemsDone = 0;
		$scope.pageLoadItemsTotal = 3;
		$scope.pageLoadPct = 0;


	}
	
	

	}
    //    $scope.ff_teamList(); // Update the position drop down data
    ]);
	

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
		$http.post('http://karnick.me/chat/submit', {subname:inSub, author:'author', chatText:inChatText}).
			  success(onSuccess).
			  error(onFailure);
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
