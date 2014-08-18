(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course','Course_student','HomePage','User','Twitter', function ($scope, Course,Course_student, HomePage, User, Twitter) {
         $scope.myInterval = 8000;
         var id_course =null;
         $scope.user_number_per_courses=[];

        $scope.home_page = new HomePage();

        HomePage.query({}).$promise
                    .then(function(home_pages){
                         $scope.home_pages = home_pages;
                          home_pages.forEach(function(homepage) {
                             if (homepage.id === parseInt(1)) {
                                  $scope.home_page=homepage;
                             }
          })
          });


        function compare_by_position(a,b) {
            if (a.home_position < b.home_position)
               return -1;
            if (a.home_position > b.home_position)
               return 1;
            return 0;
        }

        $scope.courses = Course.query({'home_published': 'True'}, function(courses) {
            courses.sort(compare_by_position);
            $scope.courses_rows = [];
            var row = [];
            var index = 0;
            angular.forEach(courses, function(course) {
                row.push(course);
                if (index == 1) {
                    $scope.courses_rows.push(row);
                    row = [];
                    index = 0;
                } else
                    index++;
            });
        });

        $scope.upcoming_courses = Course.query({'home_published': 'True'}, function(upcoming_courses) {

            $scope.upcoming_courses_rows_3 = [];

            for (var i = 0; i < upcoming_courses.length; i++) {
                var row = [];
                row[0] = $scope.upcoming_courses[i];


                 id_course= row[0].id;
                 $scope.students = Course_student.query({'course':id_course}, function(students) {
                      $scope.students = students;
                     row[0].user_number=students.length;

        });
                if (upcoming_courses.length - i > 1){
                    // normal case
                    row[1] = $scope.upcoming_courses[i+1];
                    id_course= row[1].id;
                    $scope.students = Course_student.query({'course':id_course}, function(students) {
                    $scope.students = students;
                   row[1].user_number=students.length;
        });

                    if (upcoming_courses.length - i > 2)

                        row[2] = $scope.upcoming_courses[i+2];


                    else
                        row[2] = $scope.upcoming_courses[upcoming_courses.length - i - 2];

                } else {
                    row[1] = $scope.upcoming_courses[upcoming_courses.length - i - 1];
                     id_course= row[1].id;
                      $scope.students = Course_student.query({'course':id_course}, function(students) {
                      $scope.students = students;
                    row[1].user_number=students.length;
                });
                    row[2] = $scope.upcoming_courses[upcoming_courses.length - i];
                     id_course= row[2].id;
                $scope.students = Course_student.query({'course':id_course}, function(students) {
                      $scope.students = students;
                       row[2].user_number=students.length;
                });
                }

                $scope.upcoming_courses_rows_3.push(row);
            }
        });

//slider Mentores 2
         $scope.coming_teachers = User.query({'groups__name': 'professors'}, function(coming_teachers) {

            $scope.coming_teachers_rows_3 = [];

            for (var i = 0; i < coming_teachers.length; i++) {
                var row = [];
                row[0] = $scope.coming_teachers[i];

                if (coming_teachers.length - i > 1){
                    // normal case
                    row[1] = $scope.coming_teachers[i+1];
                    if (coming_teachers.length - i > 2)
                        row[2] = $scope.coming_teachers[i+2];
                    else
                        row[2] = $scope.coming_teachers[coming_teachers.length - i - 2];
                } else {
                    row[1] = $scope.coming_teachers[coming_teachers.length - i - 1];
                    row[2] = $scope.coming_teachers[coming_teachers.length - i];
                }
                $scope.coming_teachers_rows_3.push(row);
            }
        });




//        Slider Mentores
        $scope.coming_mentores = User.query({'groups__name': 'professors'}, function(coming_mentores) {

            $scope.coming_mentores_2 = [];

            for (var i = 0; i < coming_mentores.length; i++) {
                var row = [];
                row[0] = $scope.coming_mentores[i];

                if (coming_mentores.length - i > 1){
                    // normal case
                    row[1] = $scope.coming_mentores[i+1];
                } else {
                    row[1] = $scope.coming_mentores[coming_mentores.length - i - 1];
                }


                $scope.coming_mentores_2.push(row);

            }
        });


        $scope.twits = Twitter.query({});
    }]);

})(angular);

