'use strict';

/**
 * @ngdoc function
 * @author Damis Garcia
 * @name pyLousaDigitalApp.config
 * @description
 * # pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp',['ui.router'])
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");

    $stateProvider
      .state('media', {
        url: "/",
        templateUrl: "app/views/media.html",
        controller: "MediaCtrl"
      })

      .state('media.detail', {
        url: "/media/:id",
        templateUrl: "app/views/media-detail.html",
        controller: "MediaDetailCtrl"
      })

      .state('lessons', {
        url: "/lessons",
        templateUrl: "app/views/lessons.html"
      })

      .state('account', {
        url: "/account",
        templateUrl: "app/views/account.html"
      })

      .state('settings', {
        url: "/settings",
        templateUrl: "app/views/settings.html"
      })
    })

    .directive('dialogStartRecord',function(){
      return {
        restrict: "E",
        templateUrl:"app/templates/dialog-start-record.html"
      }
    })

    .run(function($rootScope,$http,$state,$interval){
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
        })
      }

      $rootScope.$stop = function(){
        $http.get("/capture/save").success(function(data){
          $rootScope.$isRecording = false
          $rootScope.$log.push(data)
          $state.go($state.current, {reload: true}); // Reload View
        })
      }

      // Observers
      function isOnline(){
        $http.get("/connection").success(function(data){
          $rootScope.$connection = data
        })
      }

      isOnline()
      $interval(isOnline,5000)
    })
