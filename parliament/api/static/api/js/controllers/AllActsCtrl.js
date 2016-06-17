/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.AllActsCtrl', [])
        .controller('AllActsCtrl', function($rootScope, $scope, $location, $http){
           $scope.message = $rootScope.user.username;
            $scope.show = false;
            $scope.trazi = true;
            $scope.napredna = false;
            $scope.noresults = false;

            $scope.imaginary=[{uri:"stagod",name:"kakosezove", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", type:"Akt", proces:"Usvojen"}];


           $scope.sSearch = function () {
                console.log("pozvana funkcija za prostu pretragu!");
               if ($scope.ssearch!=undefined) {
                   console.log($scope.ssearch);
                   var pretraga = $scope.ssearch;
                   $http({
                        method: 'POST',
                        url: '/api/simple_search/',
                        data: { 'ssearch' : $scope.ssearch }
                    }).then(function success(response) {
                        console.log("poslala sam parametar pretrage");
                });

               }
               else {
                   console.log("niste nista uneli");
                   $scope.noresults = true;
               }
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

            $scope.aSearch= function () {
                console.log("pozvana funkcija za naprednu pretragu!",$scope.akt);
                $http({
                        method: 'POST',
                        url: '/api/akti/',
                        data: { 'akt' : $scope.akt }
                    }).then(function success(response) {
                    $scope.show=true;
                    $scope.imaginary = response.data;
                });
		   };

            $scope.addAmandmen = function (data) {
                console.log("pozvana funkcija za amandman", data);
                $rootScope.act = data;
                $location.path("/new_amendment");
		   };

        });
}(angular));
