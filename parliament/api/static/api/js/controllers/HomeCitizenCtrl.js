/**
 * Created by Jana on 6/15/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.HomeCitizenCtrl', [])
        .controller('HomeCitizenCtrl', function($rootScope, $scope, $location){
           $scope.message = "Dobrodosli gradjanine!";
        });
}(angular));
