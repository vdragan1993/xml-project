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

            $scope.createAct = function () {
                console.log("pozvna funkcija za kreiranje akta!");
                $location.path("/new_act");
		        };
        });
}(angular));