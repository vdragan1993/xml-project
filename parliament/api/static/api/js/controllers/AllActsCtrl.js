/**
 * Created by Jana on 6/16/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.AllActsCtrl', [])
        .controller('AllActsCtrl', function($rootScope, $scope, $location, $http){
            $scope.show = false;
            $scope.showAll = false;
            $scope.trazi = true;
            $scope.napredna = false;
            $scope.noresults = false;
            $scope.user = $rootScope.user;
            console.log($scope.user.username);
            $scope.imaginary = [];

            $scope.sSearch = function () {
                console.log("pozvana funkcija za prostu pretragu!");
               if($scope.show==true) $scope.show=false;
               if ($scope.ssearch!=undefined) {
                   console.log($scope.ssearch);
                   $http({
                        method: 'POST',
                        url: '/api/simple_search/',
                        data: { 'ssearch' : $scope.ssearch }
                    }).then(function success(response) {
                       if (response.data[0].message == 'Nema rezultata')
                       {
                           console.log(response.data[0].message);
                           $scope.noresults=true;
                           $scope.show=false;
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
                   $scope.imaginary = [];
                   $scope.show = false;
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
                 if($scope.akt.operator ==undefined || $scope.akt.operator=="" ){
                    console.log("usla u if");
                    $scope.akt.operator = "AND";
                }
                if($scope.akt.naslov==undefined && $scope.akt.datum_usvajanja==null && $scope.akt.predlagac==undefined && $scope.akt.datum_pocetka_vazenja==null &&
                $scope.akt.datum_kreiranja==null && $scope.akt.prestanak_vazenja==null && $scope.akt.status==null && $scope.akt.za==null
                && $scope.akt.br_sluzbenog_glasnika==null && $scope.akt.protiv==null && $scope.akt.kategorija==null && $scope.akt.uzdrzani==null){
                    console.log("prazno!");
                    $scope.noresults = true;
                    $scope.show = false;
                } else {
                    $http({
                        method: 'POST',
                        url: '/api/akti/',
                        data: {'akt': $scope.akt}
                    }).then(function success(response) {
                        if (response.data[0].message == 'Nema rezultata') {
                            console.log(response.data[0].message);
                            $scope.noresults = true;
                            $scope.show = false;
                        }
                        else {
                            $scope.imaginary = response.data;
                            $scope.show = true;
                            $scope.noresults = false;
                        }
                    });
                }
		   };

            $scope.addAmandmen = function (data) {
                console.log("pozvana funkcija za amandman", data);
                $rootScope.act = data;
                $location.path("/new_amendment");
		   };

            $scope.showAll= function(){
                $http({
                    method:"GET",
                    url:"/api/svi/"
                }).then(function success(response){
                    $scope.imaginary= response.data;
                   if($scope.show == false) $scope.show=true;
                    else $scope.show=false;
                });
            };

            $scope.clearFields = function() {
                $scope.akt = null;
            };

        });
}(angular));
