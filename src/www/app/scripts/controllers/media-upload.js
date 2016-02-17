'use strict';

/**
 * @ngdoc function
 * @name pyLousaDigitalApp.controller:MediaUploadCtrl
 * @description
 * # MediaUploadCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')
  .controller('MediaUploadCtrl', function ($scope,$rootScope,$stateParams,$state,$http,$timeout,flash) {
    var self = this
    self.media = $scope.repository.media[$stateParams.id]
    self.thumb = $scope.repository.thumbnails[$stateParams.id]
    self.tags = []

    self.uploaded = false
    self.seding = false

    this.upload = function(){
      var url = "/capture/upload"
      var params = "?"
      params += "access_token="+$rootScope.$token+"&"
      params += "lesson_id="+this.lesson_id+"&"
      params += "title="+this.title+"&"
      params += "description="+this.description+"&"
      params += "privilege="+this.private+"&"
      params += "archive="+this.thumb.name

      url += params

      $http.get(url).success(function(data){
        if(!!data.success){
          self.uploaded = data.success
          self.seding = false
        } else{
          var message = error.hasOwnProperty("message") || "Falha no envio por favor tente novamente"
          $rootScope.$flash_danger(message)
          self.seding = false
        }
      }).error(function(error){
        var message = error.hasOwnProperty("message") || "Falha no envio por favor tente novamente"
        $rootScope.$flash_danger(message)
        self.seding = false
      })

      self.seding = true
    }

    this.back = function () {
      if(!self.seding)
        $state.transitionTo('media',null,{reload: false}) // Reload View
    }

    this.autocomplete = function(){
      return self.tags
    }
  });
