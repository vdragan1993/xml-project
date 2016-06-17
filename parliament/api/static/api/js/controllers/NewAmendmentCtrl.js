/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.NewAmendmentCtrl', [])
        .controller('NewAmendmentCtrl', function($rootScope, $scope, $location, $http){
           //$scope.message = $rootScope.user.username;
            if($rootScope.user){
                $location.path("/new_amendment");
            }
            if($rootScope.act){
                $scope.act = $rootScope.act;
            }

            $scope.createAmendment = function (data) {
                console.log("pozvna funkcija za kreiranje amandmana!");
                console.log("amandman za akt ", data);
                $scope.amendment.act = data;
                $http({
                        method: 'POST',
                        url: '/api/create_amendment/',
                        data: { 'amendment' : $scope.amendment }
                    }).then(function success(response) {
                        console.log("poslala sam paramete amandmana");
                        $scope.message = "Novi amandman na akt "+ data + " je kreiran.";
                        $scope.amendment = null;
                        $location.path("/new_amendment");
                });
		        };
        });
}(angular));
