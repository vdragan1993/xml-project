/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.NewConferenceCtrl', [])
        .controller('NewConferenceCtrl', function($rootScope, $scope, $location, $http){
           $scope.message = "";
            $scope.message2 = "";
            if($rootScope.user){
                $location.path("/new_conference");
            }

            $scope.createConference = function () {
                $scope.conference.president = $rootScope.user.username;
                console.log($scope.conference);
                var zbir = $scope.conference.against + $scope.conference.abstained;
                console.log(zbir);
                if ($scope.conference.for < zbir) {
                    $scope.message2 = "Ne može se kreirati sjednica!"
                    $location.path("/new_conference");
                }
                else {

                $http({
                    method: 'POST',
                    url: '/api/create_conference/',
                    data: {'conference': $scope.conference}
                }).then(function success(response) {
                    console.log($scope.conference);
                    $scope.message = "Uspješno kreirana nova sjednica!";
                    $location.path("/new_conference");
                });
            }
		        };
        });
}(angular));