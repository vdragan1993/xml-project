/**
 * Created by Jana on 6/15/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.HomePresidentCtrl', [])
        .controller('HomePresidentCtrl', function($rootScope, $scope, $location){
           $scope.message = $rootScope.user.username;
        });
}(angular));
