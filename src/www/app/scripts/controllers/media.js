'use strict';

/**
 * @ngdoc function
 * @author Damis Garcia
 * @name pyLousaDigitalApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')
  .controller('MediaCtrl', function ($rootScope, $scope ,$state ,$http) {
    $scope.repository = { media:[], thumbnails:[] }
    $scope.state = $state

    $http.get("/repository/list").success(function(data){
      angular.forEach(data.recorders,function(ele,index){
        ele.path = ele.path.replace("www/","")
        var regex = ele.filename.match(/^([\w\d\S]+)\/([\w\d\S]+)\.([\w\d]+)/)
        ele.extension = regex[3]
        ele.name = regex[2]
      })

      angular.forEach(data.recorders,function(ele,index){
        ele.extension == "jpg" ? $scope.repository.thumbnails.push(ele) : $scope.repository.media.push(ele)
      })
    })
  });
