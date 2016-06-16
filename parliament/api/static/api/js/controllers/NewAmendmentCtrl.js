/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.NewAmendmentCtrl', [])
        .controller('NewAmendmentCtrl', function($rootScope, $scope, $location){
           //$scope.message = $rootScope.user.username;
            if($rootScope.user){
                $location.path("/new_amendment");
            }

            $scope.createConference = function () {
                $scope.message = "pozvana funkcija!";
                console.log("pozvna funkcija!");
                $location.path("/new_conference");
		        };
        });
}(angular));
