(function(angular){
    'use strict';

    var app = angular.module('core.services', []);

    app.factory('Course', function($resource){
        return $resource('/api/course/:courseId', {}, {
        });
    });
     app.factory('Course_student', function($resource){
        return $resource('/api/course_student/:course_studentId', {}, {
        });
    });

     app.factory('HomePage', function($resource){
        return $resource('/api/homepage/:homepageId', {}, {
        });
    });

     app.factory('User', function($resource){
        return $resource('/api/user/:UserId', {}, {
        });
    });

    app.factory('Twitter', function($resource){
        return $resource('/api/twitter/', {}, {
        });
    });

})(angular);
