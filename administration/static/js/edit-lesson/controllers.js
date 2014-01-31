(function(angular){

    var app = angular.module('edit-lesson');

    app.controller('EditLessonController',
        ['$scope', '$location', 'Course', 'CourseProfessor', 'Lesson', 'VideoData', 'youtubePlayerApi', 'MarkdownDirective',
        function($scope, $location, Course, CourseProfessor, Lesson, VideoData, youtubePlayerApi, MarkdownDirective){
            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };
            // load youtube
            $scope.playerReady = false;
            youtubePlayerApi.loadPlayer().then(function(p){
                $scope.playerReady = true;
            });

            // end load youtube

            $scope.play = function(youtube_id) {
                youtubePlayerApi.loadPlayer().then(function(player){
                    if(player.getVideoData().video_id === youtube_id) return;
                    player.cueVideoById(youtube_id);
                });
            };

            $scope.course = new Course();
            $scope.lesson = new Lesson();
            $scope.lessons = new Lesson();

            $scope.courseProfessors = [];

            $scope.activityTypes = [
                {'name': 'simplechoice', 'label': 'Escolha simples'},
                {'name': 'multiplechoice', 'label': 'Múltipla escolha'},
                {'name': 'trueorfalse', 'label': 'Verdadeiro ou falso'},
                {'name': 'relationship', 'label': 'Relacionar sentenças'},
                {'name': 'html5', 'label': 'HTML5'},
                {'name': 'markdown', 'label': 'Texto simples'}
            ];

            $scope.baseUrl = "/admin/courses/{0}/lessons/{1}/";
            window.onpopstate = function(evt) {
                if(!$scope.lessons.forEach) return;

                var id = /lessons\/(\d+|new)\/?$/.extract($location.path(), 1);
                $scope.lessons.forEach(function(lesson){
                    if( (lesson.id == id) || (id === 'new' && !lesson.id) ) {
                        $scope.setLesson(lesson);
                    }
                });
            };

            /*  Methods */
            $scope.setLesson = function(l) {
                $scope.lesson = l;
                document.title = 'Aula: {0}'.format(l.name || '');

                var path = $scope.baseUrl.format($scope.course.id, (l.id || 'new') );
                $location.path(path);

                if(l.units.length > 0) {
                    $scope.selectUnit(l.units[0]);
                } else {
                    $scope.addUnit();
                }

                if(!$scope.$$phase) $scope.$apply();
            };

            $scope.saveLesson = function() {
                var unitIndex = $scope.lesson.units.indexOf($scope.currentUnit);
                var activityIndex = $scope.currentUnit.activities.indexOf($scope.currentActivity);

                $scope.lesson.saveOrUpdate()
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso.');
                        $scope.selectUnit($scope.lesson.units[unitIndex]);
                        if(activityIndex >= 0) {
                            $scope.currentActivity = $scope.currentUnit.activities[activityIndex];
                        }
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            };

            $scope.publishLesson = function() {
                $scope.lesson.status = 'published';
                $scope.saveLesson();
            };

            $scope.deleteLesson = function() {
                var msg = 'Apagar a aula "{0}" e todo seu conteúdo?'
                          .format($scope.lesson.name);

                if(!confirm(msg)) return;

                function backToCourse () {
                    document.location.href = '/admin/courses/{0}'
                                             .format($scope.course.id);
                }

                var index = $scope.lessons.indexOf($scope.lesson);
                if(index >= 0) {
                    $scope.lessons.splice(index, 1);

                    if($scope.lesson.id){
                        msg = 'A aula "{0}" e todo seu conteúdo foram apagados do sistema.'
                              .format($scope.lesson.name);
                        $scope.lesson.$delete().then(function(){
                            $scope.alert.success(msg);
                            backToCourse();
                        });
                    } else {
                        backToCourse();
                    }
                } else {
                    $scope.lesson = new Lesson();
                }
            };

            $scope.selectUnit = function(u) {
                $scope.currentUnit = u;
                if(u.video && u.video.youtube_id){
                    $scope.play(u.video.youtube_id);
                }
                if($scope.currentUnit.activities) {
                    $scope.currentActivity = $scope.currentUnit.activities[0];
                }
                $scope.newActivityType = null;

                MarkdownDirective.resetEditors();
                MarkdownDirective.refreshEditorsPreview();
            };

            $scope.addUnit = function() {
                if(!$scope.lesson.units) {
                    $scope.lesson.units = [];
                }
                $scope.currentUnit = {'activities': []};
                $scope.lesson.units.push($scope.currentUnit);
            };

            $scope.removeCurrentUnit = function() {
                if(!$scope.lesson.units) return;
                if(!confirm('Apagar unidade?')) return;
                var index = $scope.lesson.units.indexOf($scope.currentUnit);
                $scope.lesson.units.splice(index,1);

                index = index > 0 ? index - 1 : 0;
                if(index < $scope.lesson.units.length) {
                    $scope.selectUnit($scope.lesson.units[index]);
                }
            };

            $scope.setCurrentUnitVideo = function() {
                var youtube_id = $scope.currentUnit.intended_youtube_id;
                if(!$scope.currentUnit.video) {
                    $scope.currentUnit.video = {};
                }
                $scope.currentUnit.video.youtube_id = youtube_id;
                VideoData.load(youtube_id).then(function(data){
                    $scope.currentUnit.video.name = data.entry.title.$t;
                });
                $scope.play(youtube_id);
            };

            $scope.loadActivityTemplateUrl = function() {
                if(!$scope.currentActivity) return;
                return '/static/templates/activities/activity_{0}.html'
                       .format($scope.currentActivity.type);
            };

            $scope.addNewActivity = function() {
                if(!$scope.currentUnit) return;
                if(!$scope.currentUnit.activities) $scope.currentUnit.activities = [];

                var type = $scope.newActivityType;
                $scope.currentActivity = {
                    'type': type,
                    'data': {
                        'question': '',
                        'alternatives': [],
                        'column1': [],
                        'column2': []
                    },
                    'expected': (type==='simplechoice' || type==='html5') ? '' : []
                };
                $scope.currentUnit.activities.push($scope.currentActivity);
                $scope.newActivityType = null;
            };

            $scope.selectActivity = function(activity) {
                $scope.currentActivity = activity;
                MarkdownDirective.resetEditors();
            };

            $scope.removeCurrentActivity = function() {
                if(!$scope.currentUnit) return;
                if(!$scope.currentUnit.activities) return;
                var idx = $scope.currentUnit.activities.indexOf($scope.currentActivity);
                if(idx >= 0) {
                    $scope.currentUnit.activities.splice(idx, 1);
                }
                if(idx > 0) {
                    idx--;
                    $scope.currentActivity = $scope.currentUnit.activities[idx];
                } else if($scope.currentUnit.activities.length > 0) {
                    $scope.currentActivity = $scope.currentUnit.activities[idx];
                } else {
                    $scope.currentActivity = null;
                }
            };
            /*  End Methods */

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/(\d+)\/lessons\/(new|\d+)/);
            if( match ) {
                $scope.isNewLesson = ('new' === match[2]);

                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        $scope.courseProfessors = CourseProfessor.query({ course: course.id });
                        $scope.lesson.course = course.slug;
                        return $scope.courseProfessors.$promise;
                    });

                Lesson.query({course__id: match[1]}).$promise
                    .then(function(lessons){
                        $scope.lessons = lessons;
                        lessons.forEach(function(lesson){
                            if(lesson.id === parseInt(match[2], 10)) {
                                $scope.setLesson(lesson);
                            }
                        });
                        if($scope.isNewLesson) {
                            $scope.addUnit();
                            $scope.lesson.position = $scope.lessons.length;
                            $scope.lessons.push($scope.lesson);
                        }
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            }
            // ^^ como faz isso de uma formula angular ?
        }
    ]);


})(window.angular);
