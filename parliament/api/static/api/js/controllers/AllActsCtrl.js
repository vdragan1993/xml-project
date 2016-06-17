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

            /*
            $scope.imaginary=[{uri:"stagod",name:"kakosezove", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", type:"Akt", proces:"Usvojen"}];
            */
            $scope.imaginary = [];

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
                       if (response.data[0].message == 'Nema rezultata')
                       {
                            console.log(response.data[0].message);
                       }
                       else {
                           $scope.imaginary = response.data;
                           $scope.show = true;
                       }
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
                        method: 'POST',
                        url: '/api/pdf/', //odsjekla sam pdf sa pocetka urija
                        data : {'uri':data.slice(3)},
                        responseType: 'arraybuffer'
                    }).then(function success(response) {
                        var blob = new Blob([response.data], {type:"application/pdf"});
                        var objectUrl = URL.createObjectURL(blob);
                        window.open(objectUrl);
                });
                }
                else if(data.indexOf('xml') == 0){
                console.log(data.slice(3));
                $http({
                        method: 'POST',
                        url: '/api/xml/',
                        data : {'uri':data.slice(3)},
                        responseType: 'arraybuffer'
                    }).then(function success(response) {
                        var blob = new Blob([response.data], {type:"application/xml"});
                        var objectUrl = URL.createObjectURL(blob);
                        window.open(objectUrl);
                });}
                else if(data.indexOf('html') == 0) {
                    $http({
                        method: 'POST',
                        url: '/api/html/',
                        data: {'uri' : data.slice(4)},
                        responseType: 'arraybuffer'
                    }).then(function success(response) {
                        var blob = new Blob([response.data], {type:"text/html"});
                        var objectUrl = URL.createObjectURL(blob);
                        window.open(objectUrl);
                    });
                }
		   };

            $scope.aSearch= function () {
                console.log("pozvana funkcija za naprednu pretragu!",$scope.akt);
                $http({
                        method: 'POST',
                        url: '/api/akti/',
                        data: { 'akt' : $scope.akt }
                    }).then(function success(response) {
                   if (response.data[0].message == 'Nema rezultata')
                       {
                            console.log(response.data[0].message);
                       }
                       else {
                           $scope.imaginary = response.data;
                           $scope.show = true;
                       }
                });
		   };

            $scope.addAmandmen = function (data) {
                console.log("pozvana funkcija za amandman", data);
                $rootScope.act = data;
                $location.path("/new_amendment");
		   };

            $scope.prikaziSve= function(){
                $http({
                    method:"GET",
                    url:"/api/svi/"
                }).then(function success(response){
                    $scope.imaginary= response.data;
                   $scope.show= true;
                });
            };

        });
}(angular));
