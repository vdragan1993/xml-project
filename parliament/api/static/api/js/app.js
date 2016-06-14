(function(angular){
    "use strict";
    var parliamentApp = angular.module('parliamentApp', ['parliamentApp.controllers', 'ngRoute']);

    parliamentApp.config(function($locationProvider) {
       $locationProvider.html5Mode(true);
    });

    // force AngularJS to use [[]] instead of {{}}
    parliamentApp.config(function($interpolateProvider) {
       $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });

    parliamentApp.config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '/static/api/pages/login.html',
                controller: 'LoginCtrl'
            })
            .when('/home',{
                templateUrl: '/static/api/pages/home.html',
                controller: 'HomeCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });

}(angular));