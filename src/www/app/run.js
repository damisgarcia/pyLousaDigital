'use strict';

/**
 * @ngdoc function
 * @author Damis Garcia
 * @name pyLousaDigitalApp.run
 * @description
 * # pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')

.run(function($rootScope,$templateCache,$http,$state,$interval){
  $rootScope.$token = false
  $rootScope.$log = []
  $rootScope.$isRecording = false

  $rootScope.$capture = function(){
    var mode = $('.tm-choise-mode .uk-button.uk-active').attr("data-mode")
    var url = "/capture/new?mode=" + mode

    if(mode == null || mode == undefined){
      alert("Por favor selecione um modo de captura")
      return false
    }

    $http.get(url).success(function(data){
      $rootScope.$isRecording = true
      $rootScope.$log.push(data)
      $state.transitionTo($rootScope.$previousState,null,{reload: true}) // Reload View
    })

  }

  $rootScope.$stop = function(){
    $http.get("/capture/save").success(function(data){
      $rootScope.$isRecording = false
      $rootScope.$freeze = false
      $rootScope.$process = null
      $state.transitionTo("media",null,{reload: true}) // Reload View
    })

    $rootScope.$process = "Aguarde um instante ...";
    $rootScope.$freeze = true;
  }

  $rootScope.$on('$stateChangeSuccess', function(event, to, toParams, from, fromParams) {
    $rootScope.$previousState = from;
  });

  // Get Auth Token
  $http.get("/auth/token/get").success(function(data){
    $rootScope.$token = data.token
    $rootScope.$profile = data.profile
  })

  /** Observers **/
  function isOnline(){
    $http.get("/connection").success(function(data){
      $rootScope.$connection = data
    })
  }

  isOnline()
  $interval(isOnline,15000)
})
