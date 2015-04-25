var myApp = angular.module('myApp', [])

myApp.controller('DashCtrl', ['$scope', 'Data_TeamList', 'Data_AllRosters','Data_Scoreboard', 'Service_Shared', 'Data_Subdomain', 'SignupService', function($scope, Data_TeamList, Data_AllRosters, Data_Scoreboard, Service_Shared, Data_Subdomain, SignupService) {
	window.MY_SCOPE = $scope

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
			$scope.inLeague = data[0].fields.leagueId
			$scope.inYear = 2014;
			$scope.ff_teamList();
			$scope.ff_scores();
			$scope.ff_allRosters(2014);
		})
	}

	$scope.setScoreWeek = function(inWeek) {
		$scope.inWeek = inWeek;
		$scope.ff_scores();
	}




	$scope.signup = function() {
		SignupService.post($scope.inSignupSubname,$scope.inSignupLeagueId);
		$scope.showAlert = 1;
		

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
	
myApp.controller('MainPageCtrl',  ['$scope', 'Service_Shared', 'SignupService', function($scope, Service_Shared, SignupService) {
	window.MY_SCOPE = $scope;
	$scope.signupState="danger";
	$scope.signupMsg="This is the message";
	$scope.signup = function() {
			SignupService.post($scope.inSignupSubname,$scope.inSignupLeagueId);
			$scope.showAlert = 1;

		}

		
}])

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



myApp.factory('SignupService',function($http) {
	var SignupService = {};
  

	SignupService.post = function(inSub, inLeague) {
		$http.post('/signup', {subname:inSub, leagueId:inLeague}).
		  success(function(data, status, headers, config) {

		  }).
		  error(function(data, status, headers, config) {

		  });
	}

	return SignupService

	})
