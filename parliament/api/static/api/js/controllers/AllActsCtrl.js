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


            $scope.imaginary=[{uri:"stagod",name:"kakosezove", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", type:"Akt", proces:"Usvojen"}];


           $scope.sSearch = function () {
                console.log("pozvana funkcija za pretragu!");
                $scope.show=true;
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

            $scope.sNapredna= function () {
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
                $rootScope.amendment_uri = data;
                $location.path("/new_amendment");
		   };

        });
}(angular));
