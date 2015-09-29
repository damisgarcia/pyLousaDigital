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
        ele.filename = ele.filename.match(/[\w\d\.\-\_]+$/)[0]
      })

      angular.forEach(data.recorders,function(ele,index){
        ele.filename.match(/\.jpg$/) ? $scope.repository.thumbnails.push(ele) : $scope.repository.media.push(ele)
      })
    })
  });
