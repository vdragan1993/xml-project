/**
 * Created by Jana on 6/17/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.HistoryCtrl', [])
        .controller('HistoryCtrl', function($rootScope, $scope, $location, $http){
           $scope.message = $rootScope.user.username;
            $scope.user = $scope.user;
            $scope.imaginary=[{uri:"stagod",name:"kakosezove", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", type:"Akt", proces:"Usvojen"}];


           $scope.discardAmendment = function (data) {
                console.log("pozvana funkcija povuci amandmand!");
		   };

            $scope.discardAct = function (data) {
                console.log("pozvana funkcija povuci akt!");
		   };

            $scope.downloadPDF = function (data) {
                if(data.indexOf('pdf') == 0)
                {
                    $http({
                        method: 'GET',
                        url: '/api/'+data.slice(3)+'/pdf/' //odsjekla sam pdf sa pocetka urija
                    }).then(function success(response) {
                        console.log("sta dalje?")
                });
                }
                else if(data.indexOf('xml') == 0)
                $http({
                        method: 'GET',
                        url: '/api/'+data.slice(3)+'/xml/'
                    }).then(function success(response) {
                        console.log("sta dalje?")
                });
                else if(data.indexOf('html') == 0)
                $http({
                        method: 'GET',
                        url: '/api/'+data.slice(4)+'/html/'
                    }).then(function success(response) {
                        console.log("sta dalje?")
                });
		   };


        });
}(angular));

