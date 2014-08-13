
(function (angular) {
    'use strict';
    /* Services */

     var app = angular.module('portfolio.services', []);


      app.factory('Portfolio', ['$resource', 'getRestOptions', function($resource, getRestOptions) {

        var Portfolio = $resource('/api/portfolio/:id', {'id':'@id'});
        Portfolio.prototype.isDraft = function() { return this.status === 'draft'; };
        Portfolio.prototype.isPublished = function() { return this.status === 'published'; };

        Portfolio.prototype.saveOrUpdate = function() {
            if(!this.name) this.name = this.user+'Sem título';
            if(!this.status) this.status = 'draft';
            return this.$save();
        };
         Portfolio.prototype.hasVideo = function(){
            return this.video && this.video.youtube_id &&
                   this.video.youtube_id.length > 0;
        };
          getRestOptions('/api/portfolio').success(function(data) {
            Portfolio.fields = angular.copy(data.actions.POST);
        });
        return Portfolio;
    }]);


 app.factory('User', function($resource){
        return $resource('/api/user/:id', {'id':'@id'});
    });
       /**
     * A object that fetch info from Youtube. It expects a video ID and returns
     * a promise that video info will be fetched.
     */
    app.factory('VideoData', ['$document', '$q', function($document, $q){
        var funcName = 'getYoutubeData'+Math.random().toString(16).substring(2);

        var VideoData = function() {
            this.load = function(vid) {
                this.deferred = $q.defer();

                // youtube service
                this.src = 'http://gdata.youtube.com/feeds/api/videos/'+
                            vid + '?alt=json&callback=' + funcName;

                var script = $document[0].createElement('script');
                script.type = 'text/javascript';
                script.src = this.src;
                $document[0].body.appendChild(script);

                return this.deferred.promise;
            };
        };
        var vd = new VideoData();

        window[funcName] = function(data) {
            vd.deferred.resolve(data);
            return data;
        };

        return vd;
    }]);



     /**
     * Provide an object that wraps a FormData and a XMLHttpRequest
     * to upload files. Returns a promise with request info.
     */
    app.factory('FormUpload', ['createXMLHTTPObject', '$q', function(createXMLHTTPObject, $q){
        return function() {

            var formData = new FormData();

            this.addField = function(name, value) {
                formData.append(name, value);
            };

            this.sendTo = function(url) {
                var deferred = $q.defer();

                formData.append('csrfmiddlewaretoken',
                                /csrftoken=(\w+)/.extract(document.cookie, 1));

                var oReq = createXMLHTTPObject();

                oReq.onreadystatechange = function(){
                    if(this.readyState !== 4) return;

                    var response = {};
                    response.data = angular.fromJson(this.responseText || '{}');
                    response.status = this.status;

                    if( this.status === 200  ) {
                        deferred.resolve(response);
                    } else {
                        deferred.reject(response);
                    }
                };

                oReq.open('POST', url, true);
                oReq.send(formData);

                return deferred.promise;
            };
        };
    }]);

     /**
     * Give a function that send _method=OPTIONS to django rest_framework
     * URL informed and return a promise with result.
     */
    app.factory('getRestOptions', ['$http', function($http){
        return function(url){
            return $http({
                method:'POST',
                url: url,
                data:'_method=OPTIONS',
                headers:{'Content-Type':'application/x-www-form-urlencoded'}
            });
        };
    }]);

     /**
     * returns a function that creates XMLHttpRequest for different browsers
     */
    app.factory('createXMLHTTPObject', function(){
            var XMLHttpFactories = [
                function () {return new XMLHttpRequest();},
                function () {return new window.ActiveXObject('Msxml2.XMLHTTP');},
                function () {return new window.ActiveXObject('Msxml3.XMLHTTP');},
                function () {return new window.ActiveXObject('Microsoft.XMLHTTP');}
            ];

            function createXMLHTTPObject() {
                var xmlhttp = false;
                for (var i=0;i<XMLHttpFactories.length;i++) {
                    try {
                        xmlhttp = XMLHttpFactories[i]();
                    }
                    catch (e) {
                        continue;
                    }
                    break;
                }
                return xmlhttp;
            }
            return createXMLHTTPObject;
        });


})(angular);


