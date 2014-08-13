(function(angular){
    'use strict';
    var app = angular.module('portfolios.filters',[]);

      app.filter('offset', function() {
  return function(input, start) {
    start = parseInt(start, 10);
    return input.slice(start);
  };
});
})(window.angular);