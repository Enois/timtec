(function(angular){

    var app = angular.module('portfolio.controllers', []);

   app.controller('PortfolioEditController',
        ['$scope', 'Portfolio','User', '$filter', 'youtubePlayerApi', 'VideoData', 'FormUpload',
        function($scope, Portfolio,User, $filter, youtubePlayerApi, VideoData, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/portfolios\/([0-9]+)/);
            $scope.portfolio = new Portfolio();
            $scope.user = new User();
            window.s = $scope;
            console.log(window.userId);
            $scope.portfolio.user = window.userId;

            if( match ) {
                $scope.portfolio.$get({id: match[1]})
                    .then(function(portfolio){
                        if(portfolio.video) {
                            youtubePlayerApi.videoId = portfolio.video.youtube_id;
                        }
                        document.title = 'Portfolio: {0}'.format(portfolio.name);
                        $scope.addThumb = !portfolio.thumbnail_url;

                    }).then(function(){
                        $scope.user.$get({id: $scope.portfolio.user});
                        return $scope.user.promise;
                    })

            }
            // ^^ como faz isso de uma formula angular ?

            var player;
            $scope.playerReady = false;
            youtubePlayerApi.loadPlayer().then(function(p){
                player = p;
                $scope.playerReady = true;
            });

            $scope.$watch('portfolio.video.youtube_id', function(vid, oldVid){
                if(!vid || vid === oldVid) return;
                if(player) player.cueVideoById(vid);
                VideoData.load(vid).then(function(data){
                    $scope.portfolio.video.name = data.entry.title.$t;
                });
            });

            function showFieldErrors(response) {
                $scope.errors = response.data;
                var messages = [];
                for (var att in response.data) {
                    var message = response.data[att];
                    if (Portfolio.fields && Portfolio.fields[att]) {
                        message = Portfolio.fields[att].label + ': ' + message;
                    }
                    messages.push(message);
                }
                $scope.alert.error('Encontramos alguns erros!', messages, true);
            }

            $scope.saveThumb = function() {
                if(! $scope.thumbfile) {
                    return;
                }

                if ($scope.portfolio.id) {
                    var fu = new FormUpload();
                    fu.addField('thumbnail', $scope.thumbfile);
                    // return a new promise that file will be uploaded
                    return fu.sendTo('/api/portfoliothumbs/' + $scope.portfolio.id)
                        .then(function(){
                            $scope.alert.success('A imagem atualizada.');
                        });
                }
            };

            $scope.savePortfolio = function() {
                if(!$scope.portfolio.hasVideo()){
                    delete $scope.portfolio.video;
                }
                $scope.portfolio.save()
                    .then(function(){
                        return $scope.saveThumb();
                    })
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso!');
                    })['catch'](showFieldErrors);
            };

            $scope.publishPortfolio = function() {
                $scope.portfolio.status = 'published';
                $scope.savePortfolio();
            };

            $scope.deletePortfolio = function() {
                if(!confirm('Tem certeza que deseja remover este curso?')) return;

                $scope.portfolio.$delete()
                    .then(function(){
                        document.location.href = '/';
                    });
            };

        }
    ]);

})(window.angular);
