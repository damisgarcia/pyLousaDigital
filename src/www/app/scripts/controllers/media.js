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

    $scope.edit = function(index){
      $scope.edit_dialog = true
      $scope.$obj = $scope.repository.thumbnails[index]
      $scope.$obj.$id = index
      $scope.$obj.new_name = $scope.$obj.name      
    }

    $scope.update = function(index){
      var obj = $scope.repository.thumbnails[index]
      var params = "old="+obj.name+"&new="+obj.new_name
      var url = "/capture/update?"+params
      $http.get(url).success(function(data){
        $scope.edit_dialog = false
        obj.name = obj.new_name
      })
    }

    $scope.remove = function(index){
      var obj = $scope.repository.thumbnails[index]
      var params = "id="+index
      var url = "/capture/destroy?"+params
      if(confirm("Deseja realmente apagar este arquivo?")){
        $http.get(url).success(function(data){
          $scope.repository.thumbnails.splice(index,1)
          $scope.repository.media.splice(index,1)
        })
      }
    }

  })

  .directive('dialogEditRecord',function(){
    return {
      restrict: "E",
      templateUrl:"app/templates/dialog-edit-record.html"
    }
  })

  .directive('dialogUploadRecord',function(){
    return {
      restrict: "E",
      templateUrl:"app/templates/dialog-upload-record.html"
    }
  })
