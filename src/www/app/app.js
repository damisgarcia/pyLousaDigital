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

    .run(function($rootScope,$http,$state){
      $rootScope.$log = []
      $rootScope.$isRecording = false

      $rootScope.$capture = function(){
        $http.get("/capture/new").success(function(data){
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
    })
