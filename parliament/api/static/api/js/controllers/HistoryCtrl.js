/**
 * Created by Jana on 6/17/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.HistoryCtrl', [])
        .controller('HistoryCtrl', function($rootScope, $scope, $location, $http){
           $scope.message = "";
            $scope.user = $scope.user;
            var acts = [{uri:"stagod",name:"kakosezove", proponent: "dragan", type:"Akt", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", proponent: "marko",type:"Akt", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3",proponent: "marko", type:"Akt", proces:"Usvojen"}];
            var amendments = [{uri:"stagod",name:"kakosezove",proponent: "marina", type:"Amandman", proces:"Usvojen"},
                    {uri:"stagod2",name:"kakosezove2", proponent: "marko", type:"Amandman", proces:"U procesu"},
                    {uri:"stagod3",name:"kakosezove3", proponent: "dragan", type:"Amandman", proces:"Usvojen"}];
            var all = acts.concat(amendments);

            $scope.imaginary=all;


           $scope.discardAmendment = function (data) {
               var index = $scope.imaginary.indexOf(data);
                $scope.imaginary.splice(index, 1);
                console.log("pozvana funkcija povuci amandmand!");
               $scope.message = "Uspješno brisanje amandmana!";
		   };

            $scope.discardAct = function (data) {
                var index = $scope.imaginary.indexOf(data);
                $scope.imaginary.splice(index, 1);
                console.log("pozvana funkcija povuci akt!");
                $scope.message = "Uspješno brisanje akta!";
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

