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
    self.uploaded = false
    self.submit_text = null

    this.upload = function(){
      var url = "/capture/upload"
      var params = "?"
      params += "access_token="+$rootScope.$token+"&"
      params += "lesson_id="+this.lesson_id+"&"
      params += "archive="+this.thumb.name

      url += params

      $http.get(url).success(function(data){
        $timeout(function(){
          self.uploaded = data.success
          self.submit_text = null
        },1500)
      }).error(function(error){
        flash('danger',(error.message || "Falha no envio por favor tente novamente"))
        self.submit_text = null
      })

      self.submit_text = "Enviando Captura por favor aguarde alguns instantes"
    }

    this.back = function () {
      if(!self.submit_text)
        $state.transitionTo('media',null,{reload: true}) // Reload View
    }
  });
