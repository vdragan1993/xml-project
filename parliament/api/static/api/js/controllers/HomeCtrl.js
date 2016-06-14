(function (angular){
    "use strict";

    angular.module('parliamentApp.HomeCtrl', [])
        .controller('HomeCtrl', function($rootScope, $scope, $location){
           $scope.message = $rootScope.user.username;
        });
}(angular));