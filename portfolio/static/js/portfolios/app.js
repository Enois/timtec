(function(angular){
    'use strict';

    angular.module('portfolios', [
        'portfolios.controllers',
        'portfolios.services',
        'ngRoute',
        'ngResource',
        'django',
        'ui.bootstrap'
    ]);
})(window.angular);

