/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.NewActCtrl', [])
        .controller('NewActCtrl', function($rootScope, $scope, $location){
           //$scope.message = $rootScope.user.username;
            if($rootScope.user){
                $location.path("/new_act");
            }

            $scope.createConference = function () {
                console.log("pozvna funkcija!");
                $location.path("/new_act");
		        };
        });
}(angular));