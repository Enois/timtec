
(function (angular) {
    'use strict';
    /* Services */

     var app = angular.module('portfolios.services', []);


 app.factory('User', function($resource){
        return $resource('/api/user/:id', {'id':'@id'});
    });


 app.factory('Portfolio', function($resource){
        return $resource('/api/portfolio/:id', {'id':'@id'});
    });



})(angular);


