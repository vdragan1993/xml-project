/**
 * Created by Jana on 6/15/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.HomeAldermanCtrl', [])
        .controller('HomeAldermanCtrl', function($rootScope, $scope, $location){
           $scope.message = "Dobrodosli odbornice!";
        });
}(angular));
