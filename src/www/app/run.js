'use strict';

/**
 * @ngdoc function
 * @author Damis Garcia
 * @name pyLousaDigitalApp.run
 * @description
 * # pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')

.run(function($rootScope,$templateCache,$http,$state,$interval,$filter){
  $rootScope.$token = false
  $rootScope.$screen = window.screen
  $rootScope.$devices = {}
  $rootScope.$framerate = 25

  $rootScope.$log = []
  $rootScope.$isRecording = false

  $rootScope.$capture = function(){
    var mode = $('.tm-choise-mode .uk-button.uk-active').attr("data-mode")
    var url = "/capture/new"

    if(mode == null || mode == undefined){
      alert("Por favor selecione um modo de captura")
      return false
    }

    var params = "?"
    params += "mode="+mode+"&"
    params += "audiodevice=" + $rootScope.$devices.default_microphone.value +"&"
    params += "audiochannel=" + $rootScope.$devices.default_microphone.channel

    if(mode != 1){
      params += "&videodevice=" + $rootScope.$devices.default_camera
    }

    url += params

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

  // Get Devices
  $http.get("/devices/list/webcam").success(function(data){
    $rootScope.$devices.cameras = data.devices
    // default
    $rootScope.$devices.default_camera = data.devices[0]
  })

  $http.get("/devices/list/mic").success(function(data){
    var devices = $filter('filter')(data.devices,"hw:")
    $rootScope.$devices.microphones = []

    angular.forEach(devices,function(device,index){
      var value = device.name.match(/(hw:[\w\d,]+)/)[0]
      var microphone = { name:device.name, value:value, channel:device.channel }
      $rootScope.$devices.microphones.push(microphone)
    })

    // default
    $rootScope.$devices.default_microphone = $rootScope.$devices.microphones[0]    
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
