/**
 * Created by Jana on 6/17/2016.
 */

(function (angular){
    "use strict";

    angular.module('parliamentApp.HistoryCtrl', [])
        .controller('HistoryCtrl', function($rootScope, $scope, $location, $http){
           $scope.message = "";
            $scope.user = $rootScope.user;
            $scope.imaginary = [];
             $http({
                        method: 'POST',
                        url: '/api/load/',
                        data : {'username': $scope.user.username}
                    }).then(function success(response) {
                        $scope.imaginary = response.data;
                });

           $scope.discardAmendment = function (data) {
               var index = $scope.imaginary.indexOf(data);
               var mojUri = data.uri;
               $scope.imaginary.splice(index, 1);
               $http({
                        method: 'POST',
                        url: '/api/discard/',
                        data : {'uri': mojUri}
                    }).then(function success(response) {
                        $scope.message = "Uspješno brisanje amandmana!";
               });

		   };

            $scope.discardAct = function (data) {
                var index = $scope.imaginary.indexOf(data);
                var mojUri = data.uri;
                $scope.imaginary.splice(index, 1);
                $http({
                        method: 'POST',
                        url: '/api/discard/',
                        data : {'uri': mojUri}
                    }).then(function success(response) {
                        $scope.message = "Uspješno brisanje akta!";
               });
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


        });
}(angular));

