(function(angular){
    'use strict';

    angular.module('portfolio', [
        'portfolio.controllers',
        'portfolio.services',
        'directive.markdowneditor',
        'directive.codemirror',
        'ngRoute',
        'ngResource',
        'youtube',
        'django'
    ]);
})(window.angular);