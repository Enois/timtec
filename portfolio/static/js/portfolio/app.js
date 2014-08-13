(function(angular){
    'use strict';

    angular.module('portfolio', [
        'portfolio.controllers',
        'portfolio.services',
        'directive.markdowneditor',
        'directive.codemirror',
        'directive.alertPopup',
        'directive.contenteditable',
        'directive.fixedBar',
        'directive.sortable',
        'ngRoute',
        'ngResource',
        'youtube',
        'django',
        'ngTagsInput'
    ]);
})(window.angular);

