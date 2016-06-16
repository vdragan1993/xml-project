/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.PendingActsCtrl', [])
        .controller('PendingActsCtrl', function($rootScope, $scope, $location){
           $scope.message = $rootScope.user.username;
            if($rootScope.user){
                $location.path("/pending_acts");
            }

            $scope.addAmandmen = function () {
                console.log("pozvana funkcija za novi amandman!");
		        };

        });
}(angular));
