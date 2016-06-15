/**
 * Created by Jana on 6/15/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.LogoutCtrl', [])
        .controller('LogoutCtrl', function($rootScope, $scope, $location,$http){
                $scope.user=$rootScope.user;

                $scope.logout = function () {
                    $scope.message = 'Uspešno ste se izlogovali.';
                    $rootScope.user= null;
                    $location.path("/");
		        };


        });
}(angular));
