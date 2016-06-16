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
            .when('/citizen',{
                templateUrl: '/static/api/pages/home_citizen.html',
                controller: 'HomeCitizenCtrl'
            })
            .when('/president',{
                templateUrl: '/static/api/pages/home_president.html',
                controller: 'HomePresidentCtrl'
            })
            .when('/alderman',{
                templateUrl: '/static/api/pages/home_alderman.html',
                controller: 'HomeAldermanCtrl'
            })
            .when('/all_conferences',{
                templateUrl: '/static/api/pages/all_conferences.html',
                controller: 'AllConferencesCtrl'
            })
            .when('/new_conference',{
                templateUrl: '/static/api/pages/new_conference.html',
                controller: 'NewConferenceCtrl'
            })
            .when('/all_acts',{
                templateUrl: '/static/api/pages/all_acts.html',
                controller: 'AllActsCtrl'
            })
            .when('/new_act',{
                templateUrl: '/static/api/pages/new_act.html',
                controller: 'NewActCtrl'
            })
            .when('/new_amendment',{
                templateUrl: '/static/api/pages/new_amendment.html',
                controller: 'NewAmendmentCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });

}(angular));