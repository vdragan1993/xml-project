/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.AllConferencesCtrl', [])
        .controller('AllConferencesCtrl', function($rootScope, $scope, $location){
           $scope.message = $rootScope.user.username;
            if($rootScope.user){
                $location.path("/all_conferences");
            }
        });
}(angular));