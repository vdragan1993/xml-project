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
            $scope.show=true;
            console.log($scope.showMe)
            $scope.imaginary=[{uri:"stagod",name:"kakosezove", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", type:"Akt", proces:"Usvojen"}];

           $scope.sSearch = function () {
                console.log("pozvana funkcija za pretragu!");
                $scope.show=!$scope.show;
                $scope.showMe = true;
                           console.log($scope.show)
		   };

            $scope.addAmandmen = function (data) {
                console.log("pozvana funkcija za amandman", data);
                $rootScope.amendment_uri = data;
                $location.path("/new_amendment");
		   };

        });
}(angular));
