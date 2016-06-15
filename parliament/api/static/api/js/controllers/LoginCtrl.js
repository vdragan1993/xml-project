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
                console.log($scope.user);
                $scope.login = function () {
                    $http({
                        method: 'POST',
                        url: '/api/users/',
                        data: { 'user' : $scope.user }
                    }).then(function success(response) {
                        // for superuser (predsednik)
                        if (response.data.user && response.data.user.is_superuser && response.data.user.is_staff){
                            console.log(response.data.user.is_superuser);
                            $rootScope.user= response.data.user;
                            $location.path("/president");
                        }
                        // for staff user (odbornik)
                        else if(response.data.user && response.data.user.is_superuser==false && response.data.user.is_staff){
                            console.log("ti si odbornik");
                            $rootScope.user= response.data.user;
                            $location.path("/alderman");
                        }
                        // for regular user (gradjanin)
                        else if(response.data.user && response.data.user.is_superuser==false && response.data.user.is_staff==false){
                           console.log("ti si gradjanin");
                            $rootScope.user= response.data.user;
                            $location.path("/citizen");
                        }
                        else
                            $scope.message = 'Netačno korisničko ime ili lozinka!'
                    });
		        };




            }
        });
}(angular));