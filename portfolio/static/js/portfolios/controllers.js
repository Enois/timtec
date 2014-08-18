(function(angular){

var app = angular.module('portfolios.controllers', [ ]);

app.controller('PortfoliosController',
    ['$scope', 'Portfolio','User',
    function ($scope,Portfolio,User) {
         $scope.user=new User();
         $scope.datalist=Portfolio.query({status: 'published'});







        $scope.showData = function () {


            $scope.curPage = 0;
            $scope.pageSize = 16;
            $scope.dataportfolios=  $scope.datalist;




            $scope.numberOfPages = function () {
                return Math.ceil($scope.dataportfolios.length / $scope.pageSize);
            };

        }

    }]);

angular.module('portfolios').filter('pagination', function()
{
 return function(input, start)
 {
  start = +start;
  return input.slice(start);
 };
});


})(window.angular);
