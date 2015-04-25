
myApp.directive("signupstatus", function() {
	return {
		restrict: "E",
		scope: {
			signupState:'=',
			signupMsg:'='
		},
		templateUrl:'html/signupstatus.html'
	}
})


myApp.directive("dashstandings", function() {
	return {
		restrict: "E",
		templateUrl:'html/standings.html',
	}
})

myApp.directive("dashscoreboard", function() {
	return {
		restrict: "E",
		templateUrl:'html/scoreboard.html',
	}
})

myApp.directive("dashrosters", function() {
	return {
		restrict: "E",
		templateUrl:'html/rosters.html',
	}
})

myApp.directive("navigationbar",function() {
	return {
		restrict: "E",
		templateUrl:'html/nav.html',
	}
})

myApp.directive("loginpopup",function() {
	return {
		restrict: "E",
		templateUrl:'html/login.html',
	}
})

myApp.directive("gettingstarted",function() {
	return {
		restrict: "E",
		templateUrl:'html/gettingstarted.html',
	}
})

myApp.directive("signupform",function() {
	return {
		restrict: "E",
		templateUrl:'html/signupform.html',
	}
})

myApp.directive("progressbar",function() {
	return {
		restrict: "E",
		templateUrl:'html/progressbar.html',
	}
})

myApp.directive("carousel",function() {
	return {
		restrict: "E",
		templateUrl:'html/carousel.html',
	}
})
