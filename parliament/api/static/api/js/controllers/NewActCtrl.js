/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.NewActCtrl', [])
        .controller('NewActCtrl', function($rootScope, $scope, $location, $http){
           $scope.message = "";
            if($rootScope.user){
                $location.path("/new_act");
            }

            $scope.createAct = function () {
                console.log("pozvna funkcija za kreiranje akta!");
                console.log("akt ", $scope.act);
                $http({
                        method: 'POST',
                        url: '/api/create_act/',
                        data: { 'act' : $scope.act }
                    }).then(function success(response) {
                        console.log("poslala sam paramete akta");
                        $scope.message = "Uspješno ste kreirali novi akt!";
                        $location.path("/new_act");
                });


		        };
        });
}(angular));