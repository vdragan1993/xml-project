(function (angular){
    "use strict";

    angular.module('parliamentApp.LoginCtrl', [])
        .controller('LoginCtrl', function($rootScope, $scope, $location,$http){
            if($rootScope.user){
                $location.path("/home");
            }
            else{
                $scope.message = 'Angular message example';
                $scope.user={};
                $scope.login = function () {
                    $http({
                        method: 'POST',
                        url: '/api/users/',
                        data: { 'user' : $scope.user }
                    }).then(function success(response) {
                        if (response.data.user){
                            console.log(response.data.user);
                            $rootScope.user= response.data.user;
                            $location.path("/home");
                        }
                        else
                            $scope.message = 'Incorrect username/password.'
                    });
		        };

            }
        });
}(angular));