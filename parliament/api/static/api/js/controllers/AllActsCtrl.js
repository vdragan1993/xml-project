/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.AllActsCtrl', [])
        .controller('AllActsCtrl', function($rootScope, $scope, $location){
           $scope.message = $rootScope.user.username;
            if($rootScope.user){
                $location.path("/all_acts");
            }

             $scope.sSearch = function () {
                console.log("pozvana funkcija za pretragu!");
                $location.path("/all_acts");
		        };
        });
}(angular));
