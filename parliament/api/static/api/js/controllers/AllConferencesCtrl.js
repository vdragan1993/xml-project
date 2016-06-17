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
            $scope.conferences = [{president:"dagan",date:"16-06-2016", for:19, against:4, abstained:2, received:2},
                    {president:"dagan",date:"10-06-2016", for:21, against:2, abstained:2, received:7},
                    {president:"dagan",date:"16-06-2016", for:25, against:0, abstained:0, received:5}];
        });
}(angular));