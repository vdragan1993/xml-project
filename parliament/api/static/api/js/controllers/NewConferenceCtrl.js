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

            $scope.imaginary=[{uri:"stagod",name:"kakosezove", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", type:"Akt", proces:"Usvojen"}];


            $scope.createConference = function () {
                $scope.conference.president = $rootScope.user.username;
                $scope.conference.received = 0;
                console.log($scope.conference);
                var zbir = $scope.conference.against + $scope.conference.abstained;
                if ($scope.conference.for < zbir) {
                    $scope.message2 = "Kreiranje nove sjednice nije uspjelo."
                    $scope.message = "";
                    $location.path("/new_conference");
                }
                else {
                    $scope.actsamendArray = [];
                    angular.forEach($scope.imaginary, function(i){
                        if (i.selected) $scope.actsamendArray.push(i.uri);
                    })
                    console.log("pokupio je:", $scope.actsamendArray);
                    $scope.conference.received = $scope.actsamendArray;
                $http({
                    method: 'POST',
                    url: '/api/create_conference/',
                    data: {'conference': $scope.conference}
                }).then(function success(response) {
                    console.log($scope.conference);
                    $scope.message2 = "";
                    $scope.message = "Nova sjednica je kreirana.";
                    $scope.conference = null;
                    $location.path("/new_conference");
                });
            }
		        };
        });
}(angular));