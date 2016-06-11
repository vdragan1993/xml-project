(function (angular){
    "use strict";

    angular.module('parliamentApp.LoginCtrl', [])
        .controller('LoginCtrl', function($rootScope, $scope, $location){
           $scope.message = 'Angular message example';
        });
}(angular));